import streamlit as st
import datetime
import os
import json
from collections import Counter

#file where user reports will be stored
REPORT_FILE = "reports.json"


#this will load existing reports, (we create a list to be able to store multiple reports)
if os.path.exists(REPORT_FILE):
    with open(REPORT_FILE, "r") as f:
        reports = json.load(f)
else:
    reports = []

district_counts = Counter([r["district"] for r in reports]) #counter for reports per district
for d in ["District 1", "District 2", "District 3"]: #make sure all the districts are shown, even if the count of a district is 0
    if d not in district_counts:
        district_counts[d] = 0




st.title("Water Quality Reports")

st.subheader("Report Count by District") #header for the chart that shows count of districts reported
st.bar_chart(district_counts) #the bar chart that has the distrcit counters

#displaying reports from reports, backwards (recent)
if reports:  #if reports has any reports
    for i in range(len(reports) - 1, -1, -1):  #looping through reports backwards #make sure to reference index 
        report = reports[i]
        with st.container():  #just a visual container around the report before displaying it
            st.markdown(f"Area: {report['district']}")  #Displays the district from the report and makes it bold
            st.markdown(f"UserReport: {report['text']}") #displays the text
            st.markdown(f"Date Submitted: {report['date']}") #displays the date
            st.markdown("---") #just a visual horizontal line
        delete_button = st.button("Delete", key=f"delete{i}") #creates a delete button by the report
        if delete_button: #if the button is clicked
            reports.pop(i) #we reports (remove using the stack function)
            with open(REPORT_FILE, "w") as f: #(then we open the main report file again) ("w" means write mode, so we can modify it)
                json.dump(reports, f, indent=4) #writes the new list of reports (after deletion)
            st.rerun() #instantly rerns the streamlit app so we can see it delted

        st.markdown("---")
else:   #if reports is empty, it will say there are no reports
    st.info("No reports yet.")

st.subheader("Submit a New Report") #sub header

with st.form("report_form"):# creating an "input block", inputs won't take action until report has been submitted
    #drop down with district options
    district = st.selectbox("District", ["District 1", "District 2", "District 3"], index=None, placeholder="Select a district...")
    text = st.text_input("Describe the issue") #statement for the issue
    submitted = st.form_submit_button("Submit") #when submitted, saves as a variable

if submitted and district and text: #now if those three inputs have been triggered

    new_report = { #create a dictionary to store the new report
        "district": district, #mapping the dictionary
        "text": text,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    reports.append(new_report) #adding the new report to reports

    with open(REPORT_FILE, "w") as f:# open the main reports file (with is there to handle opening and closing file)
        json.dump(reports, f, indent=4) #writes the updated reports list to the JSON file. indent for visuals.

    st.success("Report submitted successfully.") #Report has been submitted

    st.rerun() #reruns the program for the user with the updated report
