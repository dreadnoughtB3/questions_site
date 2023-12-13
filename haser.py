import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['test1', 'test1']).generate()
print(hashed_passwords)