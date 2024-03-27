import streamlit as st
import calendar
from datetime import datetime

reservations = pd.DataFrame()
# Sample data
reservations["2023-12-01"] = ["John Doe", "10:00 AM"]
reservations["2023-12-15"] = ["Jane Doe", "2:00 PM"]
# Get user input
selected_month, selected_year = st.date_input("Select Month", datetime.now())

# Iterate through days
for day in range(1, calendar.monthrange(selected_year, selected_month)[1] + 1):
    date_str = f"{selected_year}-{selected_month:02d}-{day:02d}"
    
    # Display day number and reservation details
    st.write(f"{day:02d}")
    if date_str in reservations:
        for reservation in reservations[date_str]:
            st.write(f"- {reservation}")
    else:
        st.write("- No reservations")
