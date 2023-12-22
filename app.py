import streamlit as st
import streamlit_authenticator as stauth
import yaml
import datetime
import pandas as pd
from time import sleep
from yaml.loader import SafeLoader

with open('./config.yaml', 'rb') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
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
    df = pd.read_csv("data/user.csv")
    df.set_index("id", inplace=True)
    name = st.session_state["name"]
    st.write('*Created by mayonaka4355*')
    st.write(f'>ログイン中のユーザー：*{st.session_state["name"]}*')
    st.divider()
    
    if name == "mayonaka":
        st.dataframe(df)
    elif name in df["name"].values:
        st.write("> `クリアおめでとうございます。`")
    else:
        st.write(f"> ◖問題 [1/1]")
        st.write("Question - AES256:\n  ```6DGSO+04IoF/JtKVCB3TPxykZ1qZkS9dWeJdPXNYI77lqvropOHbXnszhIpOhlEpDXN8vX+6s/eC/9kvASDTNpAx5dvo2BzpzQwENxew833221LvYloaUYdYbKIY8WeUAbfKh+ggD0TWmLEkH1TbpMmgfwKOYb/j0hGG+LHltmRzdAX+u1vPQdVS6ppFV11zLYm/jP+a83+DUz1Msd6OCQ==```")
        st.write("Hint: `K(C)aiser Andrew Jackson says: ᚢᚼᛆᛔᚵᛂᛆᚡᛂᚢᛍᚡᛔ-NOT=?`")
        st.write("**ドミニカ共和国(DOM) → エチオピア(ETH) → X → フランス(FRA)**")
        st.write("Hint: `G↑ P← I↓ T→ P← XVIII`")
        st.write("`0x:57 68 65 72 65 20 69 73 20 74 68 65 20 63 61 70 69 74 61 6c 20 63 69 74 79 20 6f 66 20 58 3f (a=61)`\n  `yhork>lhvfhnqmkxuccpfvlnufannspbu2dwV`")
        inputText_A = st.text_input('回答記入欄',placeholder="回答")
        # 回答ボタンを入力した時
        if st.button("回答する"):
            if inputText_A == "ivan":
                st.warning('正解')
                st.balloons()
                df.loc["0"] = [name,datetime.datetime.utcnow() + datetime.timedelta(hours=9)]
                df.to_csv('data/user.csv')
                sleep(3)
                st.rerun()
            else:
                st.warning('不正解')
                sleep(3)
    authenticator.logout('ログアウト', 'main', key='unique_key')
        
# ユーザー名/パスワードが違う
elif st.session_state["authentication_status"] is False:
    st.error('ユーザー名かパスワードが間違っています')
# ログインしていない
elif st.session_state["authentication_status"] is None:
    st.warning('ユーザー名とパスワードを入力してください')