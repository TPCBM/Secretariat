import streamlit as st
from datetime import datetime, timedelta
st.image(
            "https://s3-us-west-2.amazonaws.com/uw-s3-cdn/wp-content/uploads/sites/6/2017/11/04133712/waterfall.jpg",
            width=400, # Manually Adjust the width of the image as per requirement
        )
def main():
    st.title("勵進餐廳訂位系統")

    # 選擇日期
    selected_date = st.date_input("選擇日期", datetime.today())

    # 選擇時間
    # selected_time = st.time_input("選擇時間", datetime.now().time())

    # 選擇服務或項目
    service_options = ["中餐", "晚餐"]
    selected_service = st.selectbox("選擇服務或項目", service_options)

    # 顯示訂單摘要
    st.subheader("訂單摘要")
    st.write(f"日期: {selected_date}")
    # st.write(f"時間: {selected_time}")
    st.write(f"服務或項目: {selected_service}")

    # 如果選擇了日期，顯示訂位按鈕
    if selected_date:
        st.write(f"你選擇的日期是: {selected_date}")
        st.write("請點選下方按鈕訂位")

        if st.button("訂位"):
            st.write("訂位成功！")


if __name__ == "__main__":
    main()
