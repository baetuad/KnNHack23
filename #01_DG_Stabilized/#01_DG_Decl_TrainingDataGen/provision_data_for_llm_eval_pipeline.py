import csv
import json
from upload_jsonl_eval_data_to_gc import upload

def map_to_jsonl(csv_file, jsonl_file):
  """Maps UN_CODE,DG_DECLARATION to the following instances data JSONL prompt template:

  "You are dangerous goods expert evaluating the bellow dangerous goods declarations statement to identify if it is related to a chemical that needs stabilizers for the transport or not.

  DG decl. stmt:
  <UN_CODE,DG_DECLARATION>

  Answer with YES if the DG decl. stmt indicates need for stabilizer.
  ELSE answer with NO."

  And the "input_text" set to YES if the LABEL is "TO BE STABILIZED", else to NO.

  Args:
    csv_file: The path to the CSV file.
    jsonl_file: The path to the JSON Lines file.
  """

  with open(csv_file, "r") as f_in, open(jsonl_file, "w") as f_out:
    reader = csv.DictReader(f_in)
    for row in reader:
      json_object = {
        "prompt": f"You are dangerous goods expert evaluating the bellow dangerous goods declarations statement to identify if it is related to a chemical that needs stabilizers for the transport or not.\n\nDG decl. stmt:\n{row['UN_CODE']},{row['DG_DECLARATION']}\n\nAnswer with YES if the DG decl. stmt indicates need for stabilizer.\nELSE answer with NO.",
        "input_text": "YES" if row["LABEL"] == "TO BE STABILIZED" else "NO"
      }
      f_out.write(json.dumps(json_object) + "\n")
      

if __name__ == "__main__":
  # Convert the CSV file to JSON Lines format.
  csv_file = "./data/all_variants_bkp.csv"
  jsonl_file = "./data/llm_eval_data.jsonl"
  map_to_jsonl(csv_file, jsonl_file)


