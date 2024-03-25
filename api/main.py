from dotenv import dotenv_values
from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pinecone import Pinecone
from Neurall import NerualClass

app = Flask(__name__)

queue = []
neural = []

config = dotenv_values(".env")
pc = Pinecone(api_key = config["PINECONE_API_KEY"])
index = pc.Index('secon-1')
embeddings = OpenAIEmbeddings(api_key=config["OPENAI_API_KEY"])
neuralObj = NerualClass(pinecone_api_key=config["PINECONE_API_KEY"], openai_api_key=config["OPENAI_API_KEY"])

class RequiredSchema(Schema):
    username = fields.String(required=True)
    msg_id = fields.String(required=True)
    content = fields.String(required=True)

@app.route('/api/ping', methods = ['GET'])
def Ping():
    print('pong')
    return jsonify({'message': 'pong'})

"""
Queue routes
"""
@app.route('/api/queue', methods = ['GET'])
def GetQueue():
    return jsonify({'queue': queue})

@app.route('/api/queue', methods = ['POST'])
def AddToQueue():
    data = request.get_json()
    print(data, "- получил")
    schema = RequiredSchema()
    try:
        result = schema.load(data)
    except ValidationError as e:
        return "Bad Request", 400

    queue.append((result['UserId'], result['MessageText']))
    return jsonify({'total_entities_neural': f'{len(queue)}'})

"""
Neural Routes
"""

@app.route('/api/neural', methods = ['POST'])
def AddToNeural():
    data = request.get_json()
    schema = RequiredSchema()
    try:
        result = schema.load(data)
    except ValidationError as e:
        return "Bad Request", 400

    # text = str(result)
    # text = text.replace("'", '"')
    # print(text)
    neuralObj.process_data(str(result))
    return jsonify({'content': 'data was added'})

@app.route('/api/neural', methods = ['GET'])
def GetFromNeural():
    data = request.get_json()
    schema = RequiredSchema()
    try:
        result = schema.load(data)
    except ValidationError as e:
        return "Bad Request", 400

    text = result['content']
    result = neuralObj.ask_question(text)
    result = neuralObj.invoke_chat(text, result)
    return jsonify(result)

if __name__ == '__main__':
    print("was started")
    app.run(host = "0.0.0.0", debug=True)