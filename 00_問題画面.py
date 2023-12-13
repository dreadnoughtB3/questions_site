# ページ1.pyの中に記載
import streamlit as st
import common

#ログインの確認
common.check_login()

# 以下にページの内容
st.text("ログイン成功")