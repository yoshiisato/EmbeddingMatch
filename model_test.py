from openai import OpenAI
import json
import numpy as np

client = OpenAI()

def get_embedding(model="text-embedding-ada-002", text="Hello"):
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
        
        for system_message in system:
            messages.append({
                "role": "system", "content": system_message
            })

    # Add prompt messages
    if isinstance(prompt, str):
        prompt = [prompt]
    elif not isinstance(prompt, list):
        return "prompt Value Error, please input list or string"
    
    for message in prompt:
        messages.append({
            "role": "user", "content": message
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
    
    sorted_list = sorted(results, key=lambda x: x['similarity'], reverse=True)
    closest_list = sorted_list[:3]

    return closest_list

def main():
    prompt = input("What kind of anime do you like?")

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
    print(response)


if __name__ == "__main__":
    main()
