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
def show_pdf(filep):
    # Open the given PDF file in binary read mode
    with open(filep, "rb") as f:
        # Read the binary content of the file, encode it in base64 and decode to UTF-8 string
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Create an HTML iframe that embeds the base64 PDF data so it can be displayed in the app
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Render the iframe inside the Streamlit app, allowing HTML rendering
    st.markdown(pdf_display, unsafe_allow_html=True)
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
        if pdff is not None:
            with st.spinner('Uploading your Resume..'):
                time.sleep(5)
            save_image_path='./Uploaded_Resume/'+pdff.name
            with open(save_image_path,"wb") as f:
                f.write(pdff.getbuffer())
            show_pdf(save_image_path)
            resumedata=ResumeParser(save_image_path).get_extracted_data()
            if resumedata:
                resumet=pdf_reader(save_image_path)

                st.header("**Resume Analysis**")
                st.success("Hello "+resumedata['name'])
                st.subheader("Your Basic info...:-")
                try:
                    st.text('Name: '+resumedata['name'])
                    st.text('Email: '+resumedata['email'])
                    st.text('Contact: '+resumedata['mobile_number'])
                    st.text('Resume Pages: '+str(resumedata['no_of_pages']))
                except:
                    pass
                candl=''
                if resumedata['no_of_pages']==1:
                    candl='Fresher'
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                elif resumedata['no_of_pages']==2:
                    candl='Intermediate'
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are at Intermediate level!</h4>''')
                elif resumedata['no_of_pages']>=3:
                    candl='Experienced'
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are at Experienced level!</h4>''')
                ##Now turn for skills
                keywords=st_tags(label="### Your Current Skills",text='See our skills recommendation below',value=resume_data['skills'],key='1')
                ##  keywords
                ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
                ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
                uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']
                # Here we have divided every skills as per their domain so that we can understand majorly for which role resume is made for
                recommended_skills=[]
                reco_field=''
                reco_course=''
                #Course Recommendation
                for i in resume_data['skills']:
                    #Data Science Recommendation
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        reco_field='Data Science'
                        st.success("**Our Analyses stats that your are Data Science Job**")
                        recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '2')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost the chances of getting a Job</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(ds_course)
                        break
                    ## Web development recommendation
                    elif i.lower() in web_keyword:
                        print(i.lower())
                        reco_field = 'Web Development'
                        st.success("** Our analysis says you are looking for Web Development Jobs **")
                        recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '3')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(web_course)
                        break

                    ## Android App Development
                    elif i.lower() in android_keyword:
                        print(i.lower())
                        reco_field = 'Android Development'
                        st.success("** Our analysis says you are looking for Android App Development Jobs **")
                        recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '4')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(android_course)
                        break

                    ## IOS App Development
                    elif i.lower() in ios_keyword:
                        print(i.lower())
                        reco_field = 'IOS Development'
                        st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                        recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '5')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(ios_course)
                        break

                    ## Ui-UX Recommendation
                    elif i.lower() in uiux_keyword:
                        print(i.lower())
                        reco_field = 'UI-UX Development'
                        st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                        recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '6')
                        st.markdown('''<h4 style='text-align: left; color: #1ed760;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        rec_course = course_recommender(uiux_course)
                        break
                    