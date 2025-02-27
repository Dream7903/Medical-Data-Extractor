import streamlit as st
import requests
from pdf2image import convert_from_bytes
import ast
import time
#import sqlite3

#conn = sqlite3.connect("database/data.db", check_same_thread=False)
#cur = conn.cursor()


POPPLER_PATH = r"D:\Release-24.08.0-0\poppler-24.08.0\Library\bin"
URL = "http://127.0.0.1:8000/extract_from_doc"

st.title("Medical Data Extractor")

file = st.file_uploader("Upload file", type="pdf")
col3, col4 = st.columns(2)
with col3:
    file_format = st.radio(label="Select type of document", options=["prescription", "patient_details"], horizontal=True)
with col4:
    if file and st.button("Upload PDF", type="primary"):
        bar = st.progress(50)
        time.sleep(3)
        bar.progress(100)
        payload = {'file_format': file_format}
        files = [('file', file.getvalue())]
        headers = {}
        response = requests.request("POST", URL, headers=headers, data=payload, files=files)
        dict_str = response.content.decode("utf-8")
        data = ast.literal_eval(dict_str)
        if data:
            st.session_state = data

#def addData(n,a,m,d,r):
    #cur.execute("""CREATE TABLE IF NOT EXISTS prescription(NAME TEXT(50), ADDRESS TEXT(50), MEDICINES TEXT(50), DIRECTIONS TEXT(50), REFILL TEXT(50))""")
    #cur.execute("INSERT INTO prescription VALUES(?,?,?,?,?)",(n,a,m,d,r))
    #conn.commit()
    #conn.close()
    #st.success("Details successfully recorded.")

if file:
    pages = convert_from_bytes(file.getvalue(), poppler_path=POPPLER_PATH)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your file")
        st.image(pages[0])

    with col2:
        if st.session_state:
            st.subheader("Details")
            if file_format == "prescription":
                name = st.text_input(label="Name", value=st.session_state["patient_name"])
                address = st.text_input(label="Address", value=st.session_state["patient_address"])
                medicines = st.text_input(label="Medicines", value=st.session_state["medicines"])
                directions = st.text_input(label="Directions", value=st.session_state["directions"])
                refill = st.text_input(label="Refill", value=st.session_state["refill"])
            if file_format == "patient_details":
                name = st.text_input(label="Name", value=st.session_state["patient_name"])
                phone = st.text_input(label="Phone No.", value=st.session_state["phone_no"])
                vacc_status = st.text_input(label="Hepatitis B vaccination status", value = st.session_state["vaccination_status"])
                med_problems = st.text_input(label="Medical Problems", value=st.session_state["medical_problems"])
                has_insurance = st.text_input(label="Does patient have insurance?", value=st.session_state["has_insurance"])
            if st.button(label="Submit", type="primary"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                #if file_format == "prescription":
                 #   addData(name,address,medicines,directions,refill)
                #if file_format == "patient_details":
                    #addData(name,phone,vacc_status,med_problems,has_insurance)
                st.success("Details successfully recorded.")

   

