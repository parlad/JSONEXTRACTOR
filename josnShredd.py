import json
import pandas as pd
from jsonpath_ng import jsonpath, parse

# Load the JSON data
with open('/content/jsonShredd/data.json') as f:
    data = json.load(f)

# Load the mapping
with open('/content/jsonShredd/mapping.json') as f:
    mapping = json.load(f)

# Prepare an empty dataframe to hold the results
df = pd.DataFrame()

# Iterate over each datapoint in the data file
for i, datapoint in enumerate(data['datapoints']):
    # Prepare an empty dictionary to hold the results for this datapoint
    datapoint_dict = {}
    # Iterate over each field in the mapping file
    for field, path in mapping.items():
        # Prepare the JSONPath expression
        jsonpath_expr = parse(path)
        # Find the first match in the datapoint
        match = jsonpath_expr.find(datapoint)
        if match:
            # If a match was found, add it to the dictionary
            datapoint_dict[field] = [m.value for m in match]
        else:
            # If no match was found, add 'no path' to the dictionary
            datapoint_dict[field] = ['no path']

    # Create a temporary dataframe for this datapoint
    temp_df = pd.json_normalize(datapoint_dict)

    # Identify list-like columns and explode them
    while True:
        list_cols = [col for col in temp_df.columns if any(isinstance(i, list) for i in temp_df[col])]
        if not list_cols:
            break
        for col in list_cols:
            temp_df = temp_df.explode(col)

    # Append the temporary dataframe to the main dataframe
    df = df.append(temp_df)

df.reset_index(drop=True, inplace=True)
df.style.set_properties(**{'border': '1px solid black'})

