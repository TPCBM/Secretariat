import streamlit as st
import pandas as pd
import numpy as np

# 標題
st.title('儀表板範例')

# 加載數據
df = pd.DataFrame(
    np.random.randn(10, 3),
    columns=['A', 'B', 'C']
)

# 顯示數據表
st.subheader('數據表')
st.dataframe(df)

# 畫圖
st.subheader('折線圖')
st.line_chart(df)

# 篩選選項
option = st.selectbox(
    '選擇一個選項:',
    df.columns
)

st.write('你選擇了:', option)

# 顯示選擇的列
st.subheader(f'選擇的列：{option}')
st.line_chart(df[option])
