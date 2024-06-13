from langchain_community.document_loaders import TextLoader, CSVLoader, UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import langchain
import pandas as pd
import numpy as np
import faiss
import os
import pickle


# file = convert_text_file_to_utf8() 
# print(file)

def load_data_from_file(file_path):

    if file_path[-3:] == "txt":
        loader = TextLoader(file_path)
    elif file_path[-3:] == "csv":
        loader = CSVLoader(file_path)

    data = loader.load()
    content_of_page = data[0].page_content
    content_source = data[0].metadata["source"]

    # print(f"The content of the document is:\n{content_of_page}")
    # print(f"The source of the documentation is: {content_source}")

    return data

def load_data_from_url(urls:list):

    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    # content_of_website_page = data[0].page_content
    # content_source = data[0].metadata["source"]

    # print(f"The content of the document is:\n{content_of_website_page}")
    # print(f"The source of the documentation is: {content_source}")
    
    return data

def recurssively_split_text(text_to_split:list, *separators:str, chunk_size:int, chunk_overlap:int):

    text_to_split = text_to_split[0].page_content
    splitter = RecursiveCharacterTextSplitter(separators=list(separators), chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text_to_split)

    return chunks

def recurssively_split_documents(text_to_split:list, separators:list, chunk_size:int, chunk_overlap:int):

    splitter = RecursiveCharacterTextSplitter(separators=separators, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(text_to_split)

    return chunks

def query_data_from_csv(csv_path:str, sentence_transformer_model:str, query:str, number_of_results:int):

    pd.set_option('display.max_colwidth', 100)

    df = pd.read_csv(csv_path)
    encoder = SentenceTransformer(sentence_transformer_model)
    vectors = encoder.encode(df.sentence)
    number_of_elements, number_of_dimensions = vectors.shape
    index = faiss.IndexFlatL2(number_of_dimensions)
    index.add(vectors)
    search_query = query
    search_vector = encoder.encode(search_query)
    rs_search_vector = np.array(search_vector).reshape(1, -1)
    
    if number_of_results > len(df):
        print(f"The number of requested results ({number_of_results}) is more than the number of entries in the csv ({len(df)}) therefore the maximum number of results ({len(df)}) will be returned instead.")
        number_of_results = len(df)

    result_distances, result_indicies = index.search(rs_search_vector, k=number_of_results)
    query_result = df.loc[result_indicies[0]]

    print(f"The distances of the {number_of_results} elements from the search result are: {result_distances}\nThe indicies of the results are: {result_indicies}\nThe result of the query is:\n{query_result}")
    
    return query_result

def write_vectorindex_to_pickle_file(file_path:str, content_of_file):

    with open(file_path, "wb") as file:
        pickle.dump(content_of_file, file)

    pass

def load_vectorindex(file_path:str):

    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            vectorstore = pickle.load(file)
        return vectorstore
    else:
        print(f"The file path '{file_path}' does not exist.")
        pass

def create_url_vector(chunk_size:int, chunk_overlap:int, separators:list, urls:list):

    data = load_data_from_url(urls)
    chunks = recurssively_split_documents(data, separators, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    embeddings = OpenAIEmbeddings()
    openai_vectorindex = FAISS.from_documents(chunks, embeddings)

    return openai_vectorindex

def generate_query_and_result(temperature:int, max_tokens:int, query:str, chunk_size:int, chunk_overlap:int, separators:list, urls:list):

    langchain.debug = True
    # os.environ['OPENAI_API_KEY'] = openai_api_key
    llm = OpenAI(temperature=temperature, max_tokens=max_tokens)
    vector_index = create_url_vector(chunk_size, chunk_overlap, separators, urls)
    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vector_index.as_retriever())
    chain_result = chain({"question": query}, return_only_outputs=True)
    # print(chain_result)

    return chain_result

# load_dotenv()
if __name__ == "__main__":
    generate_query_and_result(0.9, 500, "What are the disadvantages of too much debt?", 1000, 200, ["\n\n", "\n", " "], ["https://hbr.org/1978/09/new-framework-for-corporate-debt-policy"])
# os.environ['OPENAI_API_KEY'] = openai_api_key

# llm = OpenAI(temperature=0.9, max_tokens=500)

# data = load_data_from_url("https://hbr.org/1978/09/new-framework-for-corporate-debt-policy")

# chunks = recurssively_split_documents(data, "\n\n", "\n", " ", chunk_size=1000, chunk_overlap=200)

# embeddings = OpenAIEmbeddings()

# openai_vectorindex = FAISS.from_documents(chunks, embeddings)

# # file_path = "vector_store.pkl"
# # with open(file_path, "wb") as file:
# #     pickle.dump(openai_vectorindex, file)

# # if os.path.exists(file_path):
# #     with open(file_path, "rb") as file:
# #         vectorstore = pickle.load(file)

# chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=openai_vectorindex.as_retriever())

# query = "What are the disadvantages of too much debt?"

# langchain.debug = True

# print(chain({"question": query}, return_only_outputs=True))
# print(len(chunks))
# print(chunks[0])
# print("-------------------------------------------------------")
# print(chunks)

# print(query_data_from_csv("sentence.csv", "all-mpnet-base-v2", "Which sentence relates to food?", 10))

# pd.set_option('display.max_colwidth', 100)

# df = pd.read_csv("sentence.csv")

# print(len(df))

# encoder = SentenceTransformer("all-mpnet-base-v2")

# # # print(df.text)

# vectors = encoder.encode(df.sentence)

# number_of_elements, number_of_dimensions = vectors.shape

# index = faiss.IndexFlatL2(number_of_dimensions)

# index.add(vectors)

# search_query = "Which one is about favorite food?"

# search_vector = encoder.encode(search_query)

# rs_search_vector = np.array(search_vector).reshape(1, -1)

# result_distances, result_indicies = index.search(rs_search_vector, k=6)

# query_result = df.loc[result_indicies[0]]

# print(f"The distances of the {6} elements from the search result are: {result_distances}\nThe indicies of the results are: {result_indicies}\nThe result of the query is:\n{query_result}")


# print(search_vector.shape)
# print(rs_search_vector.shape)
# print(type(vectors))
# print(vectors.shape)
# print(vectors[0])

# print(df.sentence)

# print(df.shape)
# print(df)

# chunks = recurssively_split_text(load_data_from_url("https://en.wikipedia.org/wiki/Sh%C5%8Dgun_(novel)"), "\n\n", "\n", " ", chunk_size=200, chunk_overlap=0)

# print(len(chunks))
# print(chunks)
# for chunk in chunks:
#     print(chunk)
#     print("-------------------------------------------------------")

# text = load_data_from_url("https://en.wikipedia.org/wiki/Sh%C5%8Dgun_(novel)")

# splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " "], chunk_size=200, chunk_overlap=0)

# chunks = splitter.split_text(text[0].page_content)

# print(type(chunks))

# for chunk in chunks:
#     print(chunk + "\n")