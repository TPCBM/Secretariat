st.title('预订日历')

# 选择月份
selected_month = st.date_input("选择月份", datetime.today(), type="spinner")

# 创建日历
st.write(selected_month)

# 针对所选月份显示每天的预订情况
for i in range(1, 32):  # 假设每月最多有31天
    day = datetime(selected_month.year, selected_month.month, i)
    st.subheader(day.strftime("%Y-%m-%d"))

    # 添加预订表单
    reservation_name = st.text_input("输入您的姓名")
    reservation_email = st.text_input("输入您的邮箱")

    # 保存预订
    if st.button("提交预订"):
        st.success(f"预订成功！{day} - {reservation_name} - {reservation_email}")
        # 在这里可以将预订信息保存到数据库或其他地方
