import json
import numpy as np
import pymysql
import os
from openai import OpenAI
import linebot

# Set the OpenAI API key from environment variables
client = OpenAI()

def get_embedding(model, text):
    embedding = client.embeddings.create(
        input=text,
        model=model
    )
    return embedding.data[0].embedding

def get_response(model, prompt, system=None):
    messages = []

    # Add system messages
    if system:
        if isinstance(system, str):
            system = [system]
        elif not isinstance(system, list):
            return "system Value Error, please input list or string"
        
        for sys_message in system:
            messages.append({
                "role": "system", "content": sys_message
            })

    # Add prompt messages
    if isinstance(prompt, str):
        prompt = [prompt]
    elif not isinstance(prompt, list):
        return "prompt Value Error, please input list or string"
    
    for pro_message in prompt:
        messages.append({
            "role": "user", "content": pro_message
        })

    # Get response from ChatGPT
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content

def calculate_similar_text(prompt):
    with open("./json/embeddings_anime.json", "r") as json_file:
        index = json.load(json_file)

    prompt = prompt.replace("\n", "")
    vec = get_embedding(text=prompt)

    results = []
    for i in index:
        similarity = np.dot(np.array(i["embedding"]), vec)
        results.append({"body": i["body"], "similarity": similarity})
    
    text_list = sorted(
        results, key=lambda x: x['similarity'], reverse=True
    )[:3]

    return text_list

def insert_message(user_id, message, reply):
    # Set up database connection (adjust as needed)
    connection = pymysql.connect(
        host=os.environ.get("HOST"),
        user=os.environ.get("USER"),
        password=os.environ.get("PASSWORD"),
        database=os.environ.get("DB_NAME"),
        connect_timeout=10,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # Use placeholders in SQL statement
            sql = "INSERT INTO all_message (user_id, message, reply) VALUES (%s, %s, %s)"
            # Execute the SQL command with the provided values
            cursor.execute(sql, (user_id, message, reply))
        # Commit the changes to the database
        connection.commit()
    finally:
        # Close the database connection
        connection.close()

def handler(event, context):
    body = json.loads(event["body"])
    events = body['events'][0]

    # ログの作成
    print(f"body:\t{body}")

    reply_token = events['replyToken']
    message_type = events['message']['type']
    user_id = events['source']['userId']
    message_id = events['message']['id']

    if message_type == "text":
        prompt = events['message']['text']

        similar_texts = calculate_similar_text(prompt)

        system = []
        for text in similar_texts:
            system.append(text['body'])
        system.append(
        """
        You are an anime recommendation system. Based on the user's query, 
        you have identified three animes that are numerically the closest matches. 
        Present these three animes as recommendations to the user, highlighting 
        how each anime relates to their query.
        """
        )

        response = get_response("gpt-4-1106-preview", prompt, system)

        linebot.send_message(reply_token, response)

        insert_message(user_id, prompt, response)

    else: 
        text = "This message format or structure is not supported"
        linebot.send_message(reply_token, text)
        
    return