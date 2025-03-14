from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import chromadb

from transformers import pipeline
from sentence_transformers import SentenceTransformer
from datetime import datetime
import os

import spacy


# Connexion à ChromaDB en mode client/serveur (port 8000)
client = chromadb.PersistentClient('./chromadb')

nlp = spacy.load("fr_core_news_md")



def chunk_text(text, chunk_size=1024):
    return nlp(text)[:chunk_size].text



folder="/root/airflow/data/convert_documents/"




def add_to_chromadb():
    # 1. pour les embeddings de documents
    print(True)
    doc_collection = client.get_or_create_collection("document_embeddings")
    print(doc_collection.get())

    files = os.listdir(folder)
    
    # Lecture des fichier du dossier convert_document et vérification de la présence du 
    collect_id = client.get_or_create_collection('document_embeddings').get()['ids']
    embedding_model = 'all-MiniLM-L6-v2'
    model = SentenceTransformer(embedding_model)
    
    print(files, collect_id)
    for file in files:
        if file not in collect_id:
            # 1. modèle d'embeddings
            
            print('Fichier trouvé ------->',file)
            
            with open(folder + file + '/' + file+'.md', 'r') as f:
                data = f.read()
        
            # Ajout dans la base de données Chromadb
            #document_embedding = model.encode([raw_text])
            #print(document_embedding)
            print('Summary -------->',data )
            doc_collection.add(ids=str(file), 
                               documents=data
                               #embeddings=document_embedding, 
                               #metadatas=[{"id": str(file), "text": raw_text}]
                               )

            print(doc_collection.get()['ids'])
            return file




def summary(ti):
    file = ti.xcom_pull('task_add_text_to_cromadb')
    print(file)

    #doc_collection = client.get_or_create_collection("document_embeddings")


    # 2. pour les embeddings de résumés
    summary_collection = client.get_or_create_collection("summary_embeddings")

    # 2. modèle de résumé
    summarizer_model = "facebook/bart-large-cnn"
    summarizer = pipeline("summarization", model=summarizer_model)
    # Générer le résumé

    #summary = summarizer(raw_text, min_length=15, max_length=130, do_sample=False)
    #summary_text = summary[0]['summary_text']
    # Générer l'embedding du résumé
    #summary_embedding = model.encode([summary_text])
    #summary_collection.add(ids=str(file), embeddings=summary_embedding, metadatas=[{"id": str(file), "text": summary_text}])

    pass

with DAG(
    'text_summary_dag',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@once',
    catchup=False,
    end_date=datetime(2025, 10, 10),
    ):
    
    task_add_text_to_cromadb = PythonOperator(
        task_id ='task_add_text_to_cromadb',
        python_callable=add_to_chromadb
    )

    task_add_summary = PythonOperator(
        task_id = 'task_add_summary',
        python_callable=summary
    )

task_add_text_to_cromadb >> task_add_summary
