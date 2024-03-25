import streamlit as st
import pandas as pd

def main():
    st.title("日曆型態顯示和訂位應用程式")

    # 創建範例數據框
    df = create_example_dataframe()

    # 選擇日期
    selected_date = st.date_input("選擇日期", pd.Timestamp.today())

    # 顯示選擇日期的預定狀況
    st.write(f"日期：{selected_date.date()}")
    bookings = get_bookings_for_date(df, selected_date)
    st.write(bookings)

    # 如果日期可預訂，顯示預訂按鈕
    if not bookings:
        if st.button("預訂"):
            add_booking(df, selected_date)
            st.write("預訂成功！")

def create_example_dataframe():
    # 創建範例數據框
    dates = pd.date_range(start="2024-03-01", end="2024-03-31")
    data = {"Date": dates, "Bookings": [False] * len(dates)}
    df = pd.DataFrame(data)
    # 隨機添加一些預訂
    df.loc[3, "Bookings"] = True
    df.loc[10, "Bookings"] = True
    df.loc[15, "Bookings"] = True
    return df

def get_bookings_for_date(df, selected_date):
    # 檢查選擇日期的預定狀況
    bookings = df[df["Date"].dt.date == selected_date.date()]["Bookings"].values
    return bookings[0] if bookings else False

def add_booking(df, selected_date):
    # 將選擇日期設置為已預訂
    df.loc[df["Date"].dt.date == selected_date.date(), "Bookings"] = True

if __name__ == "__main__":
    main()
