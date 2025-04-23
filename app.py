import os
import gradio as gr
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from chatopt import ChatOPT

# Initialize FastAPI app
app = FastAPI(title="ChatOPT", description="API for generating API specifications and OPT masterplan")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the ChatOPT instance
chat_opt = ChatOPT()

# Define request and response models
class OperatingModelRequest(BaseModel):
    mission_statement: str
    company_name: Optional[str] = None
    industry: Optional[str] = None
    business_size: Optional[str] = None

class APISpec(BaseModel):
    name: str
    description: str
    endpoints: List[Dict]
    build_in_house: bool
    reason: str

class MasterplanResponse(BaseModel):
    markdown_content: str
    api_specs: List[APISpec]
    questions: Optional[List[str]] = None

@app.get("/")
async def root():
    return {"message": "Welcome to ChatOPT API. Use /docs for the API documentation."}

@app.post("/generate_masterplan", response_model=MasterplanResponse)
async def generate_masterplan(request: OperatingModelRequest):
    try:
        # Generate the masterplan using ChatOPT
        result = chat_opt.generate_masterplan(
            mission_statement=request.mission_statement,
            company_name=request.company_name,
            industry=request.industry,
            business_size=request.business_size
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask_questions")
async def ask_questions(request: OperatingModelRequest):
    try:
        # Generate questions to gather more information
        questions = chat_opt.generate_questions(
            mission_statement=request.mission_statement,
            company_name=request.company_name,
            industry=request.industry,
            business_size=request.business_size
        )
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Launch the Gradio interface when run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 