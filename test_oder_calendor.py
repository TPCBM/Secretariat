import streamlit as st
from datetime import datetime
st.title('餐厅订位系统')

# 选择月份
selected_month = st.date_input("选择月份", datetime.today().replace(day=1), type="spinner")

# 创建日历
days_in_month = calendar.monthrange(selected_month.year, selected_month.month)[1]
