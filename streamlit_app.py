#Developed By SKAV TECH, AUTOBOT
import streamlit as st
import subprocess
import time
import os
import requests
from zipfile import ZipFile
import shutil

# Set page configuration
st.set_page_config(page_title="Streamlit ShareHub", layout="wide")

# Custom CSS for advanced styling
st.markdown("""
<style>
/* Dark theme */
body {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

.main {
    background-color: #2a2a2a;
}

.stButton>button {
    background: linear-gradient(to right, #0073e6, #00b3e6);
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    transition-duration: 0.4s;
    cursor: pointer;
    border-radius: 8px;
}

.stButton>button:hover {
    background: linear-gradient(to right, #0059b3, #0073e6);
}

.stProgress .st-bo {
    background-color: palegreen;
}

.stMarkdown {
    color: #e0e0e0;
}

.stFileUploader .st-dz {
    background-color: #333333;
    border-color: #0073e6;
    color: #e0e0e0;
}

.stFileUploader .st-dz p {
    color: #e0e0e0;
}

.stFileUploader .st-dz svg {
    fill: #0073e6;
}

.stFileUploader .st-dz.st-dz-dragover {
    border-color: #0073e6;
}

.stFileUploader .st-dz.st-dz-error {
    border-color: #ff4d4d;
}

.stFileUploader .st-dz.st-dz-error svg {
    fill: #ff4d4d;
}

.stFileUploader .st-dz.st-dz-error p {
    color: #ff4d4d;
}

.stCheckbox span.checkmark {
    border-color: #0073e6;
}

.stCheckbox:checked+label span.checkmark {
    background-color: #0073e6;
}

.stCheckbox:checked+label span.checkmark:after {
    border-color: #1e1e1e;
}

.stHelp {
    color: #9e9e9e;
}

.stMarkdown code {
    background-color: #333333;
    color: #ffffff;
}

.stMarkdown pre {
    background-color: #333333;
    border-color: #0073e6;
}

.stMarkdown pre code {
    color: #ffffff;
}

.stMarkdown blockquote {
    border-left: 4px solid #0073e6;
}

.stMarkdown a {
    color: #0073e6;
}

.stMarkdown a:hover {
    color: #0059b3;
}

.stMarkdown h1 {
    color: #e0e0e0;
}

.stMarkdown h2 {
    color: #e0e0e0;
}

.stMarkdown h3 {
    color: #e0e0e0;
}

.stMarkdown h4 {
    color: #e0e0e0;
}

.stMarkdown h5 {
    color: #e0e0e0;
}

.stMarkdown h6 {
    color: #e0e0e0;
}
.upload-section {
    padding: 20px;
    border: 2px solid #0073e6;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# Function to download and extract files from GitHub repository
def download_from_github(repo_url):
    try:
        # Download the repository as a zip file
        repo_zip = requests.get(repo_url + "/archive/refs/heads/main.zip")
        with open("repo.zip", "wb") as f:
            f.write(repo_zip.content)

        # Extract the zip file
        with ZipFile("repo.zip", "r") as zip_ref:
            zip_ref.extractall("repo")

        # Find .py file and requirements.txt
        py_file = None
        requirements_file = None
        for root, dirs, files in os.walk("repo"):
            for file in files:
                if file.endswith(".py"):
                    py_file = os.path.join(root, file)
                elif file == "requirements.txt":
                    requirements_file = os.path.join(root, file)

        return py_file, requirements_file

    except Exception as e:
        st.error("Error downloading files from GitHub repository.")
        st.stop()


# Header and Instructions
st.title("Streamlit ShareHub")
st.write("""
This application allows you to upload and run your own Streamlit applications.
### Instructions
1. Enter the GitHub repository URL containing your Streamlit app Python file and requirements.txt.
2. Click the "Run Streamlit App" button.
3. The application will download the required files, install the dependencies, and run your Streamlit app.
""")

# Enter GitHub repository URL
repo_url = st.text_input("Enter GitHub repository URL")

# Check if the repository URL is provided
if repo_url:
    # Check if the URL is a valid GitHub repository
    if "github.com" not in repo_url:
        st.warning("Please enter a valid GitHub repository URL.")
    else:
        if st.button("Run Streamlit App"):
            # Download files from GitHub repository
            with st.spinner("Downloading files from GitHub repository..."):
                py_file, requirements_file = download_from_github(repo_url)

            # Check if files are found
            if py_file and requirements_file:
                with st.expander("File Details"):
                    st.write("### Streamlit App File")
                    with open(py_file, "r", encoding="utf-8") as f:
                        st.code(f.read(), language="python")
                    st.write("### Requirements File")
                    with open(requirements_file, "r", encoding="utf-8") as f:
                        st.code(f.read(), language="text")

                # Save uploaded files
                shutil.copy(py_file, "uploaded_streamlit_app.py")
                shutil.copy(requirements_file, "requirements.txt")

                # Install dependencies and run Streamlit app
                with st.spinner("Installing dependencies..."):
                    process = subprocess.Popen(
                        ["pip", "install", "-r", "requirements.txt"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
                    )

                    progress_bar = st.progress(0)
                    percent_complete = 0
                    while True:
                        output = process.stdout.readline()
                        if output == '' and process.poll() is not None:
                            break
                        if output:
                            st.text(output.strip())
                        time.sleep(0.1)
                        percent_complete += 1
                        progress_bar.progress(min(percent_complete, 100))

                    if process.returncode == 0:
                        st.success("Dependencies installed successfully!")

                        # Running the Streamlit app
                        st.info("Starting your Streamlit app...")
                        streamlit_process = subprocess.Popen(
                            ["streamlit", "run", "uploaded_streamlit_app.py"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
                        )

                        local_url = None
                        network_url = None
                        while True:
                            output = streamlit_process.stdout.readline().strip()
                            if "Local URL" in output:
                                local_url = output.split(": ")[1]
                            elif "Network URL" in output:
                                network_url = output.split(": ")[1]
                            if local_url and network_url:
                                break

                        st.success(f"Your Streamlit app is accessible at: [Local URL]({local_url}) (Open in new tab)")
                        st.success(
                            f"Your Streamlit app is accessible at: [Network URL]({network_url}) (Open in new tab)")
                    else:
                        st.error("An error occurred during the installation of dependencies.")
            else:
                st.error("Unable to find .py file or requirements.txt in the GitHub repository.")
else:
    st.warning("Please enter the GitHub repository URL.")
