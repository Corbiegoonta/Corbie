from dotenv import load_dotenv
from ai_utils import generate_query_and_result
import streamlit as st

load_dotenv()

st.title("ChatFIN")

st.sidebar.title("Finance Article URLs")

place_holder = st.empty()

place_holder.text("Provide your finance article URLs and ask a question!")

urls = []

for number in range(3):
    url = st.sidebar.text_input(f"URL {number + 1}")
    urls.append(url)

query = place_holder.text_input("Question: ")

if query:
    result = generate_query_and_result(0.9, 500, query, 1000, 200, ["\n\n", "\n", " "], urls)
    st.header("Answer: ")
    st.write(result["answer"])

sources = result.get("sources")

if sources:
    st.subheader("Sources: ")
    source_list = sources.split("\n")
    for source in source_list:
        st.write(source)
    