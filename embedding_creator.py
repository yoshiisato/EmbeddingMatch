import json
import openai
import os
import anime_reader

# Set the OpenAI API key from environment variables
openai.api_key = os.getenv('API_KEY')

texts = anime_reader.main()

def get_embedding(text):
    response = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

embeddings_json = []

for text in texts:
    embedding = get_embedding(text)
    embeddings_json.append({
        "text": text,
        "embedding": embedding
    })

with open('embeddings.json', 'w') as outfile:
    json.dump(embeddings_json, outfile, indent=4)
