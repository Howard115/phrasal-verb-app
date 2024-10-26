from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import random
import csv
from openai import OpenAI

app = FastAPI()

# Initialize the OpenAI client with a dummy key
client = OpenAI(api_key="dummy_key")

def get_openai_client():
    if client.api_key == "dummy_key":
        raise HTTPException(status_code=400, detail="OpenAI API key not set")
    return client

@app.get("/")
async def root():
    return {"message": "Welcome to my lemonade stand!"}

@app.get("/menu")
async def menu():
    return {"lemonade": ["Classic", "Strawberry", "Mint"]}

@app.get("/random-phrasal-verb")
async def random_phrasal_verb():
    with open('phrasal-verb.csv', 'r') as file:
        csv_reader = csv.reader(file)
        phrasal_verbs = list(csv_reader)
    
    # Remove header if present
    if not phrasal_verbs[0][0].isdigit():
        phrasal_verbs = phrasal_verbs[1:]
    
    chosen_verb = random.choice(phrasal_verbs)
    
    return {
        "phrasal_verb": chosen_verb[0],
        "meaning": chosen_verb[1],
        "example": chosen_verb[2]
    }

class PhrasalVerbRequest(BaseModel):
    phrasal_verbs: List[str]

class NounResponse(BaseModel):
    nouns: List[str]

@app.post("/getNounForMakeSentence", response_model=NounResponse)
async def get_noun_for_make_sentence(request: PhrasalVerbRequest, openai_client: OpenAI = Depends(get_openai_client)):
    try:
        prompt = f"Generate 5 common nouns that could be used to make sentences with these phrasal verbs: {', '.join(request.phrasal_verbs)}. Provide only the nouns, separated by commas."
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            n=1,
            temperature=0.7,
        )
        
        nouns = [noun.strip() for noun in response.choices[0].message.content.split(',')]
        return {"nouns": nouns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

class APIKeyRequest(BaseModel):
    api_key: str

@app.post("/set-api-key")
async def set_api_key(request: APIKeyRequest):
    global client
    client = OpenAI(api_key=request.api_key)
    return {"message": "API key set successfully"}



