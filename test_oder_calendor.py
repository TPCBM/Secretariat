import streamlit as st
from datetime import datetime, timedelta

def main():
    st.title("日曆型態的訂位應用程式")

    # 選擇日期
    selected_date = st.date_input("選擇日期", datetime.today())

    # 選擇時間
    selected_time = st.time_input("選擇時間", datetime.now().time())

    # 選擇服務或項目
    service_options = ["中餐", "晚餐"]
    selected_service = st.selectbox("選擇服務或項目", service_options)

    # 顯示訂單摘要
    st.subheader("訂單摘要")
    st.write(f"日期: {selected_date}")
    st.write(f"時間: {selected_time}")
    st.write(f"服務或項目: {selected_service}")

if __name__ == "__main__":
    main()
