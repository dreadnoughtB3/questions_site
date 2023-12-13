import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['F95Fs4hTyCwd']).generate()
print(hashed_passwords)