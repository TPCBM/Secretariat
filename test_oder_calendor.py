import streamlit as st
from streamlit_datetime_range_picker import datetime_range_picker

# Use datetime_range_picker to create a datetime range picker
datetime_string = datetime_range_picker(start=-30, end=0, unit='minutes', key='range_picker', 
                                        picker_button={'is_show': True, 'button_name': 'Refresh last 30min'})
if datetime_string is not None:
    start_datetime = datetime_string[0]
    end_datetime = datetime_string[1]
