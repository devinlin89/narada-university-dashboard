import streamlit as st

from dashboard.ui.cards import (
    page_header,
    vertical_spacer,
)
from dashboard.ui.layout import navigation_grid
from dashboard.ui.styles import load_css

load_css()


# Page header
page_header(
    title="About",
    description=(
        """
        An interactive dashboard presenting the university destinations,
        academic fields, majors, and admission outcomes of
        Narada Senior High School's Class of 2026.
        """
    ),
)

# About the Dashboard
st.markdown("## About the Dashboard")

st.write(
    """
    A few months before graduation, we surveyed students from
    Narada School's Class of 2026 about their post-graduation
    university destinations and academic choices. The survey collected
    information on students' committed university destinations,
    destination countries/regions, campuses, majors, academic fields,
    applications, admission outcomes, scholarships, and factors
    influencing their university decisions.

    **Narada University Dashboard** transforms these survey responses
    into an interactive dashboard for exploring the university
    destinations and academic pathways of the graduating class. Users
    can examine the geographic distribution of university destinations,
    analyze charts and statistics, and filter results by university,
    country/region, academic field, and major.

    We hope this dashboard provides a useful overview of the
    university destinations, countries/regions, academic fields, and majors
    represented within the Narada School Class of 2026.
    """
)

vertical_spacer()


st.subheader("What You Can Explore")
navigation_grid()


vertical_spacer()

# About the Data
st.markdown("## About the Data")

st.write(
    """
    The dashboard is based on self-reported responses collected through
    the Class of 2026 University Survey. The dataset represents students'
    reported university destinations and admissions information at the
    time the survey was conducted.

    Students may have applied to multiple universities, so application
    and offer statistics describe the admissions process rather than
    the number of enrolled students. University destination statistics,
    however, represent the destinations reported by students in the survey.
    """
)


vertical_spacer()

# Technology
st.markdown("## Technology")

st.write(
    """
    The dashboard is developed in Python using the libraries
    Pandas for data processing and transformation, Streamlit for the
    application interface, and Plotly for interactive data visualizations.
    Geographic data is processed using Geopy and OpenStreetMap-based
    geocoding services.
    """
)


vertical_spacer()

# Credits
st.markdown("## Created By")

st.write("This project was developed collaboratively by:")

st.markdown(
    """
    - **Devin Lin**
    - **Therius Aaron Chen**
    """
)

st.caption("AI development assistance: ChatGPT")

st.write("Special thanks to:")

st.markdown(
    """
    - **TBA**
    """
)