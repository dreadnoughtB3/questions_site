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
    if questions_prog == 11:
        prog_text = "*COMPLETED*"
    else:
        prog_text = f"*{questions_prog}/10*"
    st.write('*Created by mayonaka4355*')
    st.write(f'>ログイン中のユーザー：*{st.session_state["name"]}*  \n>現在の問題進捗　　　：{prog_text}')
    st.divider()
    
    if st.session_state["name"] == "mayonaka":
        st.json(correct_answerer)
        
        json_string_1 = json.dumps(correct_answerer, indent=2, ensure_ascii=False)
        json_string_2 = json.dumps(user_data, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="correct_answerer.json",
            file_name="correct_answerer.json",
            mime="application/json",
            data=json_string_1,
        )
        st.download_button(
            label="user_data.json",
            file_name="user_data.json",
            mime="application/json",
            data=json_string_2,
        )
        try:
            if authenticator.register_user('ユーザー追加', preauthorization=False):
                with open('./config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)
        new_user_name = st.text_input('新規ユーザー名')
        if st.button("追加"):
            if new_user_name in user_data:
                st.warning("既にユーザー名が登録されています")
            else:
                user_data[new_user_name] = 1
                print(user_data)
                with open('data/user_data.json', 'w', encoding="utf-8") as f:
                    json.dump(user_data, f, indent=2, ensure_ascii=False)
        
    elif questions_prog == 11:
        st.write("`全問題終了。お疲れさまでした。`")
    else:
        st.write(f"> ◖問題[{questions_prog}/10]")
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