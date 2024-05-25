from openai import OpenAI

client = OpenAI()

def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=prompt,
    )
    return response.choices[0].message.content
# these make it attributes instead of keys for hth


prompt = [
    # {"role": "system", "content": "Answer in a way that sonds like yoda"},
    {"role": "user", "content": "Can you give me 3 top anime recommendations if I like anime with a lot of action with a touch of comedy and humor?"}
]

print(get_response(prompt))

def get_embedding(model="text-embedding-ada-002", text="Hello"):
    embedding = client.embeddings.create(
        input=text,
        model=model
    )
    return embedding.data[0].embedding

# print(get_embedding(text="What is the best anime out there?"))