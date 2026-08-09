from rag_pipeline.retriver import retrieve
from rag_pipeline.generator import generate_answer
from rag_pipeline.hallucination_gy import guard_answer

def ask(question : str)->dict:
    document = retrieve(question)

    if not document:
        return {
            "answer": "I couldn't find any relevant commits, PRs, or issues for that question.",
            "documents": [],
            "guard": None,
        }

    answer = generate_answer(question , document)
    guard_result = guard_answer(answer , document)

    return{
        "answer" : answer,
        "documents": document,
        "guard" : guard_result,
    }
