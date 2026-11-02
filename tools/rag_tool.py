
from pathlib import Path

from dotenv import load_dotenv
from crewai.tools import tool

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

# Load environment variables
load_dotenv(BASE_DIR / ".env")


# 1. Build the RAG Vector Database
def build_vector_db():

    print("Loading company documents...")

    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    documents = loader.load()

    if not documents:
        raise ValueError(
            "No TXT documents found in the data folder."
        )

    print(f"Loaded {len(documents)} documents.")

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} text chunks.")

    # Generate embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    # Create FAISS vector database
    vector_db = FAISS.from_documents(
        chunks,
        embeddings
    )

    print("FAISS vector database created successfully.")

    return vector_db


# Build database once when this module loads
vector_db = build_vector_db()


# 2. Create RAG Search Tool
@tool("Customer Support Knowledge Base")
def customer_support_rag_tool(query: str) -> str:
    """
    Search the internal company knowledge base.

    Use this tool to find information about:
    company details, product FAQs, shipping policies,
    refund policies, warranty and customer support.

    Return relevant information from company documents only.
    """

    results = vector_db.similarity_search(
        query,
        k=4
    )

    if not results:
        return "No relevant information found in company documents."

    context = []

    for index, doc in enumerate(results, start=1):

        source = Path(
            doc.metadata.get("source", "Unknown")
        ).name

        context.append(
            f"Source {index}: {source}\n"
            f"Information: {doc.page_content}"
        )

    return "\n\n".join(context)


print("Customer Support RAG Tool is ready.")
