import sys

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
from llama_index.core import VectorStoreIndex
import chromadb 
from llama_index.core.retrievers import VectorIndexAutoRetriever

def mai2(): 
    parser = MarkdownNodeParser()
    
    md_docs = FlatReader().load_data(Path("C:\\Users\\vital\\streamlit_suite\\src\\zero-to-1-million-as-a-one-person-business-while-working-2-4-hours-per-day.md"))
    md_docs = FlatReader().load_data(Path("C:\\Users\\vital\\streamlit_suite\\src\\You Are Obligated to Get Rich in Your 20s.md"))

    nodes = parser.get_nodes_from_documents(md_docs)
    index, query_engine = my_Knowledgebase_builder.create_vectorstore_from_node_return_query_engine(nodes, similarity_cutoff=0.5)
    response = query_engine.query("How can one build a business quickly?")
    print(response)

    #chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
    index, query_engine = my_Knowledgebase_builder.create_vectorstore_from_node_return_query_engine(similarity_cutoff=0.5)
    response = query_engine.query("How can one build a business quickly?")

    #while True:
    #    response = chat_engine.chat("What about after that?")

    print(response)



import os
from llama_index.core.node_parser import SentenceSplitter

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




def main23(): 
    parser = MarkdownNodeParser()
    node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

    
    md_files, folders, file_paths = find_md_files_and_folders("C:\\Users\\vital\\iCloudDrive\\iCloud~md~obsidian\\vault")
    for file_path in file_paths: 
        print(file_path)
        md_docs = FlatReader().load_data(Path(file_path))

        nodes = node_parser.get_nodes_from_documents(md_docs)
        index, query_engine = my_Knowledgebase_builder.create_vectorstore_from_node_return_query_engine(nodes, similarity_cutoff=0.5, collection_name="oldvault")
    
    response = query_engine.query("What is my purpose?")
    print(response)

    #chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)
    index, query_engine = my_Knowledgebase_builder.create_vectorstore_from_node_return_query_engine(similarity_cutoff=0.5, collection_name="oldvault")
    response = query_engine.query("What is my purpose?")

    #while True:
    #    response = chat_engine.chat("What about after that?")

    print(response)

































def main2():
    # initialize client
    db = chromadb.PersistentClient(path="./chroma_db")
    parser = MarkdownNodeParser()

    # get collection
    print(db.list_collections())
    md_docs = FlatReader().load_data(Path("C:\\Users\\vital\\streamlit_suite\\src\\You Are Obligated to Get Rich in Your 20s.md"))

    nodes = parser.get_nodes_from_documents(md_docs)
    store_name = "vectorstore_topk_3_sim_cut_0"

    chroma_collection = db.get_or_create_collection(store_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    #storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=f".\\knowledge_base\\chroma_db\\{store_name}") # <- here you DO specify persist_dir
    #index = VectorStoreIndex([], vector_store=vector_store, storage_context=storage_context)
    index = VectorStoreIndex(nodes, vector_store=vector_store)
    db2 = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db2.get_or_create_collection("quickstart")
    vector_store2 = ChromaVectorStore(chroma_collection=chroma_collection)
    index2 = VectorStoreIndex.from_vector_store(vector_store=vector_store2)

    query_engine = index.as_query_engine()
    query_engine2 = index2.as_query_engine()

    print(query_engine.query("What are you Obligated to do in your 20s?"))
    print(query_engine2.query("What are you Obligated to do in your 20s?"))


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from IPython.display import Markdown, display
import chromadb
def main():
    #embed_model="local:BAAI/bge-small-en-v1.5"
    
    parser = MarkdownNodeParser()

    # get collection
    documents = FlatReader().load_data(Path("C:\\Users\\vital\\streamlit_suite\\src\\You Are Obligated to Get Rich in Your 20s.md"))
    nodes = parser.get_nodes_from_documents(documents)
    nodes = None
    if nodes is None:
         # load from disk
        db2 = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db2.get_or_create_collection("quickstart")
        vector_store2 = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store2
            )
        
    else:
        db = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db.get_or_create_collection("quickstart")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex(
            nodes, storage_context=storage_context
        )
        
    # Query Data from the persisted index
    retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=3,
        )

    response_synthesizer = get_response_synthesizer()

    # assemble query engine
    query_engine_vectorindex = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.5)],
    )
    response = query_engine_vectorindex.query("What are you Obligated to do in your 20s?")
    print(response)
    print("-----------------")
    query_engine = index.as_query_engine()
    response = query_engine.query("What are you Obligated to do in your 20s?")
    print(response)

    
    
main23()