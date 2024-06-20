import streamlit as st
import openai
import ollama
import pickle
import os
from variables import NAME_PROMPT
st.set_page_config(layout='wide')
'''if os.path.exists('temp.bin'):
    with open('temp.bin', "rb") as file:
        st.session_state.messages = pickle.load(file)
else:'''
if "messages" not in st.session_state:
    st.session_state.messages = []

client = openai.OpenAI(api_key="blah-blah", base_url="http://localhost:11434/v1")
models = []
models_dict = {}
ollama_data = ollama.list()
for i in (ollama_data['models']):
    models.append(i['name'])
with st.sidebar:
    model = st.selectbox("name", models, index=len(models) - 1)
    st.toast(f"{model} Selected")
    sav = st.button("SAVE")
    cls = st.button("clear chat")
    if sav:
        name = ollama.generate(model='qwen2:0.5b', stream=False, system=NAME_PROMPT,
                               prompt=str(st.session_state.messages))
        with open(f"{name['response'].replace('"', '').replace('\'', '')}.bin", 'wb') as file:
            pickle.dump(st.session_state.messages, file)
        st.toast("SAVED CHAT!")
    if cls:
        st.session_state.messages = []
        with open("temp.bin", 'wb') as file:
            pickle.dump(st.session_state.messages, file)
        st.toast("cleared CHAT!")

prompt = st.chat_input("Say something")
for message in st.session_state.messages:
    if message['role'] == 'user':
        avatar = "🧑🏻‍💻"
    else:
        avatar = "🐉"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑🏻‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🐉"):
        g = client.chat.completions.create(model=model, stream=True, messages=st.session_state.messages)
        response = st.write_stream(g)
    st.session_state.messages.append({"role": "assistant", "content": response})
