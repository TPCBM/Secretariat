import streamlit as st

import numpy as np
import pandas as pd
st.title('我的第一個應用程式')


with st.form(key='my_form'):
    form_name = st.text_input(label='姓名', placeholder='請輸入姓名')
    form_gender = st.selectbox('性別', ['男', '女', '其他'])
    form_birthday = st.date_input("生日")
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    st.write(f'hello {form_name}, 性別:{form_gender}, 生日:{form_birthday}')
