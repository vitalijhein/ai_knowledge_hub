from youtube_transcript_api import YouTubeTranscriptApi
import importlib
from langchain_community.chat_models import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema.output_parser import StrOutputParser
from typing import List

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
import sys
sys.path.append('C:\\Users\\vital\\streamlit_suite\\src')
import my_utils.my_utils  # Adjust based on your actual import path
importlib.reload(my_utils.my_utils)
from my_utils.my_utils import MyUtils
from prompts.prompts import Prompts
from youtube_transcript_api.formatters import TextFormatter
from typing import Dict
import requests
import re


from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
from IPython.display import Markdown, display
import os

my_utils = MyUtils()
my_prompts = Prompts()
model = ChatOpenAI(temperature=0)
#model = ChatOpenAI(model = "gpt-4-0125-preview", temperature=0)

article = my_prompts.get_test_research_chapter()


class Questions(BaseModel):
    questions: Dict[str, str] = Field(
        ..., 
        description="Dynamic dictionary to store an arbitrary number of questions."
    )


def get_keyinfos_from_article(article):
    prompt = ChatPromptTemplate.from_template("""
    You extract surprising, insightful, and interesting information from text content. Identify the Main Ideas Of the Article.

    Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

    STEPS:
    1. Extract up to 15-50 of the most important, insightful, and/or interesting key points in a section called KEYPOINTS. If there are less than 15 then collect all of them. Make sure you extract at least 15.
    2. Extract up to 5-30 of the most important, insightful, and/or supporting arguments in a section called ARGUMENTS. If there are less than 5 then collect all of them. Make sure you extract at least 5.
    3. Extract up to 5-20 of the most important and/or insightful conclusions in a section called CONCLUSIONS. If there are less than 5 then collect all of them. Make sure you extract at least 5.

    OUTPUT INSTRUCTIONS
    - Only output Markdown.
    - Extract at least 15 KEYPOINTS answered from the content as Markdown H1 headers.
    - Extract at least 5 ARGUMENTS answered from the content as Markdown H1 headers.
    - Extract at least 5 KEYPOINTS answered from the content as Markdown H1 headers.
    - Do not give warnings or notes; only output the requested sections.
    - You use bulleted lists for output, not numbered lists.
    - Do not repeat key points, arguments or conclusions.
    - Ensure you follow ALL these instructions when creating your output.

    INPUT
    {article}
    """
    )
    chain = prompt | model | StrOutputParser()

    output = chain.invoke({"article": article})
    
    return output
    
    
def main(): 
    url = "https://thedankoe.com/letters/you-are-obligated-to-get-rich-in-your-20s/"
    #response = requests.get(url)
    #html = response.text
    #pattern = re.compile('<.*?>')
    #article = re.sub(pattern, '', html)
    documents = SimpleWebPageReader(html_to_text=True).load_data(
    #["https://thedankoe.com/letters/zero-to-1-million-as-a-one-person-business-while-working-2-4-hours-per-day/"]
    [url]
    )
    article = documents[0].get_content()

    article_summary_prompt = my_prompts.get_article_summary_prompt() 
    model_output = my_utils.get_model_StrOutputResponse_single_argument(article_summary_prompt, model, "article", article)
    print(model_output)
    my_utils.save_to_unprocessed_from_string(model_output, "get-rich")

main()