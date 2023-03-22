import streamlit as st
import openai
import requests
import base64

# Set up OpenAI API key
openai.api_key = st.text_input("Enter OpenAI API key:", type="password")

# Define function to retrieve GitHub repo information
def get_repo_info(url):
    # Extract username and repo name from URL
    url_parts = url.split("/")
    username = url_parts[-2]
    repo_name = url_parts[-1]
    
    # Make API request to GitHub to retrieve repo information
    response = requests.get(f"https://api.github.com/repos/{username}/{repo_name}")
    
    # Return repo information as JSON
    return response.json()

def generate_response(prompt, repo_info):
    # Retrieve repo description and readme contents
    description = repo_info.get("description", "")
    if description is None:
        description = ""
    readme_url = repo_info["svn_url"] + "/readme"
    readme_response = requests.get(readme_url)
    readme_contents = readme_response.json()["content"]
    
    # Generate AI response using OpenAI's GPT-3
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt + "\n\n" + description + "\n\n" + readme_contents,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    # Return AI response
    return response.choices[0].text

# Set up StreamLit app
st.title("GitHub AI Prompt")
url = st.text_input("Enter GitHub repo URL:")
prompt = "Please provide a summary of the main features of this Python repository, and suggest any improvements that could be made to the codebase. The repository is called \"" + url.split("/")[-1] + "\" and is located at \"" + url + "\"."
if st.button("Generate Response"):
    repo_info = get_repo_info(url)
    response = generate_response(prompt, repo_info)
    decoded_response = base64.b64decode(response).decode("utf-8")
    st.write(decoded_response)
