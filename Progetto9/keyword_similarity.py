import os
import pandas as pd
from dotenv import load_dotenv
import db_operations
import yake
import spacy
import numpy as np

#%% Dotenv permette di recuperare le variabili d'ambiente da un file .env
load_dotenv("../.env")

INPUT_DB_HOST = os.getenv("INPUT_DB_HOST")
INPUT_DB_NAME = os.getenv("INPUT_DB_NAME")
INPUT_DB_USER = os.getenv("INPUT_DB_USER")
INPUT_DB_PASSWORD = os.getenv("INPUT_DB_PASSWORD")
INPUT_DB_PORT = int(os.getenv("INPUT_DB_PORT"))

OUTPUT_DB_HOST = os.getenv("OUTPUT_DB_HOST")
OUTPUT_DB_NAME = os.getenv("OUTPUT_DB_NAME")
OUTPUT_DB_USER = os.getenv("OUTPUT_DB_USER")
OUTPUT_DB_PASSWORD = os.getenv("OUTPUT_DB_PASSWORD")
OUTPUT_DB_PORT = int(os.getenv("OUTPUT_DB_PORT"))

create_table_query = """CREATE TABLE IF NOT EXISTS argomenti (
                            id INT PRIMARY KEY,
                            descrizione TEXT NOT NULL)"""

db_operations.create_table(INPUT_DB_HOST, INPUT_DB_NAME, INPUT_DB_USER, INPUT_DB_PASSWORD, INPUT_DB_PORT, create_table_query)

dati = [
        (1, "It discusses the importance of early detection and the various treatment options available. For example, regular screenings can help detect cancer early, improving treatment outcomes."),
        (2, "It emphasizes the significance of a balanced diet and regular exercise in maintaining overall well-being. For instance, incorporating fruits and vegetables into daily meals can boost health."),
        (3, "It covers the advancements in technology and the impact of electric vehicles on the environment. For example, electric cars reduce carbon emissions compared to traditional gasoline vehicles."),
        (4, "It explains the role of chemical reactions in everyday life and the importance of safety measures in handling chemicals. For instance, understanding how household cleaners react can prevent accidents."),
        (5, "It highlights the importance of financial planning and investment strategies for securing one's future. For example, creating a budget can help manage expenses and save for retirement."),
        (6, "It covers effective sales techniques and the importance of understanding customer needs to drive business growth. For instance, personalized marketing can increase customer satisfaction and sales.")
        ]

insert_query = """
    INSERT INTO argomenti (id, descrizione) 
    VALUES (:id, :descrizione)
    ON CONFLICT (id) DO NOTHING;
"""

db_operations.insert_data(INPUT_DB_HOST, INPUT_DB_NAME, INPUT_DB_USER, INPUT_DB_PASSWORD, INPUT_DB_PORT, insert_query, dati)

df = db_operations.read_data(INPUT_DB_HOST, INPUT_DB_NAME, INPUT_DB_USER, INPUT_DB_PASSWORD, INPUT_DB_PORT,
                             "SELECT * FROM argomenti;")
print(df)

nlp = spacy.load("en_core_web_md")

sentences = df["descrizione"]

def extract_keywords(text):
    return [kw for kw, _ in yake.KeywordExtractor(lan="en", n=1, top=3).extract_keywords(text)]

def keyword_similarity(kw1, kw2):
    best_pair = None
    max_sim = 0
    similarities = []
    
    for w1 in kw1:
        for w2 in kw2:
            sim = nlp(w1).similarity(nlp(w2))
            similarities.append(sim)
            if sim > max_sim:
                max_sim = sim
                best_pair = (w1, w2)
    
    avg_similarity = np.mean(similarities) if similarities else 0
    return avg_similarity, best_pair, similarities

keywords_list = [extract_keywords(sentence) for sentence in sentences]

similarity_data = []
for i, kw1 in enumerate(keywords_list):
    for j, kw2 in enumerate(keywords_list):
        if i < j:
            avg_similarity, best_pair, similarities = keyword_similarity(kw1, kw2)
            similarity_data.append({
                "frase_x": f"Frase {i+1}",
                "frase_y": f"Frase {j+1}",
                "similarity": avg_similarity,
                "keywords_x": kw1,
                "keywords_y": kw2,
                "miglior_coppia": best_pair,
                "similarità:": similarities
            })

df_similarity = pd.DataFrame(similarity_data)

print(df_similarity)
df_similarity.to_csv("Progetto9/similarity.csv", index=False)