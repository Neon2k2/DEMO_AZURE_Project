# Demo Azure Project

This project is a demo of using Azure Blob Storage and Azure SQL Storage with Python, Django, and PySpark. The purpose of this project is to showcase the process of manually taking data from the user as a CSV, uploading it to Azure Blob Storage using the web application, dynamically processing the data, and then uploading the data to Azure SQL Storage.

## Prerequisites

Python 3.6 or higher

Django 3.0 or higher

PySpark 3.0 or higher

Azure Blob Storage account

Azure SQL Storage account



## Getting Started
To get started with the project, follow the steps below:

1. Clone the repository to your local machine
```bash
git clone https://github.com/your-username/demo-azure-project.git

```
2. Create a virtual environment and activate it.
```bash
python -m venv env
source env/bin/activate
```

3. Install the required packages using pip

```bash
pip install -r requirements.txt
```

4. Update the credentials for your Azure Blob Storage and Azure SQL Storage accounts in the settings.py file

5.Run the Django web application

```bash
python manage.py runserver
```

6. Navigate to http://127.0.0.1:8000/ in your web browser

7. Upload a CSV file containing data to be processed

8. Click on the "Process Data" button to dynamically process the data using PySpark

9. Click on the "Upload to SQL" button to upload the processed data to Azure SQL Storage
## Project Structure

The project is structured as follows:

app - Contains the Django web application files

data_processing - Contains the PySpark script to dynamically process the uploaded data

templates - Contains the HTML templates for the web application


## Conclusion

This project serves as a simple example of how to use Azure Blob Storage and Azure SQL Storage with Python, Django, and PySpark to process and store data dynamically.
