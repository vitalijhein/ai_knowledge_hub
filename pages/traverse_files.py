import streamlit as st
import os
import sys
import openai

from datetime import datetime
sys.path.append('C:\\Users\\vital\\streamlit_suite\\src')
from my_utils.my_utils import MyKnowledgeBaseBuilder
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key = os.environ['OPENAI_API_KEY']
my_Knowledgebase_builder = MyKnowledgeBaseBuilder()

sys.path.append('C:\\Users\\vital\\streamlit_suite\\src')
from my_utils.my_utils import MyKnowledgeBaseBuilder
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
my_Knowledgebase_builder = MyKnowledgeBaseBuilder()
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.readers.file import FlatReader
from pathlib import Path
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.retrievers import VectorIndexAutoRetriever
import streamlit as st

# Base path to remove from folder display
BASE_PATH = "C:\\Users\\vital\\iCloudDrive\\iCloud~md~obsidian\\new_vault\\"
SAVE_PATH = "C:\\Users\\vital\\iCloudDrive\\iCloud~md~obsidian\\new_vault\\06 Unprocessed AI"

if 'messages' not in st.session_state:
    st.session_state['messages'] = []  # Initialize with an empty list if not present

# Function to find Markdown files and their folders
def find_md_files_and_folders(directory):
    md_files = []
    folders = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append((file, os.path.join(root, file)))
                display_folder = root.replace(BASE_PATH, "")
                folders.add(display_folder)
    return md_files, list(folders)

@st.cache_data()
def generate_next_steps(file_content):
    # Placeholder for your recommendation logic
    st.write("Generating next steps based on the selected file...")

    sys_prompt = """
Analyze the provided input text and suggest innovative approaches or additional lines of inquiry based on its content. Please identify key themes, concepts, or arguments within the text and provide at least three unique ideas for further exploration related to these aspects.
"""

    user_prompt = f"""
    Input: {file_content}
    Output:
"""

    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", "{sys_prompt_template}"),
            ("human", "{user_prompt_template}")
        ]
    )
    
    model = ChatOpenAI(
        model="gpt-4-1106-preview",
        temperature=0,
        model_kwargs= {
            "seed": 123,
            "top_p": 1
        }
    )
    output_parser = StrOutputParser()

    chain = chat_template | model | output_parser
    output = chain.invoke({"sys_prompt_template": sys_prompt ,"user_prompt_template": user_prompt})

    return output


def chat_with_knowledge(file_content):
    # Your chat functionality goes here
    # This is a placeholder for the chat code you've provided
    st.header("Chat with the Knowledge Base 💬 📚")

    # Initialize chat message history if not already present
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Ask me a question about my knowledge base! 😊"}]
    
    parser = MarkdownNodeParser()
    md_docs = FlatReader().load_data(Path("C:\\Users\\vital\\streamlit_suite\\src\\zero-to-1-million-as-a-one-person-business-while-working-2-4-hours-per-day.md"))
    md_docs = FlatReader().load_data(Path("C:\\Users\\vital\\streamlit_suite\\src\\You Are Obligated to Get Rich in Your 20s.md"))

    nodes = parser.get_nodes_from_documents(md_docs)
    index, query_engine = my_Knowledgebase_builder.create_vectorstore_from_node_return_query_engine(similarity_cutoff=0.5)
    #response = query_engine.query("How can one build a business quickly?")
    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

    if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
    else: 
        prompt = file_content
        st.session_state.messages.append({"role": "user", "content": file_content})


    if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":        
        message = st.session_state.messages[-1]
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message) # Add response to message history

def save_to_unprocessed(output, markdown_files, selected_file):
    current_time = datetime.now().strftime('%d-%m-%Y')

    output_final = f"""---
tags:
- Recommendation
---
{current_time}

Status: #idea
Tags:   


{output}


---
# References
    """

    selected_file = selected_file.replace(".md", "")
    filename = f'{selected_file} recommendation.md'
    SAVE_PATH_File = f'{SAVE_PATH}\\{filename}'
    with open(SAVE_PATH_File, 'w') as file:
        file.write(output_final)

# Streamlit app
def main():
    st.title('Inspiration for Further Research')

    # User input for directory path
    directory = BASE_PATH
    if directory:
        markdown_files, folders = find_md_files_and_folders(directory)
        if markdown_files:
            # Let the user select a folder
            selected_display_folder = st.selectbox('Select a folder:', folders)
            # Convert back to the actual path for filtering
            selected_folder = os.path.join(BASE_PATH, selected_display_folder)
            # Filter markdown files by the selected folder
            filtered_files = [(file_name, file_path) for file_name, file_path in markdown_files if file_path.startswith(selected_folder)]
            file_content = ""

            if filtered_files:
                file_names = [file_name for file_name, _ in filtered_files]
                selected_file = st.selectbox('Select a Markdown file:', file_names)
                for file_name, file_path in filtered_files:
                    if file_name == selected_file:
                        display_path = file_path.replace(BASE_PATH, "")
                        st.write(f'**File Name:** {file_name}, **Path:** {display_path}')
                        with open(file_path, 'r', encoding='utf-8') as file:
                            file_content = file.read()
                            st.text_area("File Content", file_content, height=300)
                            break
                # Add a button for "Chat With Knowledge"
                if st.button('Chat With Knowledge'):
                    chat_with_knowledge(file_content)  # Call the function to handle chat  
                                      
                if st.button('Get Recommendation'):
                    output = generate_next_steps(file_content)
                    st.session_state['last_recommendation'] = output
                    st.write(st.session_state['last_recommendation'])

                if st.button("Save Recommendation"):
                    save_to_unprocessed(st.session_state['last_recommendation'], markdown_files, selected_file)

            else:
                st.write(f'No Markdown files found in {selected_display_folder}.')
        else:
            st.write('No Markdown files found in the specified directory.')
    else:
        st.write('Please enter a valid directory path.')

if __name__ == "__main__":
    main()
