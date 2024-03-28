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
        json_result[column_name] = data_type
    return json_result

def MakeinOrder(path):
    with open(path, "r") as f:
        contents = f.read()

    # Load the JSON data from the file
    result = json.loads(contents)

    converted_data_types = convert_data_types(result["data_types"])
    json_output = convert_to_json(result["column_names"], converted_data_types)

    print(json.dumps(json_output, indent=2))
    
    # Save the final output back to the same file path
    with open(path, "w") as f:
        json.dump(json_output, f, indent=2)
        
if __name__ == "__main__":
    path = "Data/mizoram_result.csv"
    result = get_dataset_data_types(path)
    
    jsonpath = "Data/result2.json"
    with open(jsonpath, "w") as f:
        f.write(json.dumps(result) + "\n")
        
    MakeinOrder(jsonpath)
    
