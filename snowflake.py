# streamlit_app.py

import streamlit as st
import snowflake.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.

def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT email from employee_credentials;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")