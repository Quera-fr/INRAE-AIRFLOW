from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import requests
import json

class DataStrucure(BaseModel):
    name : str
    age : int
    adresse : str


tags = [
    { 'name' : "Mathématiques",
     'description': "Mathématiques"},

     {
         'name' : 'NLP',
         'description' : 'Traitement du language naturel'
     }
]


app = FastAPI(
    title='My FastAPI',
    description='This is a simple API',
    version='0.0.1',
    openapi_tags=tags
)


@app.get('/', )
def root():
    return 'Hello world'

@app.get('/square',tags=["Mathématiques"])
def square(n:int=5) ->str:
    return str(n*n)


@app.post('/user_login', tags=["Mathématiques"])
def user_login(data:DataStrucure):
    print(data)


@app.post('/upload_file', tags=["NLP"])
def upload_file(file:UploadFile=File(...)):
    my_doc = file.file.read().decode()[2000:3000]

    url = "http://localhost:11434/api/chat"
    prompt = """
    Donne moi une question et une réponse à partir du texte suivant au format : 
    {"messages":[{"role": "user", "content": "Une question que poseras"}, {"role": "assistant", "content": "Une réponse que tu donneras"}]}
    Voici le texte :""" + my_doc 

    data = {
        "model": "llama3.3:latest",  # Remplace par ton modèle (ex: "llama3", "gemma", etc.)
        "prompt":  prompt,
        "stream": False
    }

    response = requests.post('http://localhost:11434/api/generate', json=data)
    text = response.json()['response'].split('```')[1]

    with open("data.jsonl", "a", encoding="utf-8") as file:
        json.dump({"response": text}, file)

    return text