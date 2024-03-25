import streamlit as st
from streamlit-date-picker import st_datepicker

def main():
    st.title("日曆型態顯示和訂位應用程式")

    # 顯示日曆
    selected_date = st_datepicker("選擇日期")

    # 如果選擇了日期，顯示訂位按鈕
    if selected_date:
        st.write(f"你選擇的日期是: {selected_date}")
        st.write("請點選下方按鈕訂位")

        if st.button("訂位"):
            st.write("訂位成功！")

if __name__ == "__main__":
    main()
