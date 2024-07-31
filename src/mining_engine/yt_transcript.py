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
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict


video_url = 'https://www.youtube.com/watch?v=mwH10sE-8wY'
model = ChatOpenAI(model="gpt-4-0125-preview")

my_utils = MyUtils()
my_prompts = Prompts()

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

def get_summary_from_transcript(transcript):
    prompt1 = my_prompts.get_article_summary_prompt()
    chain = prompt1 | model | StrOutputParser()
    output2 = my_utils.get_model_StrOutputResponse_single_argument(prompt1, model, "article", transcript)
    return output2



def main():
    transcript = my_utils.get_transcript(video_url)
    _, video_title = my_utils.get_yt_video_info(video_url)
    summary = get_summary_from_transcript(transcript)
    my_utils.save_to_unprocessed_from_string(summary, video_title)

main()