import streamlit as st
import streamlit_authenticator as stauth
import yaml
import json
import datetime
from time import sleep
from yaml.loader import SafeLoader

with open('./config.yaml', 'rb') as file:
    config = yaml.load(file, Loader=SafeLoader)
questions = json.load(open('data/questions.json', 'r', encoding="utf-8"))
user_data = json.load(open('data/user_data.json', 'r', encoding="utf-8"))
correct_answerer = json.load(open('data/correct_answerer.json', 'r', encoding="utf-8"))

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
    if questions_prog == 4:
        prog_text = "*COMPLETED*"
    else:
        prog_text = f"*{questions_prog}/3*"
    st.write('*Created by mayonaka4355*')
    st.write(f'>ログイン中のユーザー：*{st.session_state["name"]}*  \n>現在の問題進捗　　　：{prog_text}')
    st.divider()
    
    if questions_prog == 4:
        st.write("`全問題終了。イベント本番をお待ちください。`")
    elif st.session_state["name"] == "mayonaka":
        st.json(correct_answerer)
    else:
        st.write(f"> ◖問題[{questions_prog}/3]")
        question_data = questions["questions"][str(questions_prog)]
        st.write(question_data)
        
        inputText_A = st.text_input('回答記入欄',placeholder="回答")
        # 回答ボタンを入力した時
        if st.button("回答する"):
            if inputText_A == questions["answers"][str(questions_prog)]:
                user_data[st.session_state["name"]] += 1
                with open('data/user_data.json', 'w', encoding="utf-8") as f:
                    json.dump(user_data, f, indent=2, ensure_ascii=False)
                current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
                correct_answerer[str(questions_prog)][st.session_state["name"]] = {"name":st.session_state["name"], "date":str(current_time)}
                with open('data/correct_answerer.json', 'w', encoding="utf-8") as file:
                    sleep(1)
                    json.dump(correct_answerer, file, indent=2, ensure_ascii=False)
                st.warning('正解')
                st.balloons()
                sleep(2)
                st.rerun()
            else:
                st.warning('不正解')
        
# ユーザー名/パスワードが違う
elif st.session_state["authentication_status"] is False:
    st.error('ユーザー名かパスワードが間違っています')
# ログインしていない
elif st.session_state["authentication_status"] is None:
    st.warning('ユーザー名とパスワードを入力してください')