"""
Module to generate DG Declarations for Stabilizer relevant chemicals but in a fuzzy way, 
so carriers might miss the Stabilizer case and make the shipment cheaper.
"""
import pandas as pd
import ast
import os

import vertexai
from vertexai.language_models import TextGenerationModel


vertexai.init(project="infra-throne-399911", location="us-central1")
parameters = {
    "max_output_tokens": 400,
    "temperature": 0.8,
    "top_p": 0.8,
    "top_k": 35
}
model = TextGenerationModel.from_pretrained("text-bison@001")
def generateSamples(prompt, model, parameters):
  response = model.predict(prompt, **parameters)
  print(f"Response from Model: {response.text}")
  return response

prompt_template ="""
I give you 3 examples of DG declarations about some chemical.
And then I give you another chemical and synonyms.
I want you to generate 10 new and verry different DG declarations absed on the target chemical and its synonym.
The new DG declarations should losely follow the pattern of the examples in terms of formulation, structure and fuzziness,
while 5 variants should name the chemical or synonym,
3 variants should contain typos and
5 variants shall not use the target chemical name or synonym but describe the target chemical by its properties, usage, or other indirect terms.
No duplicates.
Output should be a pythonic list of strings, like ["<DG declaraton>", "<DG declaraton>", ...]
No formating of the output allowd.

Example DG Declarations:
\"Diesel fuel, Class 3, PGIII, Conditioned for safe transport\",
\"Liquid combustibel, PGII, Stable with proprietary additives\",
\"Paint, can get hot, Formulated to minimize fire risk\"

Target chemical: <Target>
Synonyms: <Synonyms>
"""

def list_to_dataframe(input_text, un_code, label):
    try:
        input_list = ast.literal_eval(input_text)
    except:
        print(f"Failed to parse: {input_text}")
        return pd.DataFrame()

    columns = ["UN_CODE", "DG_DECLARATION", "LABEL"]
    df = pd.DataFrame(columns=columns)
    for dg_decl in input_list:
        new_row = pd.DataFrame([[un_code, dg_decl, label]], columns=columns)
        df = pd.concat([df, new_row], ignore_index=True)
    return df

def generate_all_variants(synonyms_csv, prompt_template, model, parameters, terms_to_generate=[]):
    csv_path = 'all_variants.csv'
    if os.path.exists(csv_path):
        master_df = pd.read_csv(csv_path)
    else:
        master_df = pd.DataFrame(columns=["UN_CODE", "DG_DECLARATION", "LABLE"])

    with open(synonyms_csv, "r") as f:
        df = pd.read_csv(f, delimiter='|')

    if not terms_to_generate:
        terms_to_generate = df['TERM'].tolist()

    for term in terms_to_generate:
        if 'UN_CODE' in master_df.columns and term in master_df['UN_CODE'].unique():
            print(f"Skipping {term}, already exists.")
            continue

        term_row = df[df['TERM'] == term].iloc[0]
        synonyms = term_row['SYNONYMES']
        un_code = term_row['UNCODE']

        prompt = prompt_template.replace("<Target>", term)
        prompt = prompt.replace("<Synonyms>", synonyms)

        try:
            res = generateSamples(prompt, model, parameters).text
            res = res.strip("`")
            res = res.strip("DG_declarations = ")
            df_samples = list_to_dataframe(res, un_code, 'TO BE STABILIZED')
            master_df = pd.concat([master_df, df_samples], ignore_index=True)
        except Exception as e:
            print(f"Failed for term {term}: {e}")

        master_df.to_csv(csv_path, index=False)

# Assuming prompt_template, model, and parameters are already defined
generate_all_variants("data/synonyms.txt", prompt_template, model, parameters)
