import streamlit as st

st.title(" 🤺 Head2Head PFA Rankings Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("pages/images/womens_epee.jpg", use_container_width=True)
    if st.button("Women's Epee", use_container_width=True):
        st.switch_page("pages/01_Women's_Epee.py")

with col2:
    st.image("pages/images/mens_epee.jpg", use_container_width=True)
    if st.button("Men's Epee", use_container_width=True):
        st.switch_page("pages/02_Men's_Epee.py")


with col3:
    st.image("pages/images/mens_epee.jpg", use_container_width=True)
    if st.button("Men's Epee", use_container_width=True):
        st.switch_page("pages/02_Men's_Epee.py")

col4, col5, col6 = st.columns(3)

with col4:
    st.image("pages/images/womens_epee.jpg", use_container_width=True)
    if st.button("Women's Epee", use_container_width=True):
        st.switch_page("pages/01_Women's_Epee.py")

with col5:
    st.image("pages/images/mens_epee.jpg", use_container_width=True)
    if st.button("Men's Epee", use_container_width=True):
        st.switch_page("pages/02_Men's_Epee.py")


with col6:
    st.image("pages/images/mens_epee.jpg", use_container_width=True)
    if st.button("Men's Epee", use_container_width=True):
        st.switch_page("pages/02_Men's_Epee.py")