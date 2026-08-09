import streamlit as st

from dashboard.ui.cards import page_header
from dashboard.ui.styles import load_css
from dashboard.ui.overview import explore_more 

load_css()


# Page header
page_header(
    title="About",
    description=(
        """
            Narada University Dashboard is an interactive platform created to
            visualize and explore the post-graduation plans of students from
            Narada School.
        
            A few months ago, we conducted a survey among our friends about their
            plans after graduation. The survey collected information about their
            destination countries, universities, intended majors, academic fields,
            and admission outcomes.
        
            We transformed these survey responses into an interactive dashboard
            so the results can be explored through maps, charts, statistics,
            and university profiles. """
    ),
)

explore_more()

st.write(" ")

# How It Works
st.markdown("## How It Works")

st.write(
    """
    The dashboard processes the survey data using Python and Pandas,
    then presents the results through interactive visualizations built
    with Streamlit and Plotly.

    Filters and selections dynamically update the displayed data,
    allowing users to explore the survey from different perspectives.
    """
)

st.write(" ")
# About the Data
st.markdown("## About the Data")

st.write(
    """
    The information shown on this dashboard reflects responses collected
    at the time of the survey. It represents students' reported
    applications, plans, and admission outcomes.

    An application or admission does not necessarily mean that a student
    ultimately enrolled at that institution. Students may also have
    applied to multiple universities.
    """
)

st.write(" ")
# Our Goal
st.markdown("## Our Goal")

st.write(
    """
    Our goal is to turn our university survey into an accessible and
    interactive way to explore the different paths students from
    Narada School are pursuing after graduation.

    We hope the dashboard provides a useful snapshot of the universities,
    countries, and academic fields represented in our community.
    """
)

st.write(" ")
# Credits
st.markdown("## Created By")
st.write(
    """
    This project was developed collaboratively by:
    """
)

st.markdown(
    """
    - Devin Lin
    - Therius Aaron Chen
    - ChatGPT
    """
)

