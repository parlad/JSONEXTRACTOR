import pandas as pd
import xml.etree.ElementTree as ET

# Read the mapping file
mapping_df = pd.read_csv('mapping.csv')

# Initialize an empty list to store the data
data = []

# Parse the XML file
tree = ET.parse('sample.xml')
root = tree.getroot()

# Iterate through root elements in the XML
for element in root:
    # Initialize a dictionary to store the data for this root element
    root_data = {}

    # Iterate through the mapping DataFrame
    for index, row in mapping_df.iterrows():
        xml_path = row['xml_path']
        column_name = row['column_name']

        # Find the element in the current root using the path
        elements = element.findall(xml_path)

        # Extract the values and append to the dictionary
        values = [element.text if element is not None else '' for element in elements]
        root_data[column_name] = values

    # Append the data for this root element to the list
    data.append(root_data)

# Create a DataFrame from the extracted data
result_df = pd.DataFrame(data)

# Explode columns containing arrays into separate rows
for column_name in result_df.columns:
    result_df = result_df.explode(column_name)

# Reset the DataFrame index
result_df.reset_index(drop=True, inplace=True)

# Replace empty strings with None
result_df = result_df.applymap(lambda x: None if x == '' else x)

# Export the DataFrame as a CSV file
result_df.to_csv('output.csv', index=False)
