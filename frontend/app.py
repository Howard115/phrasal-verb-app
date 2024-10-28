import streamlit as st
import requests
from dataclasses import dataclass
from typing import List

@dataclass
class PhrasalVerb:
    phrasal_verb: str
    meaning: str
    example: str

class PhrasalVerbApp:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.phrasal_verbs: List[PhrasalVerb] = [None, None, None]
        
    def fetch_random_phrasal_verb(self) -> PhrasalVerb:
        response = requests.get(f"{self.base_url}/api/v1/phrasal-verbs/random")
        if response.status_code == 200:
            data = response.json()
            return PhrasalVerb(**data)
        return None

    def get_noun_suggestions(self) -> List[str]:
        if None in self.phrasal_verbs:
            return []
        
        payload = {
            "phrasal_verbs": [pv.phrasal_verb for pv in self.phrasal_verbs if pv]
        }
        response = requests.post(f"{self.base_url}/api/v1/nouns/suggestions", json=payload)
        if response.status_code == 200:
            return response.json()["nouns"]
        return []

    def set_api_key(self, api_key: str) -> bool:
        response = requests.post(
            f"{self.base_url}/api/v1/configuration/api-key",
            json={"api_key": api_key}
        )
        return response.status_code == 200

    def render(self):
        st.title("Phrasal Verb Learning Assistant")
        st.write("Get three random phrasal verbs and receive noun suggestions!")

        # Initialize session states
        if 'phrasal_verbs' not in st.session_state:
            st.session_state.phrasal_verbs = [None, None, None]
        if 'api_key_set' not in st.session_state:
            st.session_state.api_key_set = False

        # API Key Section (only show if not set)
        if not st.session_state.api_key_set:
            st.subheader("OpenAI API Key Configuration")
            api_key = st.text_input("Enter your OpenAI API Key", type="password")
            if st.button("Set API Key"):
                if self.set_api_key(api_key):
                    st.session_state.api_key_set = True
                    st.success("API key set successfully!")
                    st.rerun()
                else:
                    st.error("Failed to set API key. Please try again.")

        # Display three columns for phrasal verbs
        cols = st.columns(3)
        for i, col in enumerate(cols):
            with col:
                st.subheader(f"Phrasal Verb {i+1}")
                if st.button(f"Get Random Verb {i+1}", key=f"btn_{i}"):
                    st.session_state.phrasal_verbs[i] = self.fetch_random_phrasal_verb()

                if st.session_state.phrasal_verbs[i]:
                    pv = st.session_state.phrasal_verbs[i]
                    st.write(f"**Verb:** {pv.phrasal_verb}")
                    st.write(f"**Meaning:** {pv.meaning}")
                    st.write(f"**Example:** {pv.example}")

        # Get noun suggestions (only if API key is set)
        if all(st.session_state.phrasal_verbs):
            st.subheader("Noun Suggestions")
            if st.button("Get Noun Suggestions", disabled=not st.session_state.api_key_set):
                if st.session_state.api_key_set:
                    self.phrasal_verbs = st.session_state.phrasal_verbs
                    nouns = self.get_noun_suggestions()
                    if nouns:
                        st.write("You can use these nouns with the phrasal verbs:")
                        st.write(", ".join(nouns))
                else:
                    st.warning("Please set your OpenAI API key first")

def main():
    app = PhrasalVerbApp()
    app.render()

if __name__ == "__main__":
    main()
