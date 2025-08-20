import streamlit as st
import pandas as pd
import base64,random
#we use base64 to we need to read that pdf as binary to work with it 
import time,datetime

#Now Libraries to parse the resume pdf files
import nltk
nltk.download('stopwords')
#pyresparser is a library used to extract name,email mobile number, skills, total experience etc
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams,LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
#use to connect to the database
# from courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
import pafy #for uploading yt videos
import plotly.express as px #to create visualization to admin session


#connecting to the Database
connection=pymysql.connect(host='localhost',user='root',password='Kartik@#4279',db='airesumeanalyzer')
cursor=connection.cursor()
def insert_data(name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses):
    dbname='user_data'
    insql="INSERT INTO"+dbname+"""values(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values=(name,email,str(res_score),timestamp,str(no_of_pages),reco_field,cand_level,skills,recommended_skills,courses)
    cursor.execute(insql,rec_values)
    connection.commit()
# Here we are setting the webpage title and its icon
st.set_page_config(
    page_title='AI Resume Analyzer',
    page_icon='./Logo/logo3.png'
)
#Setting the actual page 
def run():
    img=Image.open('./Logo/logo3.png')
    st.image(img)
    st.title("AI Resume Analyzer")
    st.sidebar.markdown('# Choose User')
    activites=["User","Admin"]
    choice=st.sidebar.selectionbox("Choose among the given option:",activites)
    link='[Developed by Kartik Mehta](https://www.linkedin.com/in/mehta-kartik/)'
    st.sidebar.markdown(link,unsafe_allow_html=True)
    #create a database if not exist
    db_sql="""CREATE DATABASE IF NOT EXISTS airesumeanalyzer"""
    cursor.execute(db_sql)
    db_table_name='user_data'
    tablesql="CREATE TABLE IF NOT EXISTS"+db_table_name+"""(ID INT NOT NULL AUTO_INCREMENT,Name varchar(500) NOT NULL,
    EMAIL_ID VARCHAR(500) NOT NULL,
    resume_score varchar(8) NOT NULL,
    Timestamp varchar(50) NOT NULL,
    Page_no varchar(50) NOT NULL,
    Predicted_Field BLOB NOT NULL,
    User_level BLOB NOT NULL,
    Actual_skills BLOB NOT NULL,
    Recommended_skills BLOB NOT NULL,
    Recommended_courses BLOB NOT NULL,
    PRIMARY KEY (ID));"""
    cursor.execute(tablesql)
    if choice=='User':
        st.markdown('''<h4 style='text-align:left,color:#021659;'>Please Upload your resume to get smart recommendataion</h4>''',unsafe_allow_html=True)
        pdff=st.file_uploader("Choose your Resume",type=['pdf'])
