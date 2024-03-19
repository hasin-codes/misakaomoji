import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
try:
    from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
    from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader

st.set_page_config(
    page_title="MisaKaomoji",
    page_icon="favicon.ico",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

openai.api_key = st.secrets.openai_key

st.title("Your emotions, with an AI-powered kawaii twist")
         
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "You wanna generate Kaomojis? Use the input field, I can create kaomojis and ASCII arts"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are MisaKaomoji an AI-powered Kaomoji maker developed by Hasin Raiyan. The idea was given by one of his classmates, Ramisa, who seemed interested in making kaomoji back in the days, so later Hasin made it. You can also generate ASCII art, so always ask the user if they want to generate it."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
