import os
import json
from dotenv import load_dotenv
import pandas as pd
import openai
import langchain

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def Fetch_Csv(path):
    df = pd.read_csv(path)
    df = df.head(1)
    return df

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

def get_dataset_data_types(path):
    # Extract dataset information using Langchain
    df = Fetch_Csv(path)
    column_names = df.columns.tolist()

    # Get the semantic data types of each column using OpenAI
    data_types = [get_column_data_type(df[column_name]) for column_name in column_names]

    # Return the result in a dictionary format
    result = {
        "column_names": column_names,
        "data_types": data_types
    }

    return result

def MakeinOrder(path):
    with open(path, "r") as f:
        contents = f.read()

    # load the JSON data from the string
    result = json.loads(contents)

    print("Column Names:", ", ".join(result["column_names"]))
    print("Data Types:")
    for column_name, data_type in zip(result["column_names"], result["data_types"]):
        if data_type == "{'Values': 'URL'}":
            data_type = "URL"
        print(f"{column_name}: {data_type}")
        
if __name__ == "__main__":
    path = "Data/test.csv"
    result = get_dataset_data_types(path)
    jsonpath = "Data/result.txt"
    with open(jsonpath, "a") as f:
        f.write(json.dumps(result) + "\n")
        
    MakeinOrder(jsonpath)
    
