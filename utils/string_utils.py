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
    