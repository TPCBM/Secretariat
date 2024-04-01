import streamlit as st
from datetime import datetime, timedelta
def main():
    st.title('保安防護聯繫會議辦理情形填報表單')

    # 第一个问题
    question_1 = st.radio('1. 是否已召開保安防護聯繫會議?', ('是', '否'))

    # 根据第一个问题的回答显示不同的下一个问题
    if question_1 == '是':
        question_2 = st.date_input('2. 保安防護聯繫會議召開日期為?', datetime.today())
    else:
        question_3 = st.radio('3. 是否已「規劃」召開保安防護聯繫會議?', ('是', '否'))
        submitted = st.button('提交')
    
    # 根据第一个问题的回答显示不同的下一个问题
    if question_3 == '是':
        question_4 = st.date_input('4. 「規劃」保安防護聯繫會議召開日期為?', datetime.today())
    else:
        question_5 = st.text_input('5. 請說明尚未規劃保安防護聯繫會議之原因')

    submitted = st.button('提交')

    if submitted:
        # 显示收集到的数据
        st.write('感谢回答！')
        st.write(f'你喜欢编程吗？: {question_1}')
        if question_1 == '是':
            st.write(f'从事编程的时间: {question_2}')
        else:
            st.write(f'不喜欢编程的原因: {question_3}')

if __name__ == '__main__':
    main()
