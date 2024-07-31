import os
from haystack.nodes import EmbeddingRetriever, PreProcessor
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.pipelines import DocumentSearchPipeline
from haystack.utils import convert_files_to_docs

BASE_PATH = "C:\\Users\\v.hein\\iCloudDrive\\iCloud~md~obsidian\\new_vault\\"

# Function to find Markdown files and their folders
def find_md_files_and_folders(directory):
    md_files = []
    folders = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append((file, os.path.join(root, file)))
                display_folder = root.replace(BASE_PATH, "")
                folders.add(display_folder)
    return md_files, list(folders)

def main():
    markdown_files, folders = find_md_files_and_folders(BASE_PATH)
    
    # Initialize document store
    document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")

    # Initialize retriever
    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        use_gpu=False
    )

    # Convert markdown files to document objects
    # Adjusting this to directly process markdown_files list
    docs = []
    for filename, filepath in markdown_files:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            docs.append({'content': content, 'meta': {'name': filename}})

    # Preprocess documents
    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=True,
        split_by="word",
        split_length=200,
        split_respect_sentence_boundary=True
    )
    processed_docs = preprocessor.process(docs)

    # Add documents to the document store
    document_store.write_documents(processed_docs)

    # Update embeddings for all documents in the document store
    document_store.update_embeddings(retriever)

    # Initialize search pipeline
    pipeline = DocumentSearchPipeline(retriever)

    # Example search query, replace "Your search query" with an actual query
    query = "Example search query"
    results = pipeline.run(query=query, params={"Retriever": {"top_k": 10}})
    
    # Printing out the search results
    print("Search Results:")
    for result in results['documents']:
        print(f"Title: {result.meta['name']}, Score: {result.score}")

if __name__ == "__main__":
    main()
