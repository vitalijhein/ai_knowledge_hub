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
model = ChatOpenAI(model="gpt-4-0125-preview")

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

#@st.cache_data()
def get_summary_from_transcript(transcript):
    prompt1 = my_prompts.get_framework_from_article()
    prompt2= my_prompts.get_article_summary_prompt()
    

    chain = prompt1 | model | StrOutputParser()
    output1 = my_utils.get_model_StrOutputResponse_single_argument(prompt1, model, "article", transcript)
    output2 = my_utils.get_model_StrOutputResponse_single_argument(prompt2, model, "article", transcript)
    output3 = output1+"\n"+output2
    return output3


def main():
    st.title('Video Summary Generator')
    
    # Initialize session state variables if they don't already exist
    if 'summary' not in st.session_state:
        st.session_state['summary'] = ""
    if 'video_title' not in st.session_state:
        st.session_state['video_title'] = ""
    
    # Initialize the session state for showing the button
    if 'show_next_button' not in st.session_state:
        st.session_state.show_next_button = False
        
    # Text input for the user to enter the YouTube Video URL
    video_url = st.text_input('Enter the YouTube Video URL', '')

    # Button to trigger the processing
    if st.button('Generate Summary'):
        if video_url:
            # Processing the video URL
            try:
                transcript = my_utils.get_transcript(video_url)
                _, st.session_state['video_title'] = my_utils.get_yt_video_info(video_url)
                st.session_state['summary'] = get_summary_from_transcript(transcript)
                
                # Displaying the results
                st.subheader('Video Title')
                st.write(st.session_state['video_title'])
                
                st.subheader('Summary')
                st.write(st.session_state['summary'])
                
                # Optionally save the summary with the video title
                st.session_state['video_title'] = my_utils.save_to_unprocessed_from_string(st.session_state['summary'], st.session_state['video_title'])
                
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
            try:
                parser = MarkdownNodeParser()
                st.write(st.session_state['video_title'])
                file_path = my_utils.get_SAVE_PATH() + "\\" + st.session_state['video_title'] + ".md"
                md_docs = FlatReader().load_data(Path(file_path))

                nodes = parser.get_nodes_from_documents(md_docs)
                my_knowledgebase_builder.create_vectorstore_from_node_return_query_engine(nodes, similarity_cutoff=0.7)
                
                st.write("Successfully sent to vector store!")
            except Exception as e:
                st.error(f'An error occurred: {e}')

if __name__ == '__main__':
    main()



def main2():
    st.title('Video Summary Generator')
    
    summary = ""
    video_title = ""    
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
                _, video_title = my_utils.get_yt_video_info(video_url)
                summary = get_summary_from_transcript(transcript)
                
                # Displaying the results
                st.subheader('Video Title')
                st.write(video_title)
                
                st.subheader('Summary')
                st.write(summary)
                
                # Optionally save the summary with the video title
                my_utils.save_to_unprocessed_from_string(summary, video_title)
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
            st.write(video_title)
            #file_path = my_utils.get_SAVE_PATH() + "\\" + video_title + ".md"
            #md_docs = FlatReader().load_data(Path(file_path))

            #nodes = parser.get_nodes_from_documents(md_docs)
            #my_knowledgebase_builder.create_vectorstore_from_node_return_query_engine(nodes, similarity_cutoff=0.5)
            #except Exception as e:
            #    st.error(f'An error occurred: {e}')
