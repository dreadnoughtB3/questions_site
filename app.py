import streamlit as st
import streamlit_authenticator as stauth
import yaml
import datetime
import sqlite3
import json
import pandas as pd
from time import sleep
from yaml.loader import SafeLoader

with open('./config.yaml', 'rb') as file:
    config = yaml.load(file, Loader=SafeLoader)
questions = open('data/questions.json', 'r', encoding='utf8')
data = json.load(questions)
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

JST = datetime.timezone(datetime.timedelta(hours=9), 'JST')  
    
def get_db(query, param):
    global con, cur
    res = cur.execute(query, param)
    return res

def insert_db(query):
    global con, cur
    cur.execute(query)
    con.commit()
    
def update_db(query):
    global con, cur
    cur.execute(query)
    con.commit()
    
def get_current_time():
  global JST
  return str(datetime.datetime.now(JST))
    
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
  name = st.session_state["name"]
  st.write('*Created by mayonaka4355*')
  st.write(f'>ログイン中のユーザー：*{st.session_state["name"]}*')
  st.divider()
    
  if name == "mayonaka":
    st.write('管理者画面')
    dbdata = cur.execute('SELECT * from answers')
    st.dataframe(dbdata)
  else:
    user_progress = get_db('SELECT progress FROM user_progress WHERE username = ?', (st.session_state["name"],)).fetchone()[0]
    if user_progress < 5:
      question_body = data[str(user_progress)]["text"]
      st.write(f"> ◖問題 [{user_progress}/4]")
      st.write(question_body)
      inputText_A = st.text_input('回答記入欄',placeholder="回答")
      # 回答ボタンを入力した時
      if st.button("回答する"):
        if inputText_A:
          current_time = get_current_time()
          insert_db(f'INSERT INTO answers VALUES("{st.session_state["name"]}","{user_progress}問目","{inputText_A}","{current_time}")')
          if inputText_A == data[str(user_progress)]["answer"]:
            st.warning('正解')
            st.balloons()
            sleep(1)
            update_db(f'UPDATE user_progress SET progress = {user_progress + 1} WHERE username = "{st.session_state["name"]}"')
            sleep(2)
            st.rerun()
          else:
            st.warning('不正解')
            sleep(3)
    else:
      st.write("全問正解おめでとうございます。")
  authenticator.logout('ログアウト', 'main', key='unique_key')
        
# ユーザー名/パスワードが違う
elif st.session_state["authentication_status"] is False:
  st.error('ユーザー名かパスワードが間違っています')
# ログインしていない
elif st.session_state["authentication_status"] is None:
  st.warning('ユーザー名とパスワードを入力してください')