import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load cleaned data with specified encoding
loader = TextLoader("data/all_info.txt", encoding="utf-8")
documents = loader.load()

# Split text into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

# Load sentence transformer embeddings using a Hugging Face model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create and save FAISS vector store
vector_store = FAISS.from_documents(docs, embeddings)
vector_store.save_local("faiss_index")

print("✅ FAISS vector store created and saved successfully!")
