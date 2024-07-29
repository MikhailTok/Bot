from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import url_for
from flask import session
from flask import redirect
import sqlite3

import requests
import json

from db import create_database

# # importing other libraries
# import requests
# from PIL import Image

import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables


app = Flask(__name__)

# app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


from openai import OpenAI

client = OpenAI(
    api_key=os.environ['API_KEY'],
    base_url=os.environ['BASE_URL'],
)


def get_balance():
    headers = {"Authorization": f"Bearer {os.environ['API_KEY']}"}
    x = requests.get('https://api.proxyapi.ru/proxyapi/balance', headers=headers)
    balance = json.loads(x.content.decode('utf-8'))['balance']
    return balance


def sql_request(sql):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute(sql)
    out = c.fetchall()
    conn.close()
    return out


def write_to_db(user_id, ip, question, answer):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (user_id, ip, question, answer) VALUES (?, ?, ?, ?)",  (user_id, ip, question, answer))
    conn.commit()
    conn.close()


@app.route('/admin')
def index():
    return render_template('admin.html', tasks=sql_request('SELECT * FROM tasks'))


@app.route("/")
def home():
    current_dialogue = None
    if request.cookies.get('user_id'):
        current_dialogue = sql_request(f"SELECT * from tasks WHERE user_id = {request.cookies.get('user_id')}")

    resp = make_response(render_template('base.html', balance=get_balance(), dialogues=current_dialogue))

    if not request.cookies.get('user_id'):
        user_id = str(sql_request('SELECT max(user_id) FROM tasks')[0] + 1)
        resp.set_cookie('user_id', user_id)
    return resp


@app.route('/question', methods=['POST'])
def question():

    data = request.json['question']

    new_dialogue = request.json['dialogue']

    print("new_dialogue", new_dialogue)

    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": data}]
    )

    answer = chat_completion.choices[0].message.content

    write_to_db(request.cookies.get('user_id'), request.remote_addr, data, answer)

    return {'answer': answer}

    return {'answer': 'Answer from BOT'}


if __name__ == '__main__':
    create_database()
    port = 60
    app.run(host='0.0.0.0', port=port, debug=True)




