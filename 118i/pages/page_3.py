import streamlit as st
import datetime
import os
import json
from collections import Counter
import pandas as pd
import openai
from openai import OpenAI
import unicodedata

#files 
REPORT_FILE = "reports.json"
SYNTHETIC_CSV = os.path.join(os.path.dirname(__file__), "data", "Data.csv")



# Load any real reports if available before implementing synthetic data
if os.path.exists(REPORT_FILE):
    with open(REPORT_FILE, "r") as f:
        real_reports = json.load(f)
else:
    real_reports = []

# adding synthetic data
if os.path.exists(SYNTHETIC_CSV):
    df_synthetic = pd.read_csv(SYNTHETIC_CSV)
    synthetic_reports = df_synthetic.to_dict(orient="records")
else:
    synthetic_reports = []

# Combine both datasets
reports = synthetic_reports + real_reports

#counting reports per district
district_counts = Counter([r["district"] for r in reports]) #counter for reports per district
for d in ["District 1", "District 2", "District 3"]: #make sure all the districts are shown, even if the count of a district is 0
    if d not in district_counts:
        district_counts[d] = 0


st.title("Water Quality Reports")

st.subheader("Report Count by District") #header for the chart that shows count of districts reported
st.bar_chart(district_counts) #the bar chart that has the distrcit counters

#AI
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI()

district_texts = {"District 1": "", "District 2": "", "District 3": ""}
for report in reports:
    district_texts[report["district"]] += report["text"] + " "

district_summary = "\n".join([
    f"{district} — {district_counts[district]} reports\nReported issues: {district_texts[district].strip()}"
    for district in ["District 1", "District 2", "District 3"]
])
prompt = (
    "Below is a summary of water quality reports grouped by district. Each district includes the total number of reports and example reported issues:\n\n"
    f"{district_summary}\n\n"
    "Based on both the number and content of these reports, provide concise insights into each district's water quality. "
    "Highlight recurring concerns, unusual patterns, and areas that may need urgent attention.\n\n"
    "Structure the response clearly, using bullet points per district. Keep it brief and user-friendly — 3-4 bullets per district at most."
)

def ascii_safe(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

def get_completion(prompt, model="gpt-3.5-turbo"):
    safe_prompt = ascii_safe(prompt)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": safe_prompt},
            {"role": "user", "content": safe_prompt},
        ]
    )
    return completion.choices[0].message.content

st.subheader("AI-Generated Insights")
st.write(get_completion(prompt))



#displaying reports from reports, backwards (recent)
if reports:  #if reports has any reports
    for i in range(len(reports) - 1, -1, -1):  #looping through reports backwards #make sure to reference index 
        report = reports[i]
        with st.container():  #just a visual container around the report before displaying it
            st.markdown(f"Area: {report['district']}")  #Displays the district from the report and makes it bold
            st.markdown(f"UserReport: {report['text']}") #displays the text
            st.markdown(f"Date Submitted: {report['date']}") #displays the date
            st.markdown("---") #just a visual horizontal line
        #allowing deletes only on real reports
        if i>= len(synthetic_reports):
            delete_button = st.button("Delete", key=f"delete{i}") #creates a delete button by the report
            if delete_button: #if the button is clicked
                real_index = i - len(synthetic_reports) #setting the index
                real_reports.pop(real_index) # removing
                with open(REPORT_FILE, "w") as f: #(then we open the main report file again) ("w" means write mode, so we can modify it)
                    json.dump(real_reports, f, indent=4) #writes the new list of reports (after deletion)
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
    real_reports.append(new_report) #adding the new report to reports
    with open(REPORT_FILE, "w") as f:# open the main reports file (with is there to handle opening and closing file)
        json.dump(real_reports, f, indent=4) #writes the updated reports list to the JSON file. indent for visuals.
    st.success("Report submitted successfully.") #Report has been submitted
    st.rerun() #reruns the program for the user with the updated report
