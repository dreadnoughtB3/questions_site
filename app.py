import streamlit as st
import streamlit_authenticator as stauth
import yaml
import json
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
questions = json.load(open('data/questions.json', 'r'))
user_data = json.load(open('data/user_data.json', 'r'))

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
st.header(body="◍STELLARIA CHRONICLE",divider="grey")
authenticator.login('ログイン', 'main')

# ログイン済み
if st.session_state["authentication_status"]:
    questions_prog = user_data[st.session_state["name"]]
    st.write('*Created by mayonaka4355*')
    st.write(f'>ログイン中のユーザー：*{st.session_state["name"]}*  \n>現在の問題進捗　　　：*{questions_prog}/6*')
    st.divider()
    
    st.write(f"> ◖問題[{questions_prog}/6]")
    question_data = questions[str(questions_prog)]
    st.write(question_data)
    
    inputText_A = st.text_input('回答記入欄')
    st.button("回答する")
# ユーザー名/パスワードが違う
elif st.session_state["authentication_status"] is False:
    st.error('ユーザー名かパスワードが間違っています')
# ログインしていない
elif st.session_state["authentication_status"] is None:
    st.warning('ユーザー名とパスワードを入力してください')