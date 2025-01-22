import sqlite3
import argparse
import logging
import faiss
import numpy as np
from tqdm import tqdm
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# init params
def init():
  parser = argparse.ArgumentParser(prog="createVS.py", description="create a FAISS vector store from an sqlite DB")
  parser.add_argument("db_path", help="path to sqlite .db file")
  parser.add_argument("table_name", help="the table where text is stored under a 'content' label")
  parser.add_argument("save_location", help="loaction for FAISS VS to be stored")
  return parser.parse_args()

# Load documents from SQLite3 database
def load_documents_from_db(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Assuming the table has a column named 'content' containing text
    cursor.execute(f"SELECT content FROM {table_name}")
    rows = cursor.fetchall()
    
    documents = [Document(page_content=row[0]) for row in rows]
    conn.close()
    
    return documents

# Split documents into manageable chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)

# Create vector store using FAISS
def create_vector_store(documents, embedding_model):
    logging.info("Creating vector store with FAISS")

    # Step 1: Create a FAISS index
    dimension = len(embedding_model.embed_query("test"))
    index = faiss.IndexFlatL2(dimension)
    
    # Step 2: Prepare the docstore and index-to-docstore mapping
    docstore = {}
    index_to_docstore_id = {}

    # Step 3: Process and add documents
    for idx, doc in enumerate(tqdm(documents, desc="Indexing documents")):
        # Embed the document and add to FAISS index
        embedding = embedding_model.embed_query(doc.page_content)
        embedding = np.array(embedding, dtype=np.float32).reshape(1, -1)
        index.add(embedding)
        
        # Store document in docstore and map the index
        doc_id = f"doc_{idx}"
        docstore[doc_id] = doc
        index_to_docstore_id[idx] = doc_id

        logging.info(f"Indexed document {idx + 1}/{len(documents)}")

    # Step 4: Create the FAISS vector store with the index and mappings
    vector_store = FAISS(index=index, docstore=docstore, index_to_docstore_id=index_to_docstore_id)
    logging.info("Vector store created successfully")
    
    return vector_store

# Main function
def main():
    # Init params
    params = init()
    db_path = params.db_path
    table_name = params.table_name
    save_file = params.save_location
    
    # Load and split the documents
    documents = load_documents_from_db(db_path, table_name)
    split_docs = split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    # Create vector store
    vector_store = create_vector_store(split_docs, embeddings)

    # Save the vector store for future use
    vector_store.save_local(save_file)

    print("Vector database created and saved successfully!")

if __name__ == "__main__":
    main()