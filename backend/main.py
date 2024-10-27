from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import random
import csv
from openai import OpenAI

app = FastAPI()

class PhrasalVerbService:
    def __init__(self, csv_file='phrasal-verb.csv'):
        self.csv_file = csv_file

    def get_random_phrasal_verb(self):
        with open(self.csv_file, 'r') as file:
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

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key="dummy_key")

    def set_api_key(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def get_client(self):
        if self.client.api_key == "dummy_key":
            raise HTTPException(status_code=400, detail="OpenAI API key not set")
        return self.client

    async def get_nouns_for_phrasal_verbs(self, phrasal_verbs: List[str]) -> List[str]:
        prompt = f"Generate 5 common nouns that could be used to make sentences with these phrasal verbs: {', '.join(phrasal_verbs)}. Provide only the nouns, separated by commas."
        
        response = self.get_client().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            n=1,
            temperature=0.7,
        )
        
        return [noun.strip() for noun in response.choices[0].message.content.split(',')]

openai_service = OpenAIService()
phrasal_verb_service = PhrasalVerbService()

@app.get("/")
async def root():
    return {"message": "Welcome to my lemonade stand!"}


@app.get("/random-phrasal-verb")
async def random_phrasal_verb():
    return phrasal_verb_service.get_random_phrasal_verb()

class PhrasalVerbRequest(BaseModel):
    phrasal_verbs: List[str]

class NounResponse(BaseModel):
    nouns: List[str]

@app.post("/getNounForMakeSentence", response_model=NounResponse)
async def get_noun_for_make_sentence(request: PhrasalVerbRequest):
    try:
        nouns = await openai_service.get_nouns_for_phrasal_verbs(request.phrasal_verbs)
        return {"nouns": nouns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

class APIKeyRequest(BaseModel):
    api_key: str

@app.post("/set-api-key")
async def set_api_key(request: APIKeyRequest):
    openai_service.set_api_key(request.api_key)
    return {"message": "API key set successfully"}
