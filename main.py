# streamlit_app.py
import json
import requests
import streamlit as st
import snowflake.connector
import codecs
from fastapi import FastAPI
from flask import Flask, redirect, url_for, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"], insecure_mode=True,)


def ingest_data_in_snowflake(feedback_data):
    conn = init_connection()
    cs = conn.cursor()
    try:
        cs.execute("insert into feedback values (feedback_data;")
        one_row = cs.fetchall()
        for i in one_row:
            print(i[0], i[1])
    finally:
        cs.close()
    conn.close()


def authorize_login(feedback_login_data):
    conn = init_connection()
    cs = conn.cursor()
    try:
        cs.execute(
            "select count(*) from employee_credentials where email='" + feedback_login_data['email'] + "' and pass= '" +
            feedback_login_data['password'] + "' ;")
        one_row = cs.fetchall()
        print(one_row)
    finally:
        cs.close()
    conn.close()
    return '400'



@app.route('/feedback',methods = ['POST'])
def feedback_form_data_ingestion():
    feedback_data=request.get_json()
    print(feedback_data)
    ingest_data_in_snowflake(feedback_data)
    return ''

@app.route('/login',methods = ['POST'])
def feedback_login():
    feedback_login_data=request.get_json()
    print(feedback_login_data);
    response_code=authorize_login(feedback_login_data);
    data={'response':response_code}
    return data


if __name__ == '__main__':
    app.run()



'''@app.post("/feedback")
def feedback_form_data_ingestion():
        feedback_data=request.get_json()
        print(type(feedback_data))'''

''''''


