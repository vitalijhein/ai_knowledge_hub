# my_utils.py
import os
import datetime
from youtube_transcript_api import YouTubeTranscriptApi

from yt_dlp import YoutubeDL
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex
from trulens_eval import (
    Feedback,
    TruLlama,
    OpenAI as fOpenAI
)
from langchain_openai import ChatOpenAI
from llama_index.llms.openai import OpenAI as LIOpenAI
import numpy as np


from trulens_eval.feedback import Groundedness
from dotenv import load_dotenv, find_dotenv

from llama_index.core import VectorStoreIndex

import os
from llama_index.core import ServiceContext, StorageContext
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core.indices.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.indices.postprocessor import SentenceTransformerRerank
from llama_index.core import load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

BASE_PATH = os.environ['BASE_PATH']
SAVE_PATH = os.environ['SAVE_PATH']

OPENAI_API = os.environ['OPENAI_API_KEY']

class MyUtils:
    def __init__(self):
        pass
    
    # Function to find Markdown files and their folders
    def find_md_files_and_folders(self, directory):

        md_files = []
        folders = set()
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    md_files.append((file, os.path.join(root, file)))
                    display_folder = root.replace(BASE_PATH, "")
                    folders.add(display_folder)
        return md_files, list(folders)
        
    def get_openai_key(self):
        return OPENAI_API
        
    def get_BASE_PATH(self):
        return BASE_PATH
        
    def get_SAVE_PATH(self):
        return SAVE_PATH
    
    def save_to_unprocessed_from_list(self, outputs_list, video_title):
        video_title = self.sanitize_title_for_display(video_title)

        SAVE_PATH_File = f'{SAVE_PATH}\\{video_title}.md'
        with open(SAVE_PATH_File, 'w') as file:
            for question, output in outputs_list:
                file.write(f"{question}\n{output}\n\n")
    
    def save_to_unprocessed_from_string(self, model_output_string, video_title):
        video_title = self.sanitize_title_for_display(video_title)

        SAVE_PATH_File = f'{SAVE_PATH}\\{video_title}.md'
        with open(SAVE_PATH_File, 'w', encoding="utf-8") as file:
            file.write(f"{model_output_string}")
        return video_title
                
                
    def sanitize_title_for_display(self, title):
        # Characters not allowed in Windows filenames
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        # Replace each invalid character with an underscore or any suitable character
        for char in invalid_chars:
            title = title.replace(char, '. ')
        # Trim spaces at the end if any (since filenames cannot end with a space)
        title = title.rstrip(' ')
        # Ensure the title does not end with a dot (.)
        if title.endswith('.'):
            title = title[:-1] + '_'
        return title

    def get_yt_video_info(self, url):
        ydl_opts = {
            'quiet': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Unknown Title')
            # Return other information as needed
            return info_dict, video_title

    def get_model_StrOutputResponse_single_argument(self, input_prompt, model, key_name, key_value):
        
        chain = input_prompt | model | StrOutputParser()
        dynamic_dict = {key_name: key_value}

        model_output = chain.invoke(dynamic_dict)
        return model_output
    
    
    def get_model_StrOutputResponse_dynamic_argument(self, input_prompt, model, dynamic_dict):
    
        chain = input_prompt | model | StrOutputParser()

        model_output = chain.invoke(dynamic_dict)
        return model_output
    
    
    def extract_video_id(self, video_id_or_url):
        if len(video_id_or_url) > 11:
            return video_id_or_url[-11:]
        else:
            return video_id_or_url


    def get_transcript(self, video_url_or_id):
        try:
            video_id = self.extract_video_id(video_url_or_id)
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
            return transcript
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_article(self, article_url):
        try:
            video_id = self.extract_video_id(article_url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except Exception as e:
            print(f"Error: {e}")
            return None


class MyKnowledgeBaseBuilder:
    def __init__(self):
        pass
    
    def get_chroma_vectorstore_collection_list(self):
        # initialize client
        db = chromadb.PersistentClient(path=".\\chroma_db")

        # get collection
        collection_list = db.list_collections()


        #chroma_collection = db.get_or_create_collection(collection_name)

       
        return collection_list

    
    def create_vectorstore_from_node_return_query_engine(self, nodes=None, top_k=3, similarity_cutoff = 0.7, collection_name = "quickstart"):        
        if nodes is None:
            # load from disk
            db2 = chromadb.PersistentClient(path="./chroma_db")
            chroma_collection = db2.get_or_create_collection(collection_name)
            vector_store2 = ChromaVectorStore(chroma_collection=chroma_collection)
            index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store2
                )
            
        else:
            db = chromadb.PersistentClient(path="./chroma_db")
            chroma_collection = db.get_or_create_collection(collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            index = VectorStoreIndex(
                nodes, storage_context=storage_context
            )
            
        # Query Data from the persisted index
        retriever = VectorIndexRetriever(
                index=index,
                similarity_top_k=top_k,
            )

        response_synthesizer = get_response_synthesizer()

        # assemble query engine
        query_engine_vectorindex = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=similarity_cutoff)],
        )
        return index, query_engine_vectorindex
    
    
    def create_knowledgegraph_from_node_return_query_engine(self, nodes, top_k = 10, max_triplets_per_chunk=2):
        new_index_kg = KnowledgeGraphIndex(
            nodes,
            max_triplets_per_chunk=max_triplets_per_chunk,
            include_embeddings=True,
        )
        # query using top 3 triplets plus keywords (duplicate triplets are removed)
        query_engine_kg = new_index_kg.as_query_engine(
            include_text=True,
            response_mode="tree_summarize",
            embedding_mode="hybrid",
            similarity_top_k=top_k,
        )
        return query_engine_kg
    
    
    def create_sentencewindow_from_node_return_query_engine(self, nodes, sentence_window_size = 1):
        sentence_index = self.build_sentence_window_index_nodes(
            nodes,
            llm=ChatOpenAI(),
            embed_model="local:BAAI/bge-small-en-v1.5",
            sentence_window_size=sentence_window_size,
            save_dir="./knowledge_enginge/knowledgebase/sentence_index_1-koe-v3_node",
        )
        query_engine_sentencewindow = self.get_sentence_window_query_engine(sentence_index)
        return query_engine_sentencewindow
    
    
    
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


    def build_sentence_window_index_nodes(self, 
        nodes,
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
            sentence_index = VectorStoreIndex(
                nodes, service_context=sentence_context
            )
            sentence_index.storage_context.persist(persist_dir=save_dir)
        else:
            sentence_index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=save_dir),
                service_context=sentence_context,
            )

        return sentence_index


    def get_sentence_window_query_engine(self, 
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


    def get_prebuilt_trulens_recorder(self, query_engine, app_id):
        openai = fOpenAI()

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



    def run_evals(self, eval_questions, tru_recorder, query_engine):
        for question in eval_questions:
            with tru_recorder as recording:
                response = query_engine.query(question)