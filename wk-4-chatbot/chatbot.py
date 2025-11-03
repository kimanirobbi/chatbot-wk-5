import streamlit as st  
from transformers import pipeline

st.set_page_config(page_title="robbi - chatbot, layout="wide")

st.title("robbi - Your AI Chatbot")
st.write("Welcome to robbi, your AI-powered chatbot. Ask me anything!")

def load_text_generator():
    return pipeline("text-generation", model="gpt2")
    text_generator = load_text_generator()
    text_generator . tokenizer.pad_token = text_generator .model.config.eos_token
    return text_generator
text_generator = load_text_generator()
if "conversation" not in st.session_state:
    st.session_state.conversation = []
def generate_response(user_input):
    st.session_state.conversation.append({"role": "user", "content": user_input})
    conversation_history = " ".join(
        [f"{msg['role']}: {msg['content']}" for msg in st.session_state.conversation]
    )

    system_instruction = (
        "Generate code based on the conversation history."
        " Provide clear and concise responses."
        " Use markdown formatting for code snippets."
    )       

    #build the canvo prompt
    def build_coversation_prompt(system_instruction, conversation_history, user_input):
    formated_message = []

    for previous_message in st.session_state.conversation:
        prompt = f"{system_instruction}\n\n{conversation_history}\nAI
: "
        formated_message.append(prompt)
    formated_message.append(f"User: {user_input}\nAI: ")
    return "\n".join(formated_message)
     
     #sidebar for configuration
    with st.sidebar:
        st.title("Configeration")
        max_new_tokens = st.slider("Max New Tokens", min_value=50, max_value=500, value=150, step=50)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        top_p = st.slider("Top-p (nucleus sampling)", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
        st.write("Adjust the parameters to control the response generation.")
        if st.button("Clear Conversation"):
            st.session_state.conversation = ["start new conversation"]
        for msg in st.session_state.conversation:
            st.write(f"**{msg['role'].capitalize()}:** {msg['content']}")
    prompt = build_coversation_prompt(system_instruction, conversation_history, user_input)
    response = text_generator(

    # display conversation
    for user_input, ai_reply in st.session_state.conversation:
        st.write(f"**User:** {user_input}")
        st.write(f"**AI:** {ai_reply}") 

    #user input form
    user_input = st.text_input("You:", "")
    if st.button("Send"):
        if user_input:
        st.conversation.append(
            {"role": "ai", "content": response[0]['generated_text']}    
        )
        return response[0]['generated_text']
        generate_response(user_input)
         max_new_tokens=max_new_tokens,
         temperature=temperature,
         top_p=top_p,
         pad_token_id=text_generator.tokenizer.eos_token_id,
         return_full_text=False,
        )
        with st.spinner("Generating response...")
         text_generator = text_generator(
            prompt = build_coversation_prompt(
                system_instruction, conversation_history, user_input
            ),
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            pad_token_id=text_generator.tokenizer.eos_token_id,
            return_full_text=False,
        )

        # extracting the model answer from generated text
        if "assistant" in genration.text:
            answer = generation.text.split("assistant:")[-1].strip()
        else:
            answer = generation.text.strip()

        # displaying and storing the answer
        st.session_state.conversation.append({"role": "ai", "content": answer})
        return answer
        st.session_state.conversation.append(
            {"role": "ai", "content": response[0]['generated_text']}    
        )
        