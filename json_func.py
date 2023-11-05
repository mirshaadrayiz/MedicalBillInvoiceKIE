import json
import parameters


def add_to_json(page_number, key_values, final_line_values):
    
    result = [dict(zip(final_line_values.keys(), values)) for values in zip(*final_line_values.values())]
    
    data = {
        "Page_Number": page_number,
        "Table": result,
        "Key_Values": key_values
    }

    # Try to open the JSON file in append mode ("a")
    try:
        with open(parameters.json_file_name, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty dictionary
        existing_data = {}

    # Check if "Page_Number" already exists in the JSON data
    if "Page_Number" in existing_data:
        # If it exists, append the new data to the existing list
        existing_data["Page_Number"].append(data)
    else:
        # If it doesn't exist, create a list with the new data
        existing_data["Page_Number"] = [data]

    # Write the updated data back to the JSON file
    with open(parameters.json_file_name, "w") as json_file:
        json.dump(existing_data, json_file, indent=3)