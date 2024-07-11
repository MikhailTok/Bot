from flask import Flask
from flask import render_template
from flask import request

# # importing other libraries
# import requests
# from PIL import Image




app = Flask(__name__)


from openai import OpenAI

# client = OpenAI(
#     api_key="sk-MhBIe95hxEyBZCEm532kQL0pYRPVUpUw",
#     base_url="https://api.proxyapi.ru/openai/v1",
# )





@app.route("/")
def home():
    return render_template('base.html')


@app.route('/question', methods=['POST'])
def question():
    data = request.json['question']

    # print(data)

    # chat_completion = client.chat.completions.create(
    # model="gpt-3.5-turbo", messages=[{"role": "user", "content": data}]
    # )
    # return {'answer': chat_completion.choices[0].message.content}

    return {'answer': 'Answer from BOT'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)