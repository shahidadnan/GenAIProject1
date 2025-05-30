import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Set LangChain tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "")

# Imports that might crash
try:
    from langchain_ollama.llms import OllamaLLM
    #from langchain_community.llms import ollama
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except Exception as e:
    st.error(f"LangChain import failed: {e}")

# Streamlit UI
st.title("Demo AI")

input_text = st.text_input("What question do you have in mind?")

# LangChain logic
try:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Please respond to the question asked."),
        ("user", "Question: {question}")
    ])
    llm = OllamaLLM(model="gemma3:1b")
    output_parser = StrOutputParser()
    chain = prompt | llm 
    
except Exception as e:
    st.error(f"Failed to create LangChain chain: {e}")


# Output
placeholder = st.empty()  # Creates a placeholder

if input_text:
    placeholder.write("🧠 Thinking...")  # Show thinking message
    try:
        response = chain.invoke({"question": input_text})
        placeholder.empty()  # Remove the thinking message
        st.write("📝 Response:")
        st.write(response)
    except Exception as e:
        placeholder.empty()
        st.error(f"Failed to generate response: {e}")