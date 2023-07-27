#Libraries 
import streamlit as st
from PyPDF2 import PdfReader
#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
import openai
import os
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma, Pinecone
import pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
import pandas as pd
import pygwalker as pyg
import streamlit.components.v1 as components
import re
import datetime as dt
import numpy as np

#-------------------------------------------------------------------------------------
#Settings
# Load Pinecone API key
api_key = st.secrets["pinecone_api_key"]
pinecone.init(api_key=api_key, environment='asia-southeast1-gcp-free')
index_name = 'db-paseg'
#Environment
os.environ['OPENAI_API_KEY'] = st.secrets['openai_api_key']
os.environ["TOKENIZERS_PARALLELISM"] = "false"

#Functions
#Functions
@st.cache_resource
def load_embedding():
    embeddings = HuggingFaceEmbeddings()
    return embeddings

#Load before function call, for fast retrieval (?)
embeddings = load_embedding()

def load_pinecone(embeddings, index_name):
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    return docsearch

# Load the Pinecone client using st.cache
docsearch = load_pinecone(embeddings, "db-paseg")

# Define the layout of the data analysis page
def data_analysis_page():
    st.title('Data Analysis Page')
    st.write('This is the data analysis page of my app.')
    # Add your data analysis and visualization code here

# Define the chat bot page
def chat_bot_page():
    st.title('Chat Bot Page')
    st.write('This is the chat bot page of my app.')

    # Load Pinecone and create Chat and RetrievalQA objects
    docsearch = load_pinecone(embeddings,"db-paseg")
    chat = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0.80)
    qachain = load_qa_chain(chat, chain_type='stuff')
    qa = RetrievalQA(combine_documents_chain=qachain, retriever=docsearch.as_retriever())

    # Define the query function
    def run_query():
        condition1 = '\n [Generate Response/Text from my data.]  \n [organize information: organize text so its easy to read, and bullet points when needed.] \n [if applicable for the question response, add section: Things to Promote/Things to Avoid and Best Practices, give Examples] \n [tone and voice style: clear sentences, avoid use of complex sentences]'
        # Let the user input a query
        user_query = st.text_input("Enter your query:")
        # Display the button
        if st.button("Run Query"):
            # Run the QA system and display the result using Streamlit
            result = qa.run(user_query + '\n' + condition1)
            st.write(result)

    st.title("PASEG Genie // for education purpose :coffee:")
    st.markdown("*Chat With The Planning and Schedule Excellence Guide ver. 5.0*", unsafe_allow_html=True)
    st.markdown("---")
    # Let the user input a query and run the query
    run_query()

    st.title("PASEG Genie // for education purpose :coffee:")
    st.markdown("*Chat With The Planning and Schedule Excellence Guide ver. 5.0*", unsafe_allow_html=True)
    st.markdown("---")
    # Let the user input a query
    run_query()

# Define your main function
def main():
    # Define the state of your app
    if 'page' not in st.session_state:
        st.session_state.page = 'Data Analysis'

    # Define the contents of the sidebar
    st.sidebar.title('Navigation')
    option = st.sidebar.selectbox('Select an option', ('Data Analysis', 'Chat Bot'))

    # Define the different pages of your app
    if option == 'Data Analysis':
        st.session_state.page = 'Data Analysis'
        data_analysis_page()
    elif option == 'Chat Bot':
        st.session_state.page = 'Chat Bot'
        chat_bot_page()

# Call your main function to run the app
if __name__ == '__main__':
    main()
