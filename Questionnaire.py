import streamlit as st

def main():
    st.title('动态问卷')

    # 第一部分问题
    st.subheader('第一部分')
    name = st.text_input('1. 你的名字是什么？')

    # 根据第一个问题的答案决定是否显示第二部分问题
    if name:
        st.subheader('第二部分')
        age = st.slider('2. 你的年龄是多少？', min_value=0, max_value=100)

    # 根据第二个问题的答案决定是否显示第三部分问题
    if 'age' in locals() and age:
        st.subheader('第三部分')
        gender = st.selectbox('3. 你的性别是？', ['男', '女'])
        feedback = st.text_area('4. 你有什么反馈或建议？')

    submitted = st.button('提交')

    if submitted:
        # 将收集到的数据显示出来
        st.write('感谢回答！')
        st.write(f'名字: {name}')
        if 'age' in locals():
            st.write(f'年龄: {age}')
        if 'gender' in locals():
            st.write(f'性别: {gender}')
            st.write(f'反馈: {feedback}')

if __name__ == '__main__':
    main()
