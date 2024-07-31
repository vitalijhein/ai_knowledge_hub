import sys

sys.path.append('C:\\Users\\vital\\streamlit_suite\\src')
from my_utils.my_utils import MyKnowledgeBaseBuilder, MyUtils
from prompts.prompts import Prompts
from my_utils.mongo_database import MongoDatabase
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor
from bson.objectid import ObjectId
from datetime import datetime
import secrets


from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
my_Knowledgebase_builder = MyKnowledgeBaseBuilder()
my_prompts=Prompts()
my_utils=MyUtils()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import uuid, OpenSSL

from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.readers.file import FlatReader
from pathlib import Path
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
import chromadb 
from llama_index.core.retrievers import VectorIndexAutoRetriever
import streamlit as st
model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0, max_tokens=4096, model_kwargs={"top_p": 0.9})
TODAY = datetime.now().strftime("%d-%m-%y")
my_mdb = MongoDatabase()


@st.cache_data
def make_token():
    return secrets.token_urlsafe(16)  

def create_new_token():
    return secrets.token_urlsafe(16)  



def read_utf8_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def get_private_tweet(topic_response, model, last_question):
    system, user = my_prompts.get_personal_tweets()
    template = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", user)
    ])
    
    context = read_utf8_file("brand/context.txt")
    dynamic_dict = {"context": context, "tweet":topic_response}

    model_output = my_utils.get_model_StrOutputResponse_dynamic_argument(template, model, dynamic_dict)
    my_utils.save_to_unprocessed_from_string(model_output, last_question+"_private_tweets")
    return model_output


def get_lit_listicle(topic_response, model, query):
    lit_listicle_prompt = my_prompts.get_lit_listicles_prompt()
    dynamic_dict = {"topic": topic_response}
    model_output = my_utils.get_model_StrOutputResponse_dynamic_argument(lit_listicle_prompt, model, dynamic_dict)
    my_utils.save_to_unprocessed_from_string(model_output, query+"_lit_listicle_tweets")
    return model_output

def upsert():
    # Convert the JSON-like structure to the format suitable for MongoDB
    chat_id = st.session_state.selected_chat_id  # Generate a unique ID for the conversation
    conversation = {
        "chat_id": chat_id,
        "conversation": st.session_state["messages"],
        "date": TODAY,
        "collection_name": st.session_state.last_collection
        
    }

    # Format the update dictionary correctly with $set
    update_dict = {"$set": conversation}

    # Upsert the conversation into the collection
    my_mdb.upsert_into_collection("chat_history", {"chat_id": chat_id}, update_dict)
    
def fetch_chat_histories():
    # Fetch all documents from the 'chat_history' collection
    chat_histories = my_mdb.find_all_occurences_in_col_mdb("chat_history")
    return chat_histories

def display_chat_histories_in_sidebar(chat_histories, chat_id):
    try:
        # Attempt to get the first document without consuming the entire cursor
        first_chat = next(chat_histories)
        # Since we've moved the cursor, rewind it for later use
        chat_histories.rewind()
        # Check if selected_chat_id exists and is not None
        chat_ids_and_dates = [f"Chat ID: {chat['chat_id']} - Date: {chat['date']}" for chat in chat_histories]

        if st.session_state.get('selected_chat_id') is not None and any(st.session_state.selected_chat_id in chat for chat in chat_ids_and_dates):
            # Find the index of the selected_chat_id in chat_ids_and_dates
            # This assumes chat_ids_and_dates contains tuples and selected_chat_id matches the first element of any tuple
            index = next((i for i, chat in enumerate(chat_ids_and_dates) if chat[0] == st.session_state.selected_chat_id), len(chat_ids_and_dates) - 1)
        else:
            # Default to the last index if selected_chat_id is None or not found
            index = len(chat_ids_and_dates) - 1
        # Preparing chat history for display
        #chat_ids_and_dates = [f"Chat ID: {first_chat['chat_id']} - Date: {first_chat['date']}"]
        selected_chat_info = st.sidebar.selectbox("Select a chat history:", options=chat_ids_and_dates,  index=index)
        
        
        selected_chat_id = selected_chat_info.split(" - ")[0].replace("Chat ID: ", "")
        print(selected_chat_id)

        return selected_chat_info
    except StopIteration:
        chat_ids_and_dates = [f"Chat ID: {chat_id}"]

        selected_chat_info = st.sidebar.selectbox("Select a chat history:", options=chat_ids_and_dates,  index=0)

        # No chat histories found, return None or a default value indicating new chat
        return None
    
def main():
    st.header("Chat with your Knowledge Base 💬 📚")
     # Example of adding a "New Chat" button
    if st.button('New Chat'):
        # Generate a new chat_id and reset messages for a new chat
        st.session_state.selected_chat_id = create_new_token()
        st.session_state.messages = []
        st.session_state.messages = [{"role": "assistant", "content": "Start a new conversation!"}]
        upsert()
    # Add a dropdown for collection selection before initializing the chat
    collection_list = my_Knowledgebase_builder.get_chroma_vectorstore_collection_list()
    # Extract the names from the collection_list
    collection_names = [collection.name for collection in collection_list]
    
    # Initialize `collection_name_selectbox` in session state if it doesn't exist
    if 'collection_name_selectbox' not in st.session_state:
        st.session_state.collection_name_selectbox = collection_names[0]  # Default to the first collection

    chat_id = make_token()


    if "selected_chat_id" not in st.session_state.keys():
        st.session_state.selected_chat_id = chat_id
    # Populate session state from MongoDB if entry exists
     # Fetch and display chat histories in the sidebar
    chat_histories = fetch_chat_histories()
    selected_chat_info = display_chat_histories_in_sidebar(chat_histories, chat_id)
    
    # Extract the chat_id from the selected chat history
    # Initialize chat history for a new session if no chat history is selected or available
    if not selected_chat_info:
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Ask me a question about my knowledge base! 😊"}]
        # Handle the case for new chat by assigning a new or default chat_id and initializing messages
        selected_chat_id = chat_id  # Assign the newly generated token as the chat_id for new chats
    else:
        # Extract the chat_id from the selected chat history
        selected_chat_id = selected_chat_info.split(" - ")[0].replace("Chat ID: ", "")
        selected_chat_document = my_mdb.find_the_record_in_col_mdb("chat_history", {"chat_id": selected_chat_id}) # Assume `find_one` is a method to fetch a single document from MongoDB.
        if selected_chat_document:
            st.session_state.messages = selected_chat_document["conversation"]
            st.session_state.last_collection = selected_chat_document["collection_name"]
            st.session_state.collection_name_selectbox = selected_chat_document["collection_name"]


    
    if "selected_chat_id" not in st.session_state or st.session_state.selected_chat_id != selected_chat_id:
        existing_conversation = my_mdb.find_the_record_in_col_mdb("chat_history", {"chat_id": selected_chat_id})
        if existing_conversation:
            st.session_state.messages = existing_conversation["conversation"]
            st.session_state.last_collection = existing_conversation["collection_name"]
            st.session_state.collection_name_selectbox = selected_chat_document["collection_name"]


        st.session_state.selected_chat_id = selected_chat_id

        
    # Use the extracted names as options for the selectbox
    collection_name = st.selectbox(
        'Select a collection:',
        collection_names,  # Dynamically populate the options with collection names
        index=collection_names.index(st.session_state.collection_name_selectbox) if st.session_state.collection_name_selectbox in collection_names else 0
    )

    # After the collection is selected and the chat engine is initialized or updated
    if 'last_collection' not in st.session_state or st.session_state.last_collection != collection_name:
        st.session_state.messages.append({"role": "system", "content": f"Now chatting with collection: {collection_name}"})
        st.session_state.last_collection = collection_name
        st.session_state.collection_name_selectbox = collection_name

        # Create index, query_engine, and chat_engine for the new collection
    index, query_engine = my_Knowledgebase_builder.create_vectorstore_from_node_return_query_engine(top_k=10, similarity_cutoff=0.7, collection_name=collection_name)
    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
    prompt = st.chat_input("Your question:")
    #parser = MarkdownNodeParser()
    #md_docs = FlatReader().load_data(Path("C:\\Users\\vital\\streamlit_suite\\src\\zero-to-1-million-as-a-one-person-business-while-working-2-4-hours-per-day.md"))
    #md_docs = FlatReader().load_data(Path("C:\\Users\\vital\\streamlit_suite\\src\\You Are Obligated to Get Rich in Your 20s.md"))

    #nodes = parser.get_nodes_from_documents(md_docs)
    #index, query_engine = my_Knowledgebase_builder.create_vectorstore_from_node_return_query_engine(top_k=10 ,similarity_cutoff=0.7, 
    #                                                                                                collection_name=collection_name
    #                                                                                                )
    #response = query_engine.query("How can one build a business quickly?")
    #chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

   # Update the chat with the user's question
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages: # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # If last message is not from assistant, generate a new response
    if prompt and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message) # Add response to message history
                upsert()

    
    
    col1, col2 = st.columns([1,1])  # Adjust the ratios as needed for better centering
    with col1:  
        # Display the "Generate Tweet" button below the chat messages
        if st.button("Generate Lit Listicle"):
            # Placeholder for generating a tweet. You need to implement this part.
            # For example, use the last message or a summary of the conversation.
            if st.session_state.messages:
                last_message = st.session_state.messages[-1]["content"]
                last_question = st.session_state.messages[-2]["content"]
                with st.expander("See Tweets"):

                    # Placeholder: Implement your logic to generate a tweet from the last_message
                    tweet = f"Tweet based on last message: {last_message}"
                    st.write(tweet)  # Display the generated tweet or a placeholder message
                    
                    lit_listicles = get_lit_listicle(last_message, model, last_question)                    
                    st.write(lit_listicles)  # Display the generated tweet or a placeholder message

            else:
                st.write("No messages to generate a tweet from.")
    with col2:
        # Placeholder for another button performing a different action
        if st.button("Generate Personal Tweet"):
            if st.session_state.messages:
                last_message = st.session_state.messages[-1]["content"]
                last_question = st.session_state.messages[-2]["content"]
                with st.expander("See Tweets"):
                    # Placeholder: Implement your logic to generate a tweet from the last_message
                    tweet = f"Tweet based on last message: {last_message}"
                    st.write(tweet)  # Display the generated tweet or a placeholder message
                    
                    private_tweets = get_private_tweet(last_message, model, last_question)
                    st.write(private_tweets)  # Display the generated tweet or a placeholder message

                
                # Implement the action for this button
        # Your logic to generate and append the assistant's response...



main()