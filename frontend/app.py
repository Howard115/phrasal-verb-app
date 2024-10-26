import streamlit as st
import requests
import pandas as pd

# Constants
BACKEND_URL = "http://localhost:8000"  # Backend API endpoint
INITIAL_TABLE_DATA = [
    ["", "phrasal verb", "meaning", "example"],
    ["Row 1", "", "", ""],
    ["Row 2", "", "", ""],
    ["Row 3", "", "", ""]
]

# State management
def init_session_state():
    if 'table_data' not in st.session_state:
        st.session_state.table_data = INITIAL_TABLE_DATA
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""

def update_table(row_index, new_data):
    """Update table data at specified row with new data"""
    st.session_state.table_data[row_index] = [f"Row {row_index}"] + new_data

# Data fetching
def fetch_random_phrasal_verb():
    """Fetch random phrasal verb from backend API"""
    try:
        response = requests.get(f"{BACKEND_URL}/random-phrasal-verb")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: Unable to fetch data. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        st.error(f"Error: {str(e)}")
        return None

def fetch_nouns_for_sentence():
    """Fetch nouns for sentence making from backend API"""
    phrasal_verbs = [row[1] for row in st.session_state.table_data[1:] if row[1]]
    try:
        response = requests.post(f"{BACKEND_URL}/getNounForMakeSentence", json={"phrasal_verbs": phrasal_verbs})
        if response.status_code == 200:
            return response.json()["nouns"]
        else:
            st.error(f"Error: Unable to fetch nouns. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        st.error(f"Error: {str(e)}")
        return None

# UI Components
def create_dataframe():
    """Create pandas DataFrame from table data"""
    df = pd.DataFrame(st.session_state.table_data[1:], columns=st.session_state.table_data[0])
    df.set_index(df.columns[0], inplace=True)
    return df

def render_gen_buttons():
    """Render generation buttons"""
    for i in range(1, 4):
        if st.button(f"Gen {i}", key=f"gen_button_{i}"):
            data = fetch_random_phrasal_verb()
            if data:
                update_table(i, [data['phrasal_verb'], data['meaning'], data['example']])

def set_api_key(api_key):
    """Set API key in the backend"""
    try:
        response = requests.post(f"{BACKEND_URL}/set-api-key", json={"api_key": api_key})
        if response.status_code == 200:
            st.success("API key set successfully")
            st.session_state.api_key = api_key
        else:
            st.error(f"Error: Unable to set API key. Status code: {response.status_code}")
    except requests.RequestException as e:
        st.error(f"Error: {str(e)}")

# Main app
def main():
    st.title("Phrasal Verb Learning App")
    
    init_session_state()

    # API Key Input
    api_key = st.text_input("Enter your OpenAI API key:", value=st.session_state.api_key, type="password")
    if st.button("Set API Key"):
        set_api_key(api_key)

    # Section 1: Phrasal Verb Generation
    st.header("1. Generate Phrasal Verbs")
    col1, col2 = st.columns([1, 5])
    
    with col1:
        render_gen_buttons()
    
    with col2:
        df = create_dataframe()
        st.table(df)

    # Divider
    st.divider()

    # Section 2: Noun Generation for Sentence Making
    st.header("2. Generate Nouns for Sentence Making")
    if st.button("Generate Nouns"):
        nouns = fetch_nouns_for_sentence()
        if nouns:
            st.success("Nouns generated successfully!")
            st.write("Use these nouns to make sentences with the phrasal verbs above:")
            st.write(", ".join(nouns))
        else:
            st.warning("Please generate at least one phrasal verb before generating nouns.")

if __name__ == "__main__":
    main()
