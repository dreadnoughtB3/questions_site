import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['21dj3013']).generate()
print(hashed_passwords)