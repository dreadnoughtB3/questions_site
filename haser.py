import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['basashi', 'herusere', '12f310d13t']).generate()
print(hashed_passwords)