from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import session

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





@app.route("/")
def home():
    # if 'username' in session:
    #     print(request.remote_addr)
    # else:
    #     session['username'] = request.remote_addr


    return render_template('base.html')


@app.route('/question', methods=['POST'])
def question():
    
    data = request.json['question']

    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": data}]
    )
    return {'answer': chat_completion.choices[0].message.content}

    return {'answer': 'Answer from BOT'}

if __name__ == '__main__':
    port = 60
    app.run(host='0.0.0.0', port=port, debug=True)