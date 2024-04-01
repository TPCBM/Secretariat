import streamlit as st
from datetime import datetime

def main():
    st.title('保安防護聯繫會議辦理情形填報表單')

    # 第一个问题
    question_1 = st.radio('1. 是否已召開保安防護聯繫會議?', ('是', '否'))

    if question_1 == '是':
        # 如果已召开会议，则显示第二个问题：召开日期
        question_2 = st.date_input('2. 保安防護聯繫會議召開日期為?', datetime.today())
    else:
        # 如果未召开会议，则显示第三个问题：是否已规划召开会议
        question_3 = st.radio('3. 是否已「規劃」召開保安防護聯繫會議?', ('是', '否'))
        if question_3 == '是':
            # 如果已规划召开会议，则显示第四个问题：规划的会议召开日期
            question_4 = st.date_input('4. 「規劃」保安防護聯繫會議召開日期為?', datetime.today())
        else:
            # 如果未规划召开会议，则显示第五个问题：未规划原因
            question_5 = st.text_input('5. 請說明尚未規劃保安防護聯繫會議之原因')

    submitted = st.button('提交')

    if submitted:
        # 显示收集到的数据
        st.write('感谢回答！')
        st.write(f'是否已召開保安防護聯繫會議: {question_1}')
        if question_1 == '是':
            st.write(f'保安防護聯繫會議召開日期: {question_2}')
        else:
            st.write(f'是否已「規劃」召開保安防護聯繫會議: {question_3}')
            if question_3 == '是':
                st.write(f'「規劃」保安防護聯繫會議召開日期: {question_4}')
            else:
                st.write(f'尚未規劃保安防護聯繫會議之原因: {question_5}')

if __name__ == '__main__':
    main()
