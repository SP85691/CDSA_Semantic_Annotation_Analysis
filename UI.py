import os
import json
from dotenv import load_dotenv
import pandas as pd
import openai
import langchain
import streamlit as st

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def Fetch_Csv(df):
    return df.head(1)

def get_column_data_type(column):
    # Generate a prompt for the OpenAI API
    prompt = f"What is the semantic data type of the following column values? Values: {', '.join(column.astype(str))}"

    # Call the OpenAI API to get the data type
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant You have received an information about political candidates. Your task is to understand the semantic data type of each column in the dataset. Analyze the values in each column to determine the appropriate data type. Some columns may contain specific types of data such as names, addresses, dates, etc. Your goal is to provide the semantic data type for each column in the dataset. Use the following categories for semantic data types: Name, Constituency, State, Address, URL, Integer, String, Datetime, and Float/Integer for age. You have to give output in just single word"},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the data type from the API response
    data_type = response.choices[0].message.content.strip()

    return data_type

def get_dataset_data_types(df):
    # Extract dataset information using Langchain
    column_names = df.columns.tolist()

    # Get the semantic data types of each column using OpenAI
    data_types = [get_column_data_type(df[column_name]) for column_name in column_names]

    # Return the result in a dictionary format
    result = {
        "column_names": column_names,
        "data_types": data_types
    }

    return result

def convert_data_types(data_types):
    converted_types = []
    for data_type in data_types:
        if data_type == "URL":
            converted_types.append("URL")
        elif data_type == "Name":
            converted_types.append("Name")
        elif data_type == "Constituency":
            converted_types.append("Constituency")
        elif data_type == "Datetime":
            converted_types.append("Datetime")
        elif data_type == "String":
            converted_types.append("String")
        elif data_type == "State":
            converted_types.append("State")
        elif data_type == "Address":
            converted_types.append("Address")
        elif data_type == "Integer" or data_type == "Float":
            converted_types.append("Integer")
    return converted_types

def convert_to_json(column_names, data_types):
    json_result = {}
    for column_name, data_type in zip(column_names, data_types):
        if column_name == "Party_accepted":
            json_result[column_name] = "String"
        elif column_name == "Status_accepted":
            json_result[column_name] = "String"
        elif column_name == "State_accepted":
            json_result["state_data"] = "State"
        elif column_name == "Constituency_accepted":
            json_result["consts_data"] = "Constituency"
        elif column_name == "View More Link_accepted":
            json_result[column_name] = "URL"
        elif column_name == "Name_accepted":
            json_result["name"] = "Name"
        elif column_name == "Profile Picture_accepted":
            json_result[column_name] = "URL"
        elif column_name == "Application Uploaded_accepted":
            json_result[column_name] = "Datetime"
        elif column_name == "Affidavit Download Link_accepted":
            json_result[column_name] = "URL"
        elif column_name == "Affidavit Uploaded Date_accepted":
            json_result[column_name] = "Datetime"
        elif column_name == "Father's Name_accepted":
            json_result["Father's Name_accepted"] = "Name"
        elif column_name == "Gender_accepted":
            json_result["gender_data"] = "String"
        elif column_name == "Address_accepted":
            json_result["residency"] = "Address"
        elif column_name == "Age_accepted":
            json_result[column_name] = "Integer"
    return json_result

def MakeinOrder(result):
    st.write("Results:")
    st.write("User: What is the data type of each column in the dataset?")
    st.write("Bot: Sure, I can help you with that. Here are the data types of each column:")
    for column_name, data_type in result.items():
        message = f"{column_name}: {data_type}"
        st.write(f"Bot: {message}")
        
if __name__ == "__main__":
    # Create a directory for saving files
    if not os.path.exists("streamlit"):
        os.makedirs("streamlit")
        
    # Add a file uploader to allow users to upload their CSV file
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    print(uploaded_file)
    if uploaded_file:
        file_path = os.path.join("streamlit", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Read the CSV file using pandas
        df = pd.read_csv(file_path)
        result = get_dataset_data_types(df)

        # Save the results to a text file in the append manner
        with open("streamlit/result.json", "a") as f:
            f.write(json.dumps(result) + "\n")

        # Display the results in the chat interface
        MakeinOrder(result)
