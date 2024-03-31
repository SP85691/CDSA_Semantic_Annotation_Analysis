import os
import json
from dotenv import load_dotenv
import pandas as pd
import openai

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
            {"role": "system", "content": "You are a helpful assistant, Your task is to understand the semantic data type of each column in the dataset. Analyze the values in each column to determine the appropriate data type. Use the following categories for semantic data types: Numerical, Location, Categorical, Time, URL, HTML. You have to give output in just single word"},
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

    # Load the JSON data from the file
    result = json.loads(contents)
    print(f"Result: {result}")

    # Map column names to their corresponding data types
    column_data_map = dict(zip(result["column_names"], result["data_types"]))

    # Save the final output back to the same file path
    with open(path, "w") as f:
        json.dump(column_data_map, f, indent=2)
    
    print(json.dumps(column_data_map, indent=2))
        
if __name__ == "__main__":
    # Define the path to the CSV file
    csv_path = "Data/TestFiles/mizoram_accepted.csv"

    file_name = os.path.splitext(os.path.basename(csv_path))[0]

    # Extract dataset information and data types
    result = get_dataset_data_types(csv_path)

    # Define the path to save the JSON result
    json_path = f"Data/Outputs/{file_name}.json"

    # Save the result as JSON
    with open(json_path, "w") as json_file:
        json.dump(result, json_file, indent=2)

    # Update the JSON file with column names mapped to data types
    MakeinOrder(json_path)

