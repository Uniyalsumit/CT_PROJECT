import sys 
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import (FAISS_INDEX_PATH, EMBEDDING_MODEL, MMR_FETCH_K, MMR_K, MMR_LAMBDA_MULT , RERANKER_MODEL_NAME)

store = None
reranker = None
def load_vectorestore() ->FAISS:
    global store
    if store is None:
        Embedding = HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL)
        store = FAISS.load_local(
            str(FAISS_INDEX_PATH),
            Embedding,
            allow_dangerous_deserialization=True
        )
    return store

def load_reranker() -> CrossEncoder:
    global reranker
    if reranker is None:
        reranker = CrossEncoder(RERANKER_MODEL_NAME)
    return reranker

def get_retrieval():
    vector_store = load_vectorestore()
    return vector_store.as_retriever(
        search ="mmr",
        searcj_kwargs={
            "k":MMR_K,
            "fetch_k":MMR_FETCH_K,
            "lambda_mult":MMR_LAMBDA_MULT
        },
    )

def rerank(query : str , docs: list , top_k:int = 4) ->list:
    if len(docs) <= top_k:
        return docs
    Ranker = load_reranker()
    scores =Ranker.predict([(query , d.page_content) for d in docs])
    ranked = sorted(zip(docs , scores),key=lambda x:x[1] , reverse=True)
    return [doc for doc , _ in ranked[:top_k]]


def retrieve(query : str):
    retriever = get_retrieval()
    ink = retriever.invoke(query)
    return rerank(query , ink , 4)

