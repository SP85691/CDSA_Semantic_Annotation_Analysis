# CDSA Semantic Annotation Analysis

In this project I have created a solution to the problem of semantic annotation of CDSA documents. The solution is based on the use of the Openai API by using of "GPT-3.5-Turbo" Model. We are focusing on get this type of information from the documents:

```bash
{
  "Party_accepted": "Categorical",
  "Status_accepted": "Categorical",
  "state_data": "Location",
  "consts_data": "Location",
  "View More Link_accepted": "URL",
  "name": "Categorical",
  "Profile Picture_accepted": "URL",
  "Application Uploaded_accepted": "Time",
  "Affidavit Download Link_accepted": "URL",
  "Affidavit Uploaded Date_accepted": "Time",
  "Father's Name_accepted": "Categorical",
  "gender_data": "Categorical",
  "residency": "Location",
  "Age_accepted": "Numerical"
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

### Install all Required Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

#### To Run CLI Application

```bash
python main.py
```
