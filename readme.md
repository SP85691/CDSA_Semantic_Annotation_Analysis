# CDSA Semantic Annotation Analysis
In this project I have created a solution to the problem of semantic annotation of CDSA documents. The solution is based on the use of the Openai API by using of "GPT-3.5-Turbo" Model. We are focusing on get this type of information from the documents:
```bash
{
  "Party_accepted": "String",
  "Status_accepted": "String",
  "state_data": "State",
  "consts_data": "Constituency",
  "View More Link_accepted": "URL",
  "name": "Name",
  "Profile Picture_accepted": "URL",
  "Application Uploaded_accepted": "Datetime",
  "Affidavit Download Link_accepted": "URL",
  "Affidavit Uploaded Date_accepted": "Datetime",
  "Father's Name_accepted": "Name",
  "gender_data": "String",
  "residency": "Address",
  "Age_accepted": "Integer"
}
```

## Usage

```bash
git clone <repo-url> && cd <repo-name>
```

## Installation
### Create a virtual environment
```bash
python3 -m venv venv
```
### Activate the Virtual Environment
```bash
./venv/Scripts/activate
```
### Install Poetry
```bash
pip install poetry
```
### Install all Required Dependencies
```bash
poetry install
```
### Run the Application
#### To Run CLI Application
```bash
python main.py
```

#### To Run Web Application
```bash
streamlit run UI.py
```

