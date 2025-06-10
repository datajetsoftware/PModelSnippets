import sys
import json

TOPN = 4     # Define constant for top N rows to keep
MODE = "BTI"  # Options: Any combination of B (Base), T (Target), I (Index), or NONE/'' (No processing)
SORT_MODE = "Index"  # Options: Base, Target, or Index

INDEX_MIN = 1.0  # Minimum index threshold (-1 means no threshold)
INDEX_MAX = -1  # Maximum index threshold (-1 means no threshold)
BASE_MIN = -1  # Minimum threshold for base (-1 means no threshold)
BASE_MAX = -1  # Maximum threshold for base (-1 means no threshold)
TARGET_MIN = -1  # Minimum threshold for target (-1 means no threshold)
TARGET_MAX = -1  # Maximum threshold for target (-1 means no threshold)

# Get input and output file paths from command-line arguments
inputfile = sys.argv[1]
outputfile = sys.argv[2]

#Below comment must be included to be able to read json object from sys.argv[3]
#PARAMS_IN_FILE
paramfile = sys.argv[3]

#read params file
pFile = open(paramfile, 'r',encoding='utf8') 
pdata = pFile.read()
pFile.close()
pobject = json.loads(pdata)

# Parameter mapping: constant name to pobject key
param_mapping = {
    "TOPN": "TopN",
    "MODE": "Mode",
    "SORT_MODE": "SortMode",
    "INDEX_MIN": "IndexMin",
    "INDEX_MAX": "IndexMax",
    "BASE_MIN": "BaseMin",
    "BASE_MAX": "BaseMax",
    "TARGET_MIN": "TargetMin",
    "TARGET_MAX": "TargetMax"
}

hasParam = True

# Update parameters from pobject if not empty/blank
if hasParam:
    for var_name, pobject_key in param_mapping.items():
        if pobject_key in pobject:
            value = pobject[pobject_key]
            # Check for empty/blank values
            if value is None or (isinstance(value, str) and value.strip() == ""):
                continue  # Skip and keep default
            # Assign the value with appropriate type conversion
            if var_name == "TOPN":
                globals()[var_name] = int(value)
            elif var_name in ["INDEX_MIN", "INDEX_MAX", "BASE_MIN", "BASE_MAX", "TARGET_MIN", "TARGET_MAX"]:
                globals()[var_name] = float(value)
            else:  # MODE, SORT_MODE (strings)
                globals()[var_name] = str(value)

# Read input JSON file into a string
iFile = open(inputfile, 'r', encoding='utf8')
data = iFile.read()
iFile.close()

# Parse JSON string into a Python dictionary
dataModel = json.loads(data)

# Extract relevant data from the JSON model
grid = dataModel["grid"]          # Grid data (2D array)
headerInfo = dataModel["headerInfo"]  # Header metadata
rows = dataModel["rows"]          # Number of rows in grid
hasTotalRow = dataModel["hasTotalRow"]  # Flag for total row
hasNullRow = dataModel["hasNullRow"]    # Flag for null row
associatedData= dataModel["associatedData"] # associatedData Object

# Dynamically determine column indices
num_columns = len(grid)
base_col_idx = num_columns - 3  # Index of base column (second-to-last)
target_col_idx = num_columns - 2  # Index of target column (second-to-last)
index_col_idx = num_columns - 1  # Index of index column (last)

# Convert pobject items to a list of dictionaries for better readability
pobject_items = [{"key": key, "value": value} for key, value in pobject.items()]  

# Update associatedData["info"] with the list of pobject items
associatedData["info"] = {
    "associatedData Object": str(type(associatedData)),
    "pobject Object": str(type(pobject)),
    "pobject Size": str(len(pobject)),
    "pobject Items": pobject_items
}


# Initialize starting row index
startRow = 0
if hasNullRow:
    startRow = 1  # Skip first row if it contains null values

# Adjust row count if total row exists
if hasTotalRow:
    rows = rows - 1  # Exclude total row from processing
    
#------------------------------------------------
#CUSTOM SECTION - Modify section below to meet filtering criteria
#------------------------------------------------

# Normalize mode and sort mode to uppercase for consistent comparison
mode = MODE.upper() if MODE else "NONE"
sort_mode = SORT_MODE.lower()

# Check which thresholds to apply based on presence of letters in mode
apply_base = False
apply_target = False
apply_index = False

if mode not in ("NONE", ""):
    if mode == "ALL":
        apply_base = apply_target = apply_index = True
    else:
        apply_base = "B" in mode    # Check if Base threshold should be applied
        apply_target = "T" in mode  # Check if Target threshold should be applied
        apply_index = "I" in mode   # Check if Index threshold should be applied

# Collect all valid rows with their indices and values
valid_rows = []
for r in range(startRow, rows):
    base_val = float(grid[base_col_idx][r])    # Base value (second-to-last column)
    target_val = float(grid[target_col_idx][r])  # Target value (second-to-last column)
    index_val = float(grid[index_col_idx][r])   # Index value (last column)
    
    # Initialize conditions_met as True for NONE mode
    conditions_met = True
    
    # Apply threshold checks based on mode settings
    if mode not in ("NONE", ""):
        # Base threshold (skip if both min and max are -1)
        if apply_base:
            if BASE_MIN != -1:
                conditions_met = conditions_met and (base_val >= BASE_MIN)
            if BASE_MAX != -1:
                conditions_met = conditions_met and (base_val <= BASE_MAX)
        
        # Target threshold (skip if both min and max are -1)
        if apply_target:
            if TARGET_MIN != -1:
                conditions_met = conditions_met and (target_val >= TARGET_MIN)
            if TARGET_MAX != -1:
                conditions_met = conditions_met and (target_val <= TARGET_MAX)
        
        # Index threshold (skip if both min and max are -1)
        if apply_index:
            if INDEX_MIN != -1:
                conditions_met = conditions_met and (index_val >= INDEX_MIN)
            if INDEX_MAX != -1:
                conditions_met = conditions_met and (index_val <= INDEX_MAX)
    
    # If conditions are met, add row index and value for sorting
    if conditions_met:
        if sort_mode == "base":
            valid_rows.append((r, base_val))
        elif sort_mode == "target":
            valid_rows.append((r, target_val))
        elif sort_mode == "index":
            valid_rows.append((r, index_val))


# Sort valid rows by the selected sort mode in descending order
valid_rows.sort(key=lambda x: x[1], reverse=True)

# Take the top TOPN rows
selected_rows = [r[0] for r in valid_rows[:min(TOPN, len(valid_rows))]]

# Create a new grid with only the selected rows
new_grid = [[grid[c][r] for r in selected_rows] for c in range(len(grid))]

# Update the grid in the data model
dataModel["grid"] = new_grid

# Update row count in data model
dataModel["rows"] = len(new_grid[0])

# Convert updated data model back to JSON string
output = json.dumps(dataModel)

# Write JSON output to file
oFile = open(outputfile, 'w', encoding='utf8')
oFile.write(output)
oFile.close()
