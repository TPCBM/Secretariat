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

# 使用側邊欄來選擇選項
option = st.sidebar.selectbox(
    '選擇一個選項:',
    df.columns
)
st.sidebar.write('你選擇了:', option)

# 使用 st.columns 來佈局
col1, col2 = st.columns(2)

# 顯示數據表在第一列
with col1:
    st.subheader('數據表')
    st.dataframe(df)

# 顯示折線圖和選擇框在第二列
with col2:
    st.subheader('折線圖')
    st.line_chart(df)

    # 顯示選擇的列
    st.subheader(f'選擇的列：{option}')
    st.line_chart(df[option])

# 使用 expander 折疊部分內容
with st.expander("查看詳細數據"):
    st.write("這裡可以放一些詳細數據或分析報告。")
