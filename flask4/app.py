
# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
# 日本語でコメント書くため,utf-8の文字コードと宣言
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)


#  flask3 :json file形式
#  flask4 :DBfile形式
def get_profile():
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    prof_list=[]
    for i in c.execute('select * from persons'):
        prof_list+=[{'id':i[0],'name':i[1],'age':i[2],'sex':i[3]}]
    conn.commit()
    conn.close()
    return prof_list


'''
execute(sql[, parameters]) :表記法は二種類 qmark or named

# This is the qmark style:
cur.execute("insert into people values (?, ?)", (who, age))

# And this is the named style:
cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})
'''


def update_profile(prof_dict):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('UPDATE persons SET NAME=?,age=?,sex=? WHERE id=?',
              (prof_dict['name'], prof_dict['age'], prof_dict['sex'], prof_dict['id']))  # qmark style
    conn.commit()
    conn.close()




'''
request.args: the key/value pairs in the URL query string
request.form: the key/value pairs in the body, from a HTML post form, or JavaScript request that isn't JSON encoded


request.form['name']: use indexing if you know the key exists
request.form.get('name'): use get if the key might not exist
'''


@app.route('/profile')
def profile():
    prof_dict = get_profile()
    return render_template('profile.html', title='json', user=prof_dict)


@app.route('/edit/<int:id>')
def edit(id):
    prof_list = get_profile()
    prof_dict = prof_list[id-1]
    return render_template('edit.html', title='sql', user=prof_dict)

# addする情報をformにinputしてpostするためのhtmlページに遷移させる部分
@app.route('/add')
def add():
    return render_template('add.html', title='新規ユーザー登録')


#  dotPro公式回答ではupdateのように　insert_profile関数を別に作っている。
@app.route('/insert', methods=['POST'])
def insert():
    person_name = request.form['name']
    person_age = request.form['age']
    person_sex = request.form['sex']
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('INSERT INTO persons (name, age, sex) VALUES (?, ?, ?)', (person_name, person_age, person_sex))
    conn.commit()
    conn.close()
    return redirect(url_for('profile'))


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    prof_list = get_profile()
    prof_dict = prof_list[id-1]
    # prof_dictの値を変更
    prof_dict['name'] = request.form['name']
    prof_dict['age'] = request.form['age']
    prof_dict['sex'] = request.form['sex']
    update_profile(prof_dict)

    return redirect(url_for('profile'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('DELETE FROM persons WHERE id=(?)', (id,))  # (id,)の部分気持ち悪いけど、こう書かないとダメらしい、、
    conn.commit()
    conn.close()
    return redirect(url_for('profile'))

if __name__ == "__main__":
    app.run(debug=True)