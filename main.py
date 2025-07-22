# main.py
import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware # Ensure this is imported

load_dotenv()

app = FastAPI()

# --- VERIFY THIS MIDDLEWARE CONFIGURATION ---
# This setup is designed to correctly handle preflight OPTIONS requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including OPTIONS, GET, POST
    allow_headers=["*"],  # Allows all headers
)
# --- END OF MIDDLEWARE CONFIGURATION ---

@app.get("/")
async def read_root():
    return FileResponse('/Users/krishchandra/Desktop/LEXA-CHAIN/frontend/index.html')

class ContractRequest(BaseModel):
    prompt: str

@app.post("/create-and-execute")
async def create_and_execute_contract(request: ContractRequest):
    try:
        # Your logic here
        return {"status": "success", "message": "Request received!", "prompt": request.prompt}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Change the port number here
    uvicorn.run(app, host="0.0.0.0", port=8001) 

