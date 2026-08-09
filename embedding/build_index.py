import json 
import sys
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import PROCESSED_DIR, FAISS_INDEX_PATH, EMBEDDING_MODEL

def load_chunks():
    chunks_path = PROCESSED_DIR / "chunks.jsonl"
    if not chunks_path.exists():
        raise FileNotFoundError(
            f"{chunks_path} not found"
        )
    chunks = []
    with open(chunks_path) as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def chunks_to_document(chunks : list)->list[Document]:
    doc = []
    for c in chunks:
        doc.append(
            Document(
                page_content=c["text"],
                metadata={k: v for k, v in c.items() if k != "text"},
            )
        )
    return doc

def build_index():
    chunks = load_chunks()

    doc = chunks_to_document(chunks)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vectorstore = FAISS.from_documents(doc , embeddings)
    vectorstore.save_local(str(FAISS_INDEX_PATH))
    return vectorstore

if __name__ == "__main__":
    build_index()

