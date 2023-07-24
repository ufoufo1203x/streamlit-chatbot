import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage
from langchain.schema import AIMessage

from dotenv import load_dotenv
#Read environmental variables
load_dotenv()

# Make instance ver ChatGPT-3.5
chat = ChatOpenAI(model_name="gpt-3.5-turbo")

#Get chat history
try:
    memory = st.session_state["memory"]
except:
    memory = ConversationBufferMemory(return_message=True)

# Make instance for chain
chain = ConversationChain(
    llm=chat,
    memory=memory,
)

# Make UI with Streamlit
st.title("Chatbot in Streamlit")

# Make UI and form
text_input = st.text_input("Enter your message")
send_button = st.button("Send")

# Chat history
history = []

# OpenAI API setting
if send_button:
    send_button = False
    
    #ChatGpt processing
    chain(text_input)
    
    #Save history
    st.session_state["memory"] = memory
    
    # Read Chat history
    try:
        history = memory.load_memory_variables({})["history"]
    except Exception as e:
        st.error(e)
        
# Output chat history
for index, chat_message in enumerate(reversed(history)):
    if type(chat_message) == HumanMessage:
        message(chat_message.content, is_user=True, key=2 * index)
    elif type(chat_message) == AIMessage:
        message(chat_message.content, is_user=False, key=2 * index + 1)
        
