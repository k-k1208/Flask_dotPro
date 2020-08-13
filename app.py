
# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
# 日本語でコメント書くため,utf-8の文字コードと宣言
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def prime_judge(x):
    judge = True
    for i in range(2, x):
        if x % i == 0:
            judge = False
        else:
            pass
    if judge == True:
        judge="素数"
    elif judge == False:
        judge="素数じゃない"
    else:
        judge="予想外のことが起きているで"
    return judge


'''
json.load(f)
と

s = f.read()
json.loads(s)
は同じ

loadsのsはstringのs

'''
def get_profile():
    # JSONファイルの読み込み
    with open("data/profile.json", 'r') as f:
        prof_dict = json.load(f)
    user_list = list(prof_dict.keys())
    return prof_dict, user_list

# エンコード（JSON形式に変換）→json.dumps（）メソッド
# デコード（JSON形式から自分のプログラムで使用できる形式に変換) →json.loads（）メソッド

def update_profile(prof_dict):
    with open('data/profile.json', 'w') as f:
        json.dump(prof_dict, f, indent=4)  # prof_dictをfに代入

'''
request.args: the key/value pairs in the URL query string
request.form: the key/value pairs in the body, from a HTML post form, or JavaScript request that isn't JSON encoded


request.form['name']: use indexing if you know the key exists
request.form.get('name'): use get if the key might not exist
'''


@app.route('/get')
def get():
    # get削除した。　i.e. request.args.get("number", 100)などでkeyがない時の例外処理(この場合は100をいれる)をするときget使う。
    number = int(request.args['number'])
    judge = prime_judge(number)
    return render_template('get.html', title='Flask GET request', prime_or_not=judge, number=number)

@app.route('/profile')
def profile():
    prof_dict, user_list = get_profile()
    return render_template('profile.html', title='json', prof_dict=prof_dict, user_list=user_list)

@app.route('/edit/<id>')  # urlにusername変数部分を付加(パスパラメータ)
def edit(id):
    prof_dict, _ = get_profile()
    prof_dict = prof_dict[id]
    return render_template('edit.html', title='json', user=prof_dict, id=id)

@app.route('/update/<id>', methods=['POST'])
def update(id):
    prof_dict, _ = get_profile()

    # prof_dictの値を変更
    prof_dict[id]['name'] = request.form['name']
    prof_dict[id]['age'] = request.form['age']
    prof_dict[id]['sex'] = request.form['sex']

    update_profile(prof_dict)
    return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(debug=True)