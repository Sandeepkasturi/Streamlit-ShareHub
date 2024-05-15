# Streamlit ShareHub

Streamlit ShareHub is a web application that allows users to upload and run their own Streamlit applications directly from a GitHub repository. This application simplifies the process of sharing and running Streamlit apps by automating the download, installation of dependencies, and execution of the app.

## Features

- **GitHub Repository Integration:** Users can enter the URL of their GitHub repository containing the Streamlit app Python file and requirements.txt.
- **Automated File Processing:** The application automatically downloads the required files from the GitHub repository and extracts the Streamlit app Python file and requirements.txt.
- **Dependency Installation:** It installs the necessary dependencies specified in the requirements.txt file using pip.
- **Streamlit App Execution:** Once dependencies are installed, the Streamlit app is executed and made accessible via local and network URLs.

## Usage

1. **Enter GitHub Repository URL:** Input the URL of the GitHub repository containing your Streamlit app Python file and requirements.txt.
2. **Run Streamlit App:** Click the "Run Streamlit App" button to start the process.
3. **File Details:** After processing, the application displays details of the uploaded Streamlit app Python file and requirements.txt.
4. **Dependencies Installation:** Dependencies are installed automatically with progress indication.
5. **Access Your Streamlit App:** Once installed, the Streamlit app is executed, and URLs are provided for access.

## Requirements

- Python 3.x
- Streamlit
- requests (for GitHub repository download)
- zipfile (for repository extraction)
- shutil (for file copying)
- subprocess (for dependency installation and Streamlit app execution)

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/Streamlit-ShareHub.git
cd Streamlit-ShareHub
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Run the application:

```
streamlit run streamlit_app.py
```

## Credits

Streamlit ShareHub is developed by [Sandeep Kasturi](https://instagram.com/sandeep_kasturi_). It utilizes the Streamlit library for building the web application interface and interacting with Streamlit apps. Clone to Streamlit cloud.

