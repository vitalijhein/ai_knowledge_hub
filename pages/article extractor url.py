from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
import importlib
from langchain_community.chat_models import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema.output_parser import StrOutputParser
from typing import List
from llama_index.readers.file import FlatReader
from pathlib import Path
from llama_index.readers.web import SimpleWebPageReader

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
import sys
sys.path.append('C:\\Users\\vital\\streamlit_suite\\src')
import my_utils.my_utils  # Adjust based on your actual import path
importlib.reload(my_utils.my_utils)
from my_utils.my_utils import MyUtils, MyKnowledgeBaseBuilder
from prompts.prompts import Prompts
from llama_index.core import Document

from llama_index.core.node_parser import MarkdownNodeParser

from youtube_transcript_api.formatters import TextFormatter
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict
import os 

video_url = 'https://www.youtube.com/watch?v=yykGW30zgyE'
#model = ChatOpenAI(model="gpt-4-0125-preview")
model = ChatOpenAI(model="gpt-3.5-turbo")

my_utils = MyUtils()
my_prompts = Prompts()
my_knowledgebase_builder = MyKnowledgeBaseBuilder()


class Questions(BaseModel):
    questions: Dict[str, str] = Field(
        ..., 
        description="Dynamic dictionary to store an arbitrary number of questions."
    )



    
def get_questions_from_transcript(transcript):
    parser = JsonOutputParser(pydantic_object=Questions)
    prompt1 = my_prompts.get_questions_from_transcript_as_dict()

    chain = prompt1 | model | parser

    model_output_questions_dict = chain.invoke({"transcript": transcript})
    
    return model_output_questions_dict
    

def process_questions(transcript, output):
    outputs_list = []
    for question_number, question_text in output['questions'].items():
        print(f"{question_text}")
        prompt2 = my_prompts.process_questions_from_transcript()
        chain2 = prompt2 | model | StrOutputParser()
        output2 = chain2.invoke({"transcript": transcript, "question": question_text})
        # Save question and output as a pair in outputs_list
        outputs_list.append((question_text, output2))
    return outputs_list

from urllib.parse import urlparse

def extract_last_part_of_url(url):
    parsed_url = urlparse(url)
    # Split the path component of the URL by '/' and filter out empty strings
    path_parts = [part for part in parsed_url.path.split('/') if part]
    # Get the last part of the path
    last_part = path_parts[-1] if path_parts else None
    return last_part



#@st.cache_data()
def get_summary_from_transcript(article):
    prompt1 = my_prompts.get_framework_from_article()
    prompt2= my_prompts.get_article_summary_prompt()
    

    chain = prompt1 | model | StrOutputParser()
    output1 = my_utils.get_model_StrOutputResponse_single_argument(prompt1, model, "article", article)
    output2 = my_utils.get_model_StrOutputResponse_single_argument(prompt2, model, "article", article)
    output3 = output1+"\n"+output2
    return output3

    url = "https://thedankoe.com/letters/you-are-obligated-to-get-rich-in-your-20s/"
    #response = requests.get(url)
    #html = response.text
    #pattern = re.compile('<.*?>')
    #article = re.sub(pattern, '', html)




def main():
    st.title('Video Summary Generator')
    
    # Initialize session state variables if they don't already exist
    if 'summary' not in st.session_state:
        st.session_state['summary'] = ""
    if 'article_title' not in st.session_state:
        st.session_state['article_title'] = ""
    
    # Initialize the session state for showing the button
    if 'show_next_button' not in st.session_state:
        st.session_state.show_next_button = False
        
    # Text input for the user to enter the YouTube Video URL
    article_url = st.text_input('Enter the Article URL', '')

    # Button to trigger the processing
    if st.button('Generate Summary'):
        if article_url:
            # Processing the video URL
            try:
                #transcript = my_utils.get_transcript(video_url)
                documents = SimpleWebPageReader(html_to_text=True).load_data(
                    #["https://thedankoe.com/letters/zero-to-1-million-as-a-one-person-business-while-working-2-4-hours-per-day/"]
                [article_url]
                )
                
                st.session_state['article_title'] = extract_last_part_of_url(article_url)
                print(st.session_state['article_title'])
                article = documents[0].get_content()
                #_, st.session_state['article_title'] = my_utils.get_yt_video_info(video_url)
                st.session_state['summary'] = get_summary_from_transcript(article)
                
                # Displaying the results
                st.subheader('Article Title')
                st.write(st.session_state['article_title'])
                
                st.subheader('Summary')
                st.write(st.session_state['summary'])
                
                # Optionally save the summary with the video title
                st.session_state['article_title'] = my_utils.save_to_unprocessed_from_string(st.session_state['summary'], st.session_state['article_title'])
                
                # After successful execution, set the flag to show the next button
                st.session_state.show_next_button = True
            except Exception as e:
                st.error(f'An error occurred: {e}')
                st.session_state.show_next_button = False  # Ensure button is not shown on error
        else:
            st.warning('Please enter Article URL to proceed.')
            st.session_state.show_next_button = False  # Ensure button is not shown on error

    # Conditionally show the next button based on the session state
    if st.session_state.show_next_button:
        collections_list = my_knowledgebase_builder.get_chroma_vectorstore_collection_list()
        options = [collection.name for collection in collections_list]

        options.append("NEW COLLECTION")
        value = st.selectbox("Select a chat history:", options=options)

        if st.button('Send to vector store?'):
            if value == "NEW COLLECTION":
                value = st.text_input()
            try:
                parser = MarkdownNodeParser()
                st.write(st.session_state['article_title'])
                file_path = my_utils.get_SAVE_PATH() + "\\" + st.session_state['article_title'] + ".md"
                md_docs = FlatReader().load_data(Path(file_path))

                nodes = parser.get_nodes_from_documents(md_docs)
                my_knowledgebase_builder.create_vectorstore_from_node_return_query_engine(nodes, similarity_cutoff=0.7, collection_name=value)
                
                st.write("Successfully sent to vector store!")
            except Exception as e:
                st.error(f'An error occurred: {e}')

if __name__ == '__main__':
    main()



def main2():
    st.title('Article Summary Generator')
    
    summary = ""
    article_title = ""    
    # Initialize the session state for showing the button
    if 'show_next_button' not in st.session_state:
        st.session_state.show_next_button = False
    # Text input for the user to enter the video URL
    video_url = st.text_input('Enter the YouTube Video URL', '')

    # Button to trigger the processing
    if st.button('Generate Summary'):
        if video_url:
            # Processing the video URL
            try:
                transcript = my_utils.get_transcript(video_url)
                _, article_title = my_utils.get_yt_video_info(video_url)
                summary = get_summary_from_transcript(transcript)
                
                # Displaying the results
                st.subheader('Article Title')
                st.write(article_title)
                
                st.subheader('Summary')
                st.write(summary)
                
                # Optionally save the summary with the video title
                my_utils.save_to_unprocessed_from_string(summary, article_title)
                # After successful execution, set the flag to show the next button
                st.session_state.show_next_button = True
            except Exception as e:
                st.error(f'An error occurred: {e}')
                st.session_state.show_next_button = False  # Ensure button is not shown on error

        else:
            st.warning('Please enter a YouTube video URL to proceed.')
            st.session_state.show_next_button = False  # Ensure button is not shown on error

    # Conditionally show the next button based on the session state
    if st.session_state.show_next_button:

        if st.button('Send to vector store?'):
            #try:
            parser = MarkdownNodeParser()
            st.write(summary)
            st.write(article_title)
            file_path = my_utils.get_SAVE_PATH() + "\\" + article_title + ".md"
            md_docs = FlatReader().load_data(Path(file_path))

            nodes = parser.get_nodes_from_documents(md_docs)
            my_knowledgebase_builder.create_vectorstore_from_node_return_query_engine(nodes, similarity_cutoff=0.5, collection_name="linkedin_ai_content")
            #except Exception as e:
            #    st.error(f'An error occurred: {e}')
