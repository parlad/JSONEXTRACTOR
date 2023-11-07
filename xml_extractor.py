import pandas as pd
import xml.etree.ElementTree as ET
import json

# Read the mapping file
mapping_df = pd.read_csv('mapping.csv')

# Read the JSON data from a file
with open('input2.json', 'r') as json_file:
    json_data = json.load(json_file)

# Initialize an empty list to store the data
data = []

for item in json_data:
    # Parse the XML string from the JSON data
    xml_string = item['consolidatereportdetailtext']
    root = ET.fromstring(xml_string)

    # Iterate through root elements in the XML
    for element in root:
        # Initialize a dictionary to store the data for this XML
        xml_data = {}

        # Add "_id" value to the dictionary
        xml_data["_id"] = item["_id"]["$oid"]

        # Iterate through the mapping DataFrame
        for index, row in mapping_df.iterrows():
            xml_path = row['xml_path']
            column_name = row['column_name']

            # Find the element in the current root using the path
            elements = element.findall(xml_path)

            # Extract the values and append to the dictionary
            values = [element.text if element is not None else '' for element in elements]
            xml_data[column_name] = values

        data.append(xml_data)

# Create a DataFrame from the extracted data
result_df = pd.DataFrame(data)

# Explode columns containing arrays into separate rows
for column_name in result_df.columns:
    result_df = result_df.explode(column_name)

# Reset the DataFrame index
result_df.reset_index(drop=True, inplace=True)

# Replace empty strings with None
result_df = result_df.applymap(lambda x: None if x == '' else x)

# Show the resulting DataFrame
print(result_df)
