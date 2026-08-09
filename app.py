import streamlit as st
from rag_pipeline import ask

st.set_page_config(page_title="PatchContext", layout="wide")
st.title("PatchContext")
st.caption("Ask why FastAPI is designed the way it is — grounded in real commits, PRs, and issues.")

if "history" not in st.session_state:
    st.session_state.history = []


def render_source_badge(meta: dict) -> str:
    if meta.get("source_type") == "commit":
        return f"Commit `{meta.get('sha', '')[:7]}`"
    elif meta.get("source_type") == "pull_request":
        return f"PR #{meta.get('pr_number')}"
    elif meta.get("source_type") == "issue":
        return f"Issue #{meta.get('issue_number')}"
    return "Unknown source"


def render_result(result: dict):
    st.markdown(result["answer"])
    
    guard = result.get("guard")
    if guard is not None:
        if guard["passed"]:
            st.success("Verified — all claims supported, all citations valid.")
        else:
            issues = []
            if not guard["hallucination_check"]["all_supported"]:
                n = len(guard["hallucination_check"]["unsupported_claims"])
                issues.append(f"{n} unsupported claim(s)")
            if not guard["citation_check"]["all_valid"]:
                issues.append(f"invalid citations: {guard['citation_check']['invalid_citations']}")
            st.warning(f" Guardrail flagged this answer — {', '.join(issues)}.")

    if result["documents"]:
        st.markdown("**Sources**")
        st.caption("Documents retrieved for this question")
        for doc in result["documents"]:
            meta = doc.metadata
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(render_source_badge(meta))
                    st.caption(doc.page_content[:200] + ("..." if len(doc.page_content) > 200 else ""))
                with col2:
                    if meta.get("url"):
                        st.link_button("View on GitHub", meta["url"])

with st.sidebar:
    st.header("Filters")
    source_filter = st.multiselect(
        "Source type",
        options=["commit", "pull_request", "issue"],
        default=["commit", "pull_request", "issue"],
    )
    st.caption("Note: filtering applies to displayed sources; retrieval is unfiltered.")
    if st.button("Clear conversation"):
        st.session_state.history = []
        st.rerun()

# Render conversation history
for turn in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(turn["question"])
    with st.chat_message("assistant"):
        render_result(turn["result"])

# Chat input
question = st.chat_input("e.g. Why does FastAPI use Pydantic for request validation?")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving relevant information and generating answer..."):
            result = ask(question)
        render_result(result)

    st.session_state.history.append({"question": question, "result": result})
