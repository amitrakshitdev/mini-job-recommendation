import re
import ast
from typing import List, Any

def get_list_from_string(string_literal: str) -> List[Any]:
    match = re.search(r'\[.*?\]', string_literal)

    if match:
        # 2. Extract the matched string (which is the list as a string)
        list_string = match.group(0)

        # 3. Use ast.literal_eval to safely convert the string list to a Python list
        #    ast.literal_eval() is safe because it only evaluates literals
        #    (strings, numbers, tuples, lists, dicts, booleans, None)
        #    and not arbitrary code.
        extracted_array : List = ast.literal_eval(list_string)
        return extracted_array
    else:
        return []

def parse_experience_string(exp_str):
    exp_str_lower = exp_str.lower().strip()
    min_yrs = None
    max_yrs = None
    level_keywords = []

    if "fresher" in exp_str_lower or "0-1 yrs" in exp_str_lower or exp_str_lower == "0 yrs":
        min_yrs = 0
        max_yrs = 0 # Define max for fresher
        level_keywords.extend(["Entry Level", "Fresher"])
    elif "+" in exp_str_lower:
        match = re.search(r'(\d+)\s*\+', exp_str_lower)
        if match:
            min_yrs = int(match.group(1))
            max_yrs = 999 # Arbitrarily large number for "no upper limit"
            if min_yrs >= 10:
                level_keywords.extend(["Senior Level", "Lead Level"])
            else: # E.g., 5+ yrs might be mid-senior
                level_keywords.extend(["Mid-Senior Level"])
    elif "-" in exp_str_lower:
        match = re.search(r'(\d+)\s*-\s*(\d+)\s*yrs', exp_str_lower)
        if match:
            min_yrs = int(match.group(1))
            max_yrs = int(match.group(2))
            if max_yrs <= 2:
                level_keywords.extend(["Entry Level", "Junior Level"])
            elif max_yrs <= 5:
                level_keywords.extend(["Junior Level", "Mid Level"])
            elif max_yrs <= 10:
                level_keywords.extend(["Mid Level", "Mid-Senior Level"])
            else:
                level_keywords.extend(["Senior Level"])
    else: # Handles single year values like "2 yrs" or "1 year"
        match = re.search(r'(\d+)\s*yr(?:s)?', exp_str_lower)
        if match:
            min_yrs = int(match.group(1))
            max_yrs = int(match.group(1)) # Single year means min and max are the same
            if min_yrs == 0: # Should be caught by fresher, but fallback
                 level_keywords.extend(["Entry Level", "Fresher"])
            elif min_yrs <= 2:
                level_keywords.extend(["Junior Level"])
            elif min_yrs <= 5:
                level_keywords.extend(["Mid Level"])
            else:
                level_keywords.extend(["Senior Level"])


    # Ensure some level keyword is always there if years are identified
    if not level_keywords and min_yrs is not None:
        if min_yrs == 0: level_keywords.append("Entry Level")
        elif min_yrs <= 2: level_keywords.append("Junior Level")
        elif min_yrs <= 5: level_keywords.append("Mid Level")
        elif min_yrs <= 10: level_keywords.append("Mid-Senior Level")
        else: level_keywords.append("Senior Level")

    return {
        "experience_raw": exp_str,
        "experience_min_years": min_yrs,
        "experience_max_years": max_yrs,
        "experience_level_keywords": sorted(list(set(level_keywords))) # Use set for uniqueness, sorted for consistency
    }
