import streamlit as st

from AutoCorrect import AutoCorrectWords

corps = AutoCorrectWords("data/shakespeare")

st.title("Autocorrector")
word = st.text_input('Enter a word')

if st.button("Correct"):
    correct_word = corps.get_correct_word(word)
    st.success(correct_word)
