import streamlit as st
import pandas as pd

def main():
    st.title("日曆型態顯示和訂位應用程式")

    # 創建一個範例的預定狀況數據框
    bookings_df = create_bookings_df()

    # 顯示日期選擇器
    selected_date = st.date_input("選擇日期", pd.Timestamp.today())

    # 顯示所選日期的預定狀況
    if selected_date:
        st.write(f"你選擇的日期是：{selected_date.date()}")
        booking_status = get_booking_status(bookings_df, selected_date)
        if booking_status:
            st.write("這一天已預定")
        else:
            if st.button("預訂"):
                book_date(bookings_df, selected_date)
                st.write("預訂成功！")

def create_bookings_df():
    # 創建一個範例的預定狀況數據框
    dates = pd.date_range(start="2024-03-01", end="2024-03-31")
    bookings = [False] * len(dates)  # 初始情況下都未預定
    bookings_df = pd.DataFrame({"Date": dates, "Booked": bookings})
    return bookings_df

def get_booking_status(bookings_df, selected_date):
    # 檢查所選日期的預定狀況
    selected_date_booking = bookings_df[bookings_df["Date"] == selected_date]
    if not selected_date_booking.empty:
        return selected_date_booking["Booked"].values[0]
    return False

def book_date(bookings_df, selected_date):
    # 將所選日期設置為已預定
    bookings_df.loc[bookings_df["Date"] == selected_date, "Booked"] = True

if __name__ == "__main__":
    main()
