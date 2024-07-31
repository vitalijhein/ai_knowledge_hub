import os
import openai
import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from trulens_eval import Tru
from llama_index.llms.openai import OpenAI
import numpy as np
from trulens_eval import (
    Feedback,
    TruLlama,
    OpenAI
)

from trulens_eval.feedback import Groundedness
from dotenv import load_dotenv, find_dotenv

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

from llama_index.readers.obsidian import ObsidianReader
from llama_index.core import VectorStoreIndex
import logging
import sys
import os
from llama_index.core import ServiceContext, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core.indices.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.indices.postprocessor import SentenceTransformerRerank
from llama_index.core import load_index_from_storage
from llama_index.llms.openai import OpenAI as LIOpenAI

from llama_index.core  import Document


_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']
llm = LIOpenAI(model="gpt-3.5-turbo", temperature=0.1)


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


BASE_PATH = "C:\\Users\\vital\\iCloudDrive\\iCloud~md~obsidian\\new_vault\\01 Zettelkasten\\"




def build_sentence_window_index(
    documents,
    llm,
    embed_model="local:BAAI/bge-small-en-v1.5",
    sentence_window_size=3,
    save_dir="sentence_index",
):
    # create the sentence window node parser w/ default settings
    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=sentence_window_size,
        window_metadata_key="window",
        original_text_metadata_key="original_text",
    )
    sentence_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
        node_parser=node_parser,
    )
    if not os.path.exists(save_dir):
        sentence_index = VectorStoreIndex.from_documents(
            documents, service_context=sentence_context
        )
        sentence_index.storage_context.persist(persist_dir=save_dir)
    else:
        sentence_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=save_dir),
            service_context=sentence_context,
        )

    return sentence_index


def get_sentence_window_query_engine(
    sentence_index, similarity_top_k=6, rerank_top_n=2
):
    # define postprocessors
    postproc = MetadataReplacementPostProcessor(target_metadata_key="window")
    rerank = SentenceTransformerRerank(
        top_n=rerank_top_n, model="BAAI/bge-reranker-base"
    )

    sentence_window_engine = sentence_index.as_query_engine(
        similarity_top_k=similarity_top_k, node_postprocessors=[postproc, rerank]
    )
    return sentence_window_engine




def get_prebuilt_trulens_recorder(query_engine, app_id):
    openai = OpenAI()

    qa_relevance = (
        Feedback(openai.relevance_with_cot_reasons, name="Answer Relevance")
        .on_input_output()
    )

    qs_relevance = (
        Feedback(openai.relevance_with_cot_reasons, name = "Context Relevance")
        .on_input()
        .on(TruLlama.select_source_nodes().node.text)
        .aggregate(np.mean)
    )

    grounded = Groundedness(groundedness_provider=openai)

    groundedness = (
        Feedback(grounded.groundedness_measure_with_cot_reasons, name="Groundedness")
            .on(TruLlama.select_source_nodes().node.text)
            .on_output()
            .aggregate(grounded.grounded_statements_aggregator)
    )

    feedbacks = [qa_relevance, qs_relevance, groundedness]
    tru_recorder = TruLlama(
        query_engine,
        app_id=app_id,
        feedbacks=feedbacks
    )
    return tru_recorder



def run_evals(eval_questions, tru_recorder, query_engine):
    for question in eval_questions:
        with tru_recorder as recording:
            response = query_engine.query(question)

def main():
    documents = ObsidianReader(
        BASE_PATH
    ).load_data()  # Returns list of documents

    document = Document(text="\n\n".join([doc.text for doc in documents]))
    
    index = build_sentence_window_index(
    [document],
    llm=llm,
    save_dir="./sentence_index",
    )

    query_engine = get_sentence_window_query_engine(index, similarity_top_k=6)
    eval_questions = [
    "What are the most effective strategies for building long-term wealth?",
    "How does investment diversification contribute to wealth accumulation?",
    "Can you explain the importance of compound interest in wealth building?",
    "What role does entrepreneurship play in achieving financial independence?",
    "How crucial is financial literacy in the process of getting rich?",
    "Describe the risks and benefits of real estate investment as a wealth-building strategy.",
    "How can one balance risk and reward in stock market investments?",
    "What are common financial mistakes people should avoid when trying to get rich?",
    "How can setting financial goals contribute to wealth accumulation?",
    "Explain the impact of personal savings rate on the path to becoming rich.",
    "What are the key elements of a compelling narrative?",
    "How can a writer effectively develop characters in a story?",
    "Describe the process of outlining a story before writing.",
    "How important is the setting in a story, and how can it be effectively described?",
    "What techniques can writers use to maintain reader interest throughout a piece?",
    "Discuss the role of conflict in storytelling and how it can be used effectively.",
    "What are some common pitfalls in writing dialogue, and how can they be avoided?",
    "How can writers improve their writing style and voice?",
    "Explain the revision process and its importance in writing.",
    "How can feedback from others be incorporated into the writing process?"
    ]

    Tru().reset_database()
    
    
    sentence_index_1 = build_sentence_window_index(
        documents,
        llm=llm,
        embed_model="local:BAAI/bge-small-en-v1.5",
        sentence_window_size=1,
        save_dir="sentence_index_1",
    )
    sentence_window_engine_1 = get_sentence_window_query_engine(
        sentence_index_1
    )

    tru_recorder_1 = get_prebuilt_trulens_recorder(
        sentence_window_engine_1,
        app_id='sentence window engine 1'
    )
    run_evals(eval_questions, tru_recorder_1, sentence_window_engine_1)
   
    sentence_index_3 = build_sentence_window_index(
        documents,
        llm=llm,
        embed_model="local:BAAI/bge-small-en-v1.5",
        sentence_window_size=3,
        save_dir="sentence_index_3",
    )
    sentence_window_engine_3 = get_sentence_window_query_engine(
        sentence_index_3
    )

    tru_recorder_3 = get_prebuilt_trulens_recorder(
        sentence_window_engine_3,
        app_id='sentence window engine 3'
    )
    run_evals(eval_questions, tru_recorder_3, sentence_window_engine_3)
    #Tru().run_dashboard()
    
    sentence_index_10 = build_sentence_window_index(
        documents,
        llm=llm,
        embed_model="local:BAAI/bge-small-en-v1.5",
        sentence_window_size=10,
        save_dir="sentence_index_10",
    )
    sentence_window_engine_10 = get_sentence_window_query_engine(
        sentence_index_10
    )

    tru_recorder_10 = get_prebuilt_trulens_recorder(
        sentence_window_engine_10,
        app_id='sentence window engine 10'
    )
    run_evals(eval_questions, tru_recorder_10, sentence_window_engine_10)


main()
