import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.ui.cards import page_header
from dashboard.ui.styles import load_css

data = load_dashboard_data()

load_css()

page_header(
title="About",
description=(
'''
    Narada University Dashboard is an interactive platform created to visualize the post-graduation destinations of students from Narada School.

    A few months ago, we conducted a survey among our friends to learn more about their plans after graduation. The survey collected information such as their destination country, university or institution, intended major, and admission status. Rather than keeping the results as a simple dataset, we decided to turn the information into an interactive dashboard that makes the data easier to explore and understand.

    The dashboard features an interactive world map that visualizes where students are planning to continue their education, allowing users to explore destinations around the world. It also provides insights into universities, countries, majors, academic fields, and admission outcomes, giving a broader picture of the different paths students are taking after graduation.

    Our goal is to provide a simple and engaging way for students to explore these results, discover common destinations, and gain a better understanding of the different opportunities their peers are pursuing after Narada School.
'''
)

)
