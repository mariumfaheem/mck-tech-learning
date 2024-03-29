#Data Loading
with open(r"/content/data_raw_5mb.txt", 'r') as fp:
  single_line_record = fp.read().split('1A')
  first_record = (single_line_record[1])

#Data Cleaning
# Define the regex pattern to match escape characters
regex_pattern = r'[\x1c\x1d\x1e\x1f\x1a\x1b]'

# Replace escape characters with 'x1z' using regex and re.sub()
first_record_modified = re.sub(regex_pattern, ' ', first_record)

data1 = {
    "Gr 0": {
        "FDR": None,
        "FDD": None,
        "REF": None,
        "STX": None,
        "IFD": None,
        "LTS": None,
        "ATR": {}
    }
}

data2 = {
    "Gr 1": {
        "APD": None,
        "DAT": None,
        "STX": None,
        "EQP": None,
        "EQI": None,
        "EQD": None,
        "LEG": None,
        "EQN": None,

    }

}


#gr 0
# data = first_record_modified

# Extract the data using regular expressions
matches = re.findall(r'(FDR|FDD|REF|STX|IFD|LTS|ATR)\s+(.*?)\s+(?=(FDR|FDD|REF|STX|IFD|LTS|ATR)|$)', first_record_modified)
matches
# Update the dictionary with the extracted data
for match in matches:
    key = match[0]
    value = match[1]
    data1["Gr 0"][f"{key}"] = value
# Convert the dictionary to JSON
json_data = json.dumps(data1, indent=4)

# Print the JSON data
print(json_data)


#gr 1
matches = re.findall(r'(APD|DAT|STX|EQP|EQI|EQD|LEG|EQN)\s+(.*?)\s+(?=(APD|DAT|STX|EQP|EQI|EQD|LEG|EQN)|$)', first_record_modified)
matches
# Update the dictionary with the extracted data
for match in matches:
    # print(match)
    key = match[0]
    value = match[1]
    data2["Gr 1"][f"{key}"] = value


# Convert the dictionary t  o JSON
json_data = json.dumps(data2, indent=4)

# # Print the JSON data
print(json_data)
