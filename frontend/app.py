import streamlit as st
import requests
import pandas as pd

class PhrasalVerbApp:
    BACKEND_URL = "http://localhost:8000"
    INITIAL_TABLE_DATA = [
        ["", "phrasal verb", "meaning", "example"],
        ["Row 1", "", "", ""],
        ["Row 2", "", "", ""],
        ["Row 3", "", "", ""]
    ]

    def __init__(self):
        self.init_session_state()

    def init_session_state(self):
        if 'table_data' not in st.session_state:
            st.session_state.table_data = self.INITIAL_TABLE_DATA 
        if 'api_key' not in st.session_state:
            st.session_state.api_key = ""

    def update_table(self, row_index, new_data):
        st.session_state.table_data[row_index] = [f"Row {row_index}"] + new_data

    def fetch_random_phrasal_verb(self):
        return self._make_request("get", f"{self.BACKEND_URL}/random-phrasal-verb")

    def fetch_nouns_for_sentence(self):
        phrasal_verbs = [row[1] for row in st.session_state.table_data[1:] if row[1]]
        return self._make_request("post", f"{self.BACKEND_URL}/getNounForMakeSentence", json={"phrasal_verbs": phrasal_verbs})

    def set_api_key(self, api_key):
        response = self._make_request("post", f"{self.BACKEND_URL}/set-api-key", json={"api_key": api_key})
        if response:
            st.success("API key set successfully")
            st.session_state.api_key = api_key

    def _make_request(self, method, url, **kwargs):
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error: Unable to fetch data. Status code: {response.status_code}")
        except requests.RequestException as e:
            st.error(f"Error: {str(e)}")
        return None

    def create_dataframe(self):
        df = pd.DataFrame(st.session_state.table_data[1:], columns=st.session_state.table_data[0])
        df.set_index(df.columns[0], inplace=True)
        return df

    def render_gen_buttons(self):
        for i in range(1, 4):
            if st.button(f"Gen {i}", key=f"gen_button_{i}"):
                data = self.fetch_random_phrasal_verb()
                if data:
                    self.update_table(i, [data['phrasal_verb'], data['meaning'], data['example']])

    def render_api_key_input(self):
        api_key = st.text_input("Enter your OpenAI API key:", value=st.session_state.api_key, type="password")
        if st.button("Set API Key"):
            self.set_api_key(api_key)

    def render_phrasal_verb_section(self):
        st.header("1. Generate Phrasal Verbs")
        col1, col2 = st.columns([1, 12])
        with col1:
            self.render_gen_buttons()
        with col2:
            st.table(self.create_dataframe())

    def render_noun_generation_section(self):
        st.header("2. Generate Nouns for Sentence Making")
        if st.button("Generate Nouns"):
            nouns = self.fetch_nouns_for_sentence()
            if nouns:
                st.success("Nouns generated successfully!")
                st.write("Use these nouns to make sentences with the phrasal verbs above:")
                st.write(", ".join(nouns["nouns"]))
            else:
                st.warning("Please generate at least one phrasal verb before generating nouns.")

    def run(self):
        st.title("Phrasal Verb Learning App")
        self.render_api_key_input()
        self.render_phrasal_verb_section()
        st.divider()
        self.render_noun_generation_section()

if __name__ == "__main__":
    app = PhrasalVerbApp()
    app.run()