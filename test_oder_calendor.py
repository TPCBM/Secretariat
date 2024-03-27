import streamlit as st
from datetime import datetime
import calendar

# 页面标题
st.title('餐厅订位系统')

# 选择月份
selected_month = st.selectbox("选择月份", [datetime.now().replace(month=i).strftime("%Y-%m") for i in range(1, 13)])

# 获取选择的年份和月份
year, month = map(int, selected_month.split("-"))

# 创建日历
days_in_month = calendar.monthrange(year, month)[1]

for i in range(1, days_in_month + 1):
    day = datetime(year, month, i)
    st.subheader(day.strftime("%Y-%m-%d"))

    # 添加预订表单
    reservation_name = st.text_input("输入您的姓名")
    reservation_contact = st.text_input("输入您的联系方式")

    # 保存预订
    if st.button("提交预订"):
        st.success(f"预订成功！日期：{day}, 姓名：{reservation_name}, 联系方式：{reservation_contact}")
        # 在这里可以将预订信息保存到数据库或其他地方
