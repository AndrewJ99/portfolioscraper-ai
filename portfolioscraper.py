#pip install beautifulsoup4
#pip install requests
#pip install openai
#pip install streamlit

import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import streamlit as st

# Initialize the OpenAI object with your API key
ai = OpenAI(api_key='apikey')

# Define the prompt for the GPT model
prompt = 'Based on the information of this website portfolio, can you tell me the best suited job positions for this individual?'

# Title of the Streamlit app
st.title("AI Job Title Hunter")

# Input field for the URL
title = st.text_input('Enter Portfolio URL', '')

# Button to trigger the processing
if st.button('Analyze URL'):
    if title:
        st.write('Analyzing URL: ', title)
        # Function to scrape the site
        def scrape_site(url):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    text = soup.get_text(separator='\n', strip=True)
                    return text
                else:
                    st.error(f"Failed to retrieve website, status code: {response.status_code}")
                    return None
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                return None

        # Function to analyze the text using OpenAI
        def analyze_text(text):
            try:
                chat_completion = ai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are going to analyze this portfolio website and suggest possible job positions this individual can specialize in or grow in their career."},
                        {"role": "user", "content": text}
                    ]
                )
                result = chat_completion.choices[0].message.content  # Assuming correct path to extract content
                return result
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                return "No result due to error or exception."

        # Process the URL
        website_text = scrape_site(title)
        if website_text:
            result = analyze_text(website_text)
            st.text_area("Analysis Result", value=result, height=300)
    else:
        st.warning('Please enter a URL to analyze.')
