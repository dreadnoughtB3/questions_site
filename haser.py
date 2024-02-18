import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['aizena3']).generate()
print(hashed_passwords)