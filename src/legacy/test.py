import sys
import json
sys.path.append('C:\\Users\\vital\\streamlit_suite\\src')
from my_utils.my_utils import MyKnowledgeBaseBuilder, MyUtils
from my_utils.mongo_database import MongoDatabase
from prompts.prompts import Prompts
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import JsonOutputParser

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
my_Knowledgebase_builder = MyKnowledgeBaseBuilder()
my_prompts=Prompts()
my_utils=MyUtils()
my_mdb = MongoDatabase()
from typing import Dict, Optional
import csv
import os
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.readers.file import FlatReader
from pathlib import Path
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
import chromadb 
from llama_index.core.retrievers import VectorIndexAutoRetriever

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

import os
from llama_index.core.node_parser import SentenceSplitter


class TokenBot(BaseModel):
    Alert_Time: str = Field(description="The date and time when the alert was posted")
    Token: str = Field(description="The Token name, a short string starts with '$'")
    Adress: str = Field(description="The Token adress, a Base64 String that is a unique token adress")
    Market_Cap: str = Field(None, description="Market Capitalization: The current market cap when alert was posted")
    Token_Price: str = Field(None, description="The current token price when alert was posted")
    Mint_Authority: str = Field(None, description="Information, if Mint Authority is enabled or disabled or N/A")
    LP_burned:  str = Field(None, description="Information, if Liqidity Pool was burned or N/A")
    Trending:  str = Field(None, description="Information, if Token is trending")
    Lord_Impact:  str = Field(None, description="Information, on calculated Lord Impact")
    Lord_Ratio:  str = Field(None, description="Information, on calculated Lord Ratio/VMR")
    TwentyFourHoursVol: str = Field(None, description="Information, on 24h volume")
    Lord_Score: str = Field(None, description="Information, on calculated Lord Score")
    Holders: str = Field(None, description="Information, on token holders")
    Deployer: str = Field(None, description="Information, on Deployer Balances in SOL or ETH or WETH")
    Deployer_Percent: str = Field(None, description="Information, on Deployer in Percent")
    Top_Holders: str = Field(None, description="Information, on Top Holders")
    Liquidity_Pool_Balance: str = Field(None, description="Information, on provided Liquidity Pool")
    SOL_Supply: str = Field(None, description="Information, on provided Sol/Supply")
    

    

class AllTimeHighAlert(BaseModel):
    Token: str = Field(description="The Token name, a short string starts with '$'")
    Adress: str = Field(description="The TOken adress, a Base64 String that is a unique token adress")
    ATH: str = Field(None, description="All Time High: A multiplier value, that shows how often times the token has grown in market cap")
    Market_Cap: str = Field(None, description="Market Capitalization: The new highest market cap due to the All")
    ATH_was: str = Field(None, description="Information, when the All Time high was.")
    Alert_posted: str = Field(None, description="Information, when the intial alert was posted, before the all time high occured")
    
    
    
def get_json_from_tweet(tweet, tweet_type, prompt1):
    parser = JsonOutputParser(pydantic_object=tweet_type)
    model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0, max_tokens=4096, model_kwargs={"top_p": 0.9})
    chain = prompt1 | model | parser
    model_output_questions_dict = chain.invoke({"tweet": tweet})
    return model_output_questions_dict


def save_to_csv(data_dict, filename="model_output_questions.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys(), delimiter='\t')
        
        if not file_exists:
            writer.writeheader()  # Only write header if file does not exist
        
        writer.writerow(data_dict)
        
        
def get_all_time_highs():
    # Path to your JSON file
    file_path = "C:\\Users\\vital\\Downloads\\Telegram Desktop\\ChatExport_2024-04-01 (1)\\result.json"

    # Reading the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Now, `data` is a Python dictionary that contains the contents of your JSON file.
    # You can work with it just like any other dictionary.
    #print(data)
    parser = JsonOutputParser(pydantic_object=AllTimeHighAlert)

    question_extraction_prompt = ChatPromptTemplate.from_template(
            template = """
                You extract Token, Adress, ATH, Market_Cap, ATH_was and Alert_posted from dictionaries.

                Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

                STEPS
                1. Extract the Token from the dictionaries.
                2. Extract the Adress from the dictionaries.
                3. Extract the ATH from the dictionaries.
                4. Extract the Market_Cap from the dictionaries.
                5. Extract the ATH_was from the dictionaries.
                6. Extract the Alert_posted from the dictionaries.
                
                OUTPUT INSTRUCTIONS
                {format_instructions}

                Input:
                {tweet}
                """,
                partial_variables={"format_instructions": parser.get_format_instructions()},
        )

    # If you want to loop through messages as in your previous request, you could do:
    if "messages" in data:
        for message in data["messages"]:
            if message.get("from") == "DexLord SOL Bot":
                print(f'Message ID: {message.get("id", "N/A")}')
                print(f'Message date: {message.get("date_unixtime", "N/A")}')
                print(len(message.get("text_entities")))
                if len(message.get("text_entities")) > 10:
                    print('---')
                    try:
                        model_output_questions_dict = get_json_from_tweet(message.get("text_entities"), AllTimeHighAlert, question_extraction_prompt)
                        save_to_csv(model_output_questions_dict, "model_output_questions.csv")
                    except:
                        continue
                    print(model_output_questions_dict)





def get_all_tokens():
     # Path to your JSON file
    file_path = "C:\\Users\\vital\\Downloads\\Telegram Desktop\\ChatExport_2024-04-01 (1)\\result.json"

    # Reading the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Now, `data` is a Python dictionary that contains the contents of your JSON file.
    # You can work with it just like any other dictionary.
    #print(data)
    parser = JsonOutputParser(pydantic_object=TokenBot)
    question_extraction_prompt = ChatPromptTemplate.from_template(
        template = """
            You extract Alert_Time, Token, Adress, Market_Cap, Token_Price, Mint_Authority, LP_burned, Trending, Lord Impact, Lord Ratio, 24h Volume, Lord_Score,Holders, Deployer, Deployer_Percent, Top Holders, Liquidity_Pool_Balance and SOL_Supply from dictionaries.

            Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

            STEPS
            1. Extract the Alert_Time from the dictionaries.
            2. Extract the Token from the dictionaries.
            3. Extract the Adress from the dictionaries.
            4. Extract the Market_Cap from the dictionaries.
            5. Extract the Token_Price from the dictionaries.
            6. Extract the Mint_Authority from the dictionaries.
            7. Extract the LP_burned from the dictionaries.
            8. Extract the Trending from the dictionaries.
            9. Extract the Lord Impact from the dictionaries.
            10. Extract the Lord Ratio from the dictionaries.
            11. Extract the 24h Volume from the dictionaries.
            12. Extract the Lord_Score from the dictionaries.
            13. Extract the Holders from the dictionaries.
            14. Extract the Deployer from the dictionaries.
            15. Extract the Deployer_Percent from the dictionaries.
            16. Extract the Holders from the dictionaries.
            17. Extract the Liquidity_Pool_Balance from the dictionaries.
            18. Extract the SOL_Supply from the dictionaries.

            OUTPUT INSTRUCTIONS
            {format_instructions}

            Input:
            {tweet}
            """,
            partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    # If you want to loop through messages as in your previous request, you could do:
    if "messages" in data:
        for message in data["messages"]:
            if message.get("from") == "DexLord SOL Alerts":
                print(f'Message ID: {message.get("id", "N/A")}')
                print(f'Message date: {message.get("date_unixtime", "N/A")}')
                if message.get("id") >= 20522:
                    print(len(message.get("text_entities")))
                    if len(message.get("text_entities")) > 10:
                        print('---')
                        try:
                            model_output_questions_dict = get_json_from_tweet(message.get("text_entities"), AllTimeHighAlert, question_extraction_prompt)
                            save_to_csv(model_output_questions_dict, "model_output_tokens.csv")
                        except:
                            continue
                        print(model_output_questions_dict)
                    
def main():
    get_all_tokens()
    
main()

#20522