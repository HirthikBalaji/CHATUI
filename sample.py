import os.path
import pickle
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from colorama import Fore, Back, Style
import ollama
import glob


class pp:
    def __int__(self):
        pass

    def toast(self, text):
        print(Style.BRIGHT, Fore.MAGENTA)
        print(text)
        print(Style.RESET_ALL)

    def success(self, text):
        print(Style.BRIGHT, Fore.GREEN, Back.LIGHTBLUE_EX, end="")
        print(text)
        print(Style.RESET_ALL)


def Create_database():
    st = pp()
    path = "DATA"
    k = glob.glob("DATA/*")
    if os.path.exists("DATABASE.BIN"):
        with open("DATABASE.BIN", "rb") as f:
            data = pickle.load(f)
        if k == data["files"]:
            st.toast("ALREADY EMBEDDED!")
            return None
        else:
            st.toast("FILE MISMATCH WITH PREVIOUS SESSIONS RE-EMBEDDING!")
    if os.path.exists("CHROMADB"):
        shutil.rmtree("CHROMADB")
    st.toast("LOADING DOCUMENTS...")
    loader = DirectoryLoader(path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )
    # print_("SPLITTING DOCUMENTS...")
    chunks = text_splitter.split_documents(documents)
    st.toast(f"SPLIT {len(documents)} DOCUMENTS INTO {len(chunks)} CHUNKS.....")

    st.toast("EMBEDDING DOCUMENTS....")

    Chroma.from_documents(chunks, OllamaEmbeddings(model="nomic-embed-text"), persist_directory="CHROMADB")

    st.toast(f"SAVED {len(chunks)} CHUNKS ")
    st.success("CREATED DB!")
    data = {'files': k}
    with open("DATABASE.BIN", "wb") as f:
        pickle.dump(data,f)


def Memquery(context_text, query_text):
    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: 
    {question}
    """
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    return prompt


def RAG(query, K):
    q = query
    # Create_database(user)
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma(persist_directory='CHROMADB', embedding_function=embedding_function)
    results = db.similarity_search(q, k=K)
    if len(results) == 0:
        # print_(f"NO MEMORY RELATED TO THE QUESTION {q}")
        return "NO MEMORY RELATED TO THE QUESTION"
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    del db
    return context_text


Create_database()
while True:
    q = input(Fore.YELLOW + ">>>")
    if q == 'q':
        break
    ct = RAG(q, 5)
    pt = Memquery(ct, q)
    resp = ''
    m = [
        {
            'role': 'system',
            'content': 'YOU ARE A GOOD AI MODEL WHICH UNDERSTANDS ANYTHING AND ANSWERS PROPERLY'
        },
        {
            'role': 'user',
            'content': pt
        }
    ]

    g = ollama.chat(model="qwen2:1.5b", messages=m, stream=True)
    for chunk in g:
        print(chunk['message']['content'], end='')
        resp = resp + chunk['message']['content']
    print()
