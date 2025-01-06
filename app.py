import streamlit as st
import pandas as pd
import pickle
import os

# Function to save data to a file
def save_data(data, filename="data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

# Function to load data from a file
def load_data(filename="data.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return {}

# Load saved data
data = load_data()

# Sidebar: Select or Add a Role
st.sidebar.title("Vacancies")
roles = list(data.keys())
selected_role = st.sidebar.selectbox("Select a Role", ["Add New Role"] + roles)

if selected_role == "Add New Role":
    new_role = st.sidebar.text_input("Enter Role Name")
    if st.sidebar.button("Add Role") and new_role:
        if new_role not in data:
            data[new_role] = {"criteria": [], "candidates": []}
            save_data(data)
            st.experimental_rerun()
else:
    # Main App for Selected Role
    st.title(f"Role: {selected_role}")
    
    # Add Criteria Section
    st.subheader("Job Qualification Criteria")
    criteria_input = st.text_input("Add a new criterion")
    if st.button("Add Criterion") and criteria_input:
        if criteria_input not in data[selected_role]["criteria"]:
            data[selected_role]["criteria"].append(criteria_input)
            save_data(data)
            st.experimental_rerun()

    # Add Candidates Section
    st.subheader("Candidates")
    candidate_input = st.text_input("Add a new candidate")
    if st.button("Add Candidate") and candidate_input:
        if candidate_input not in data[selected_role]["candidates"]:
            data[selected_role]["candidates"].append(candidate_input)
            save_data(data)
            st.experimental_rerun()

    # Display Criteria and Candidates Table with Checkboxes
    if data[selected_role]["criteria"] and data[selected_role]["candidates"]:
        st.subheader("Comparison Table")
        
        # Create a DataFrame for checkboxes
        criteria = data[selected_role]["criteria"]
        candidates = data[selected_role]["candidates"]
        table_data = {
            criterion: [st.checkbox("", key=f"{selected_role}_{criterion}_{candidate}") 
                        for candidate in candidates]
            for criterion in criteria
        }
        
        # Convert to DataFrame for display (optional)
        df = pd.DataFrame(table_data, index=candidates).T
        st.dataframe(df)

# Save updated data on exit
save_data(data)
