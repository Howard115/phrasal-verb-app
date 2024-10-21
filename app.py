import streamlit as st
import pandas as pd
import random
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv("phrasal-verb.csv")

# Function to get a random phrasal verb
def get_random_phrasal_verb(df):
    return df.iloc[random.randint(0, len(df) - 1)]

# Function to generate the visualization
def generate_visualization(phrasal_verb, meaning, example, api_key):
    llm = OpenAI(temperature=0.7, openai_api_key=api_key)
    
    prompt = PromptTemplate(
        input_variables=["phrasal_verb", "meaning", "example"],
        template="""
        Visualize the phrasal verb "{phrasal_verb}" by explaining how its verb and preposition components combine to form its meaning.

        1. Identify Components: Break down the phrasal verb into its verb and preposition parts.
        2. Explain Each Part: Describe the typical meaning of both the verb and the preposition individually.
        3. Combine Meanings: Illustrate how the combination of these two elements merges to define the phrasal verb.
        4. Provide Examples: Use the provided definition and example to clarify the explanation.

        Meaning: {meaning}
        Example: {example}

        Output a brief paragraph explaining the formation and meaning of the phrasal verb. Include the identification and analysis of each part. End with how these parts synthesize to create the given meaning of the phrasal verb. Add a Chinese translation of the explanation at the end.
        """
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain.run(phrasal_verb=phrasal_verb, meaning=meaning, example=example)

# Streamlit app
def main():
    st.title("Phrasal Verb Visualizer")
    
    # Get OpenAI API key
    api_key = st.text_input("Enter your OpenAI API key:", type="password")
    
    if api_key:
        df = load_data()
        
        if st.button("Generate Random Phrasal Verb Visualization"):
            phrasal_verb_row = get_random_phrasal_verb(df)
            
            st.subheader(f"Phrasal Verb: {phrasal_verb_row['Phrasal Verb']}")
            st.write(f"Meaning: {phrasal_verb_row['Meaning']}")
            st.write(f"Example: {phrasal_verb_row['Example']}")
            
            with st.spinner("Generating visualization..."):
                visualization = generate_visualization(
                    phrasal_verb_row['Phrasal Verb'],
                    phrasal_verb_row['Meaning'],
                    phrasal_verb_row['Example'],
                    api_key
                )
            
            st.subheader("Visualization:")
            st.write(visualization)
    else:
        st.warning("Please enter your OpenAI API key to use the app.")

if __name__ == "__main__":
    main()