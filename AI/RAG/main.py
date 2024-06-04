from langchain_community.document_loaders import TextLoader, CSVLoader, UnstructuredURLLoader
from ai_utils import convert_text_file_to_utf8

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

    print(f"The content of the document is:\n{content_of_page}")
    print(f"The source of the documentation is: {content_source}")

    return data

def load_data_from_url(*urls):

    loader = UnstructuredURLLoader(urls=list(urls))

    data = loader.load()

    content_of_website_page = data[0].page_content

    content_source = data[0].metadata["source"]

    print(f"The content of the document is:\n{content_of_website_page}")
    print(f"The source of the documentation is: {content_source}")
    
    return data

load_data_from_url("https://stackoverflow.com/questions/76600384/unable-to-read-text-data-file-using-textloader-from-langchain-document-loaders-l","https://en.wikipedia.org/wiki/Sh%C5%8Dgun_(novel)")