import sys

sys.path.append('C:\\Users\\vital\\streamlit_suite\\src')
from my_utils.my_utils import MyKnowledgeBaseBuilder, MyUtils
from my_utils.mongo_database import MongoDatabase
from prompts.prompts import Prompts
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
my_Knowledgebase_builder = MyKnowledgeBaseBuilder()
my_prompts=Prompts()
my_utils=MyUtils()
my_mdb = MongoDatabase()
from typing import Dict, Optional

from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.readers.file import FlatReader
from pathlib import Path
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
import chromadb 
from llama_index.core.retrievers import VectorIndexAutoRetriever

import os
from llama_index.core.node_parser import SentenceSplitter

# Define your desired data structure.
class Lit_Listicle_Tweet(BaseModel):
    whole_tweet: str = Field(description="the complete tweet")
    headline: str = Field(description="the headline from the tweet")
    bullet1: Optional[str] = Field(None, description="the first bullet from the tweet")
    bullet2: Optional[str] = Field(None, description="the second bullet from the tweet")
    bullet3: Optional[str] = Field(None, description="the third bullet from the tweet")
    bullet4: Optional[str] = Field(None, description="the fourth bullet from the tweet")
    bullet5: Optional[str] = Field(None, description="the fifth bullet from the tweet")
    bullet6: Optional[str] = Field(None, description="the sixth bullet from the tweet")
    bullet7: Optional[str] = Field(None, description="the seventh bullet from the tweet")
    bullet8: Optional[str] = Field(None, description="the eighth bullet from the tweet")
    bullet9: Optional[str] = Field(None, description="the ninth bullet from the tweet")
    bullet10: Optional[str] = Field(None, description="the tenth bullet from the tweet")
    conclusion: str = Field(description="the conclusion of the tweet")
    
# Define your desired data structure.
class Private_Tweet(BaseModel):
    whole_tweet: str = Field(description="the complete tweet")

# Define your desired data structure.
class Actionable_Poster_Tweet(BaseModel):
    whole_tweet: str = Field(description="the complete tweet")
    
# Define your desired data structure.
class Actionable_Single_Tweet(BaseModel):
    whole_tweet: str = Field(description="the complete tweet")
    
# Define your desired data structure.
class Thread_Outline_Tweet(BaseModel):
    whole_tweet: str = Field(description="the complete tweet")

def find_md_files_and_folders(directory):
    md_files = []
    folders = set()
    file_paths = []  # Initialize an empty list to store the file paths
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)  # The full path of the file
                md_files.append((file, full_path))
                file_paths.append(full_path)  # Add the full path to the file_paths list
                display_folder = root.replace(directory, "")  # Assuming BASE_PATH should be directory
                folders.add(display_folder)
    return md_files, list(folders), file_paths  # Return file_paths as well

# Example usage
# BASE_PATH = '/your/base/path'
# md_files, folders, file_paths = find_md_files_and_folders(BASE_PATH)
# print(md_files, folders, file_paths)

from langchain_core.prompts import ChatPromptTemplate

def get_actionable_tweet_prompt_test3():
    
    actionale = ChatPromptTemplate.from_template(template ="""I want you to write Threads following the "What-Why-How-Snap" structure, without labeling the parts. 

The "What-Why-How-Snap" framework is a 4-part framework for every individual tweet in the thread. It works like this:
1) "What": The first part of the tweet stating what you are talking about in less than 9 words. This can be a tip, a resource, or something else.
2) "Why": Logically explains why the "What" is relevant in 8 words or less. Can't begin with "to" or "this".
3) "How": 3-5 actionable steps on 2-5 words each in bullet points “•” on how the audience can implement the advice
4) "Snap": a short, sequence that wraps up the tweet with a takeaway, wise quote, or lesson. Reading the "snap" should leave the reader with a sense of satisfaction.

You do not need to label your output with "Snap" "What" "Why" "How" etc.

STEPS:
1) Silently analyse the "What-Why-How-Snap" framework I gave you
2) Silently analyse the context I gave you and think about ideas compelling to my audience
3) Use your insights from 1) and 2) with the characteristics I gave you and write a Thread following the "What-Why-How-Snap" Framework that are insanely valuable to my audience

OUTPUT FORMAT
1. No hashtags
2. Readability grade 7 or lower
3. Every tweet consists of 250-280 characters
4. No emojis
5. Use concise language
6. Each tweet in the thread should follow the "What-Why-How-Snap" framework
7. Use complete sentences and emphasize benefits over features.
8. Use active voice

INPUT
{tweet}


No hashtags.
"""
    )
    
    return actionale       

def read_utf8_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def get_json_from_tweet(tweet, tweet_type):
    parser = JsonOutputParser(pydantic_object=tweet_type)
    prompt1 = my_prompts.get_tweets_from_transcript_as_dict(parser)
    model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0, max_tokens=4096, model_kwargs={"top_p": 0.9})
    chain = prompt1 | model | parser
    model_output_questions_dict = chain.invoke({"tweet": tweet})
    return model_output_questions_dict


def get_thread_outline(model_output, model):
    actionable_tweet_prompt = get_actionable_tweet_prompt_test3()
    threat_outline = []
    model_output_split = model_output.split("[NEW POST]")
    for tweet in model_output_split[1:]:
        print("---------------- Tweet ----------------")
        print(tweet)
        json_tweet = get_json_from_tweet(tweet, "Lit_Listicle_Tweet")
        print("---------------- json_tweet ----------------")
        print(json_tweet)
        for key, value in json_tweet.items():
            if key == "headline":
                threat_outline.append(value)
                
            if key != "headline" and key != "conclusion" and key != "whole_tweet":
                dynamic_dict = {"tweet": value}
                model_output_actionable = my_utils.get_model_StrOutputResponse_dynamic_argument(actionable_tweet_prompt, model, dynamic_dict)
                threat_outline.append(value + "\n\n" +model_output_actionable)
                print("---------------- model_output_actionable ----------------")
                print(model_output_actionable)
            if key == "conclusion":
                threat_outline.append(value)
        threat_outline.insert(0, '')  # Insert an empty string at the beginning of the list
        threads = "\n\n[NEW POST]\n\n".join(threat_outline)
        my_utils.save_to_unprocessed_from_string(threads, json_tweet["headline"]+"_threads_outline")

def get_lit_listicle(topic_response, model, query):
    lit_listicle_prompt = my_prompts.get_lit_listicles_prompt()
    dynamic_dict = {"topic": topic_response}


    model_output = my_utils.get_model_StrOutputResponse_dynamic_argument(lit_listicle_prompt, model, dynamic_dict)
    #print(model_output)
    my_utils.save_to_unprocessed_from_string(model_output, query+"_lit_listicle_tweets")
    return model_output

def generate_asci_art_from_tweet(tweet,query):
    asci_prompt, model = my_prompts.get_asci_art_prompt()
    dynamic_dict = {"tweet": tweet}
    model_output = my_utils.get_model_StrOutputResponse_dynamic_argument(asci_prompt, model, dynamic_dict)
    my_utils.save_to_unprocessed_from_string(model_output, query+"_asci_art")
    return model_output 

def generate_actionable_single_tweet(tweet, model, query, context):
    actionable_prompt = my_prompts.get_actionable_single_tweet()
    dynamic_dict = {"context": context ,"tweet": tweet}
    model_output = my_utils.get_model_StrOutputResponse_dynamic_argument(actionable_prompt, model, dynamic_dict)
    my_utils.save_to_unprocessed_from_string(model_output, query+"_single_tweet")
    return model_output 

def generate_actionable_posters(tweet, query):
    actionable_prompt, model = my_prompts.get_actionable_posters()
    dynamic_dict = {"tweet": tweet}
    model_output = my_utils.get_model_StrOutputResponse_dynamic_argument(actionable_prompt, model, dynamic_dict)
    my_utils.save_to_unprocessed_from_string(model_output, query+"_actionable_poster_tweet")
    return model_output 


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
    
def main(): 
    ### list
    index, query_engine = my_Knowledgebase_builder.create_vectorstore_from_node_return_query_engine(top_k=10,similarity_cutoff=0.7, collection_name="oldvault")
    ### get topic to write about
    query = "How to structure a writing routine?"
    #topic = query_engine.query("Give me an 9-step list about '" + query + "'." )
    topic = query_engine.query(query)
    topic_response = topic.response

    ### get context
    context = read_utf8_file("brand/context.txt")

    ### get audience
    audience = read_utf8_file("brand/audience.txt")

    
    ##get model
    model = ChatOpenAI(model="gpt-3.5-turbo-1106",max_tokens=3500, temperature=0.45, model_kwargs={"top_p": 0.75})


    #get_thread_outline(lit_listicles, model)
    single_tweets = generate_actionable_single_tweet(topic_response, model, query, context)
    split_single_tweets = single_tweets.split("[TWEET]")
    for single_tweet in split_single_tweets[1:]:
        model_output_questions_dict = get_json_from_tweet(single_tweet, Actionable_Single_Tweet)
        my_mdb.insert_one_into_collection_mdb("actionable_single_tweet_collection", model_output_questions_dict)
        print(single_tweets)
    ### get_tweet_prompt()
    ### 

        
    private_tweets = get_private_tweet(topic_response, model, query)
    split_private_tweets = private_tweets.split("[NEW TWEET]")
    for private_tweet in split_private_tweets[1:]:
        model_output_questions_dict = get_json_from_tweet(private_tweet, Private_Tweet)
        my_mdb.insert_one_into_collection_mdb("private_tweet_collection", model_output_questions_dict)
        print(private_tweet)
    
    lit_listicles = get_lit_listicle(topic_response, model, query)    
    split_lit_listicles = lit_listicles.split("[NEW POST]")
    for lit_listicle in split_lit_listicles[1:]:
        model_output_questions_dict = get_json_from_tweet(lit_listicle, Lit_Listicle_Tweet)
        my_mdb.insert_one_into_collection_mdb("lit_listicle_collection", model_output_questions_dict)
        print(lit_listicle)
        
    actionable_posters = generate_actionable_posters(topic_response, query)
    split_actionable_posters = actionable_posters.split("[NEW POST]")
    for actionable_poster in split_actionable_posters[1:]:
        model_output_questions_dict = get_json_from_tweet(actionable_poster, Actionable_Poster_Tweet)
        my_mdb.insert_one_into_collection_mdb("actionable_posters_collection", model_output_questions_dict)
        print(actionable_poster)
           
main()