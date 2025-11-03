import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="robbi - chatbot", layout="wide")

st.title("robbi - Your AI Chatbot")
st.write("Welcome to robbi, your AI-powered chatbot. Ask me anything!")


@st.cache_resource
def load_text_generator():
    gen = pipeline("text-generation", model="gpt2")
    # ensure tokenizer has a pad token
    tokenizer = getattr(gen, "tokenizer", None)
    model = getattr(gen, "model", None)
    if tokenizer is not None:
        if getattr(tokenizer, "pad_token", None) is None:
            # try to fall back to model config eos_token if available
            eos = None
            if model is not None:
                config = getattr(model, "config", None)
                if config is not None:
                    eos = getattr(config, "eos_token", None)
            if eos is not None:
                tokenizer.pad_token = eos
    return gen


text_generator = load_text_generator()

if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Sidebar configuration
with st.sidebar:
    st.title("Configuration")
    max_new_tokens = st.slider("Max New Tokens", min_value=50, max_value=500, value=150, step=50)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    top_p = st.slider("Top-p (nucleus sampling)", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
    st.write("Adjust the parameters to control the response generation.")
    if st.button("Clear Conversation"):
        st.session_state.conversation = []


from chatbot_utils import build_conversation_prompt


def generate_response(user_input, max_new_tokens, temperature, top_p):
    # store user message
    st.session_state.conversation.append({"role": "user", "content": user_input})

    conversation_history = " ".join([f"{m['role']}: {m['content']}" for m in st.session_state.conversation])

    system_instruction = (
        "You are a helpful assistant. Provide concise, clear answers."
        " When returning code, format it as a markdown code block."
    )

    prompt = build_conversation_prompt(system_instruction, conversation_history, user_input)

    try:
        # safely obtain a pad_token_id from the tokenizer if present
        _tokenizer = getattr(text_generator, "tokenizer", None)
        pad_id = None
        if _tokenizer is not None:
            pad_id = getattr(_tokenizer, "eos_token_id", None)
            if pad_id is None:
                pad_id = getattr(_tokenizer, "pad_token_id", None)

        output = text_generator(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            pad_token_id=pad_id,
            return_full_text=False,
        )
        generated = output[0].get("generated_text", "").strip()
    except Exception as e:
        generated = f"Error generating response: {e}"

    st.session_state.conversation.append({"role": "ai", "content": generated})
    return generated


# Display existing conversation
for msg in st.session_state.conversation:
    role = msg["role"].capitalize()
    st.write(f"**{role}:** {msg['content']}")


# User input form
user_input = st.text_input("You:", "")
if st.button("Send") and user_input:
    answer = generate_response(user_input, max_new_tokens, temperature, top_p)
    st.write(f"**AI:** {answer}")
    
