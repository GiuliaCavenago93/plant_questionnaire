import streamlit as st
import pandas as pd
from datetime import datetime

# Load the Excel file
questions_df = pd.read_excel("questions.xlsx")

st.set_page_config(page_title="Plant Operator Questionnaire", layout="centered")
st.title("🌿 Plant Operator Data Collection Form")

# Container for responses
responses = {}

# Group by section
sections = questions_df['Section'].dropna().unique()

with st.form("plant_data_form"):
    for section in sections:
        st.subheader(f"Section {int(section)}")
        section_questions = questions_df[questions_df['Section'] == section]

        for _, row in section_questions.iterrows():
            question = row['Question']
            input_type = str(row['Input Type']).lower()
            options = [opt.strip() for opt in str(row['optuons']).split(',')] if pd.notna(row['optuons']) else []
            unit_options = [u.strip() for u in str(row['Unit Options']).split(',')] if pd.notna(row['Unit Options']) else []

            if input_type == "dropdown":
                responses[question] = st.selectbox(question, options)
            elif input_type == "number input":
                responses[question] = st.number_input(question, step=0.01)
            elif input_type == "text":
                responses[question] = st.text_input(question)
            elif input_type == "text area":
                responses[question] = st.text_area(question)
            else:
                st.warning(f"⚠️ Unknown input type for: {question}")

            # Ask for unit if unit options exist
            if unit_options and len(unit_options) > 0 and unit_options[0] != "(no unit)":
                unit_question = f"{question} - Unit"
                responses[unit_question] = st.selectbox(unit_question, unit_options)

    submitted = st.form_submit_button("Submit")

# Save responses to Excel if submitted
if submitted:
    output_df = pd.DataFrame([responses])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"response_{timestamp}.xlsx"
    output_df.to_excel(output_file, index=False)
    st.success(f"✅ Responses saved to: {output_file}")
