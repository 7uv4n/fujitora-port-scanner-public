# Flask Application

This is an Open-source Flask application that scans a set of IP addresses and their Ports and give a dashboard on results
Developed by Yuvan and Sabrina

Warning: As this is still in Development, some features might not work or issues exist with User Experience

## Installation

1. Clone the repository:
   ```git clone https://github.com/7uv4n/fujitora-port-scanner-public```
2. Navigate to the project Directory
    cd fujitora-port-scanner
3. Create a virtual Environment:
    ```python -m venv venv```  
5. Activate the virtual environment:
    On Windows, use ```.venv\Scripts\activate```
6. Install the dependencies:
    pip install -r requirements.txt
7. Start the Flask Development Server
    ```python main.py```

## Description

JSON Payload files will be stored as 'blob_storage' folder whereas the Dashboard will be stored inside the Templates Folder after Compilation. 