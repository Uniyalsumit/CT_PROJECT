import sys 
from pathlib import Path

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import LLM_MODEL, GROQ_API_KEY

SYSTEM_PROMPT = """You are PatchContext, an assistant that explains WHY design \
decisions were made in the FastAPI codebase, grounded strictly in the provided \
excerpts from commits, pull requests, and issue threads.
 
Rules:
1. Only use information present in the provided context. Never invent a commit \
SHA, PR number, or issue number that is not explicitly present in the context.
2. Every factual claim must be followed by an inline citation in the format \
[commit abc1234] or [PR #1234] or [issue #567], using values taken directly \
from the context's metadata.
3. If the context does not contain enough information to answer, say so plainly \
instead of guessing.
4. Be concise and technical. Prefer direct explanation over hedging.
"""
USER_PROMPT = """Question: {question}
Context excerpts:
{context}
Answer the question using only the context above, with inline citations."""


def format_context(documents)-> str:
    blocks = []
    for doc in documents:
        meta = doc.metadata
        if meta.get("source_type") == "commit":
            ref = f"[commit {meta.get('sha', '')[:7]}]"
        elif meta.get("source_type") == "pull_request":
            ref =  f"[PR #{meta.get('pr_number')}]"
        elif meta.get("source_type") == "issue":
            ref = f"[issue #{meta.get('issue_number')}]"
        else:
            ref = "[unknown source]"
        blocks.append(f"{ref} {doc.page_content}\nSource URL: {meta.get('url', '')}")
    return "\n\n---\n\n".join(blocks)

def get_generation():
    if not GROQ_API_KEY:
        raise ValueError(
            "not key found GROQ"
        )
    prompt = ChatPromptTemplate(
        [
        ("system", SYSTEM_PROMPT),
        ("user", USER_PROMPT),  
        ]
    )
    llm = ChatGroq(model = LLM_MODEL, api_key=GROQ_API_KEY , temperature = 0)
    return prompt | llm | StrOutputParser()


def generate_answer(question : str , document  : list)-> str:
    chain = get_generation()
    context = format_context(document)
    return chain.invoke({"question" : question , "context": context})
