# Strokes Gained Dashboard

## Technologies Used

<div style="display: flex; justify-content: space-between;">
  <img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" width="30%">
  <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width="30%">
  <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-lighttext.png" width="30%">
</div>

<img src="https://raw.githubusercontent.com/pola-rs/polars-static/master/logos/polars_github_logo_rect_dark_name.svg">

## Data Techniques
- Developed PostgreSQL database, extracting PGATour data using a custom webscraper
- Built Django API to make calling data from database easier and more accessible
- Used Polars to select, clean and filter data to create the visulaizations i wanted
    - I found that polars code is very clean looking and allows for better code while being much faster
- Grouping and aggregation to form visualizations
- Web app development using Streamlit, ensuring user can interact with data to gain insights on their favorite players

## What I Learned
- Using django I learned the inner workings of django andf how API's work in general, also how they interact with an application
- How a SQL database and an API can interact and allow a user to make an http request to receive JSON data
- The Polars library, I come from a strong pandas background and was facinated at how fast and clean Polars code is
- How an API and a web application can work together to receive data while caching data where needed
