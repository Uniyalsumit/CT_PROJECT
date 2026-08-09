import os 
import sys 
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent # give path to folder
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
INDEX_DIR = DATA_DIR / "index"
FAISS_INDEX_PATH = INDEX_DIR /"faiss_index"
METADATA_STORE_PATH = INDEX_DIR/"metadata.jsonl"

#make dir if it does not exist 
for d in [RAW_DIR , PROCESSED_DIR , INDEX_DIR]:
    d.mkdir(parents = True , exist_ok= True)


#GIT hub config
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "fastapi"
REPO_NAME = "fastapi"

#LLM and embedding models
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

#CHUNKING
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# retrival (MMR)
MMR_K = 6            
MMR_FETCH_K = 20     
MMR_LAMBDA_MULT = 0.7 

RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

NLI_MODEL_NAME = "cross-encoder/nli-roberta-base"
NLI_ENTAILMENT_THRESHOLD = 0.06


BENCHMARK_PATH = BASE_DIR / "evaluation" / "benchmark_questions.json"
EVAL_RESULTS_DIR = BASE_DIR / "evaluation" / "results"
EVAL_RESULTS_DIR.mkdir(parents=True, exist_ok=True)