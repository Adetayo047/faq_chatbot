from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

#Load Document
loader = TextLoader('./data/kogi_hayok_data.txt')
documents = loader.load()

#Split Document
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

#Initialize Embedding
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

vectordb = Chroma.from_documents(texts, embedding, persist_directory="./data/KOGI_VECTOR_STORE")
vectordb.persist()


# print(vectordb._collection.count())

# query = vectordb.similarity_search("what is the health plan for kogi state", k=3)
# print("Retrieved Documents:", [doc.page_content for doc in query])

# print(f"Number of documents in the vector store: {len(vectordb.get())}")
