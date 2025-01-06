import streamlit as st
import pandas as pd
import pickle
import os

# --- Helper Functions ---
# Save data persistently
def save_data(data, filename="data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

# Load data from persistent storage
def load_data(filename="data.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return {}

# Export data to Excel
def export_to_excel(vacancy_name, data):
    df = pd.DataFrame(data["checkboxes"], index=data["criteria"], columns=data["candidates"])
    df.index.name = "Criteria/Most Important Things"
    excel_file = f"{vacancy_name}.xlsx"
    df.to_excel(excel_file)
    return excel_file

# --- Initialize Data ---
data = load_data()
if not data:
    data["Vacancy example 1"] = {"criteria": ["example"], "candidates": ["Candidate 1"], "checkboxes": [[False]]}

# --- Sidebar: Vacancy Management ---
st.sidebar.title("Vacancy Dropdown")
vacancies = list(data.keys())
selected_vacancy = st.sidebar.selectbox("Select a Vacancy", vacancies)

# Add New Vacancy
st.sidebar.subheader("Add Vacancy")
new_vacancy = st.sidebar.text_input("Enter New Vacancy Name")
if st.sidebar.button("Add Vacancy") and new_vacancy:
    if new_vacancy not in data:
        data[new_vacancy] = {"criteria": [], "candidates": [], "checkboxes": []}
        save_data(data)
        st.experimental_rerun()

# --- Main Section: Vacancy Table ---
st.title(f"Vacancy: {selected_vacancy}")

# Get selected vacancy data
vacancy_data = data[selected_vacancy]

# Display Table Header
st.write("### Criteria/Most Important Things vs Candidates")
if vacancy_data["criteria"] and vacancy_data["candidates"]:
    # Create a DataFrame for display
    df_display = pd.DataFrame(vacancy_data["checkboxes"], index=vacancy_data["criteria"], columns=vacancy_data["candidates"])
    df_display.index.name = "Criteria/Most Important Things"
    
    # Render checkboxes dynamically
    for i, criterion in enumerate(vacancy_data["criteria"]):
        cols = st.columns(len(vacancy_data["candidates"]) + 1)
        cols[0].write(criterion)  # Criterion name
        for j, candidate in enumerate(vacancy_data["candidates"]):
            checked = cols[j + 1].checkbox("", value=vacancy_data["checkboxes"][i][j], key=f"{selected_vacancy}_{i}_{j}")
            vacancy_data["checkboxes"][i][j] = checked

# --- Add New Criteria ---
st.write("### Add Criteria")
new_criterion = st.text_input("Enter a new criterion")
if st.button("Add Criterion"):
    if new_criterion and new_criterion not in vacancy_data["criteria"]:
        vacancy_data["criteria"].append(new_criterion)
        # Add a new row of checkboxes (False by default)
        vacancy_data["checkboxes"].append([False] * len(vacancy_data["candidates"]))
        save_data(data)
        st.experimental_rerun()

# --- Add New Candidates ---
st.write("### Add Candidate")
new_candidate = st.text_input("Enter a new candidate")
if st.button("Add Candidate"):
    if new_candidate and new_candidate not in vacancy_data["candidates"]:
        vacancy_data["candidates"].append(new_candidate)
        # Add a new column of checkboxes (False by default)
        for row in vacancy_data["checkboxes"]:
            row.append(False)
        save_data(data)
        st.experimental_rerun()

# --- Download Data as Excel ---
st.write("### Download Data")
if st.button("Download in Excel"):
    excel_file = export_to_excel(selected_vacancy, vacancy_data)
    with open(excel_file, "rb") as f:
        st.download_button(label="Download Excel File", data=f, file_name=excel_file)

# Save updated data at the end of execution
save_data(data)
