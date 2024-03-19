import openai
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(
    page_title="MisaKaomoji 🎂",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("MisaKaoMoji")
st.text("Your emotions, with an AI-powered kawaii twist")

# Set up OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize messages if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize openai_model if not present
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input and generate response
if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Instruction message for Misakaomoji
    instruction_message = (
        "Welcome to MisaKaomoji! I'm Misakaomoji, your kawaii kaomoji creator. "
        "Please express your emotions, and I'll generate adorable kaomoji for you."
    )
    st.session_state.messages.append({"role": "assistant", "content": instruction_message})
    with st.chat_message("assistant"):
        st.markdown(instruction_message)

    # Generate responses using OpenAI's Chat Completion API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
