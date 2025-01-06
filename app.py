import streamlit as st
import pandas as pd
import pickle
import os

# --- Helper Functions ---
# Save data to a file
def save_data(data, filename="data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

# Load data from a file
def load_data(filename="data.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return {}

# Initialize data storage
data = load_data()

# --- Sidebar: Role Selection ---
st.sidebar.title("Job Roles")
roles = list(data.keys())
selected_role = st.sidebar.selectbox("Select a Role", ["Add New Role"] + roles)

if selected_role == "Add New Role":
    # Add a new role
    st.sidebar.subheader("Add a New Role")
    new_role = st.sidebar.text_input("Enter Role Name")
    if st.sidebar.button("Create Role") and new_role:
        if new_role not in data:
            data[new_role] = {"criteria": [], "candidates": []}
            save_data(data)
            
            # Update query parameters to reflect the new role
            st.query_params["role"] = new_role
            st.rerun()  # Refresh the app to load the new role

else:
    # Main App for Selected Role
    st.title(f"Role: {selected_role}")

    # --- Add Criteria Section ---
    st.subheader("Job Qualification Criteria")
    criteria_input = st.text_input("Add a New Criterion", key="criteria_input")
    if st.button("Add Criterion"):
        if criteria_input and criteria_input not in data[selected_role]["criteria"]:
            data[selected_role]["criteria"].append(criteria_input)
            save_data(data)
            st.rerun()  # Refresh the app to update the criteria list

    # Display existing criteria
    if data[selected_role]["criteria"]:
        st.write("### Current Criteria:")
        for criterion in data[selected_role]["criteria"]:
            st.write(f"- {criterion}")

    # --- Add Candidates Section ---
    st.subheader("Candidates")
    candidate_input = st.text_input("Add a New Candidate", key="candidate_input")
    if st.button("Add Candidate"):
        if candidate_input and candidate_input not in data[selected_role]["candidates"]:
            data[selected_role]["candidates"].append(candidate_input)
            save_data(data)
            st.rerun()  # Refresh the app to update the candidate list

    # Display existing candidates
    if data[selected_role]["candidates"]:
        st.write("### Current Candidates:")
        for candidate in data[selected_role]["candidates"]:
            st.write(f"- {candidate}")

    # --- Comparison Table ---
    if data[selected_role]["criteria"] and data[selected_role]["candidates"]:
        st.subheader("Comparison Table")

        # Create a DataFrame for the table
        criteria = data[selected_role]["criteria"]
        candidates = data[selected_role]["candidates"]
        table_data = {
            criterion: [
                st.checkbox(
                    f"{criterion} - {candidate}",
                    key=f"{selected_role}_{criterion}_{candidate}",
                )
                for candidate in candidates
            ]
            for criterion in criteria
        }

        # Optional: Convert to DataFrame (for display or further logic)
        df = pd.DataFrame(table_data, index=candidates).T
        st.dataframe(df)

# Save updated data at the end of execution
save_data(data)
