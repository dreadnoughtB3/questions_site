import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['bravotango152']).generate()
print(hashed_passwords)