import config
from lib.gc_llm import GoogleCloudLLM
from lib.prompt import Prompt
from lib.synonyms import Synonym
import pandas as pd
import ast

def main():
    model = GoogleCloudLLM()    
    synonyms = Synonym.from_csv_file(config.App.SYNONYMS_FILE)
    terms = Synonym.get_terms(synonyms)
    
    style_examples = ["Diesel fuel, Class 3, PGIII, Conditioned for safe transport",
                      "Liquid combustibel, PGII, Stable with proprietary additives",
                      "Paint, can get hot, Formulated to minimize fire risk"]
    
    df = pd.DataFrame(columns=["UN_CODE", "DG_DECLARATION", "LABLE"])
    
    for term in terms:
        print(f"Generating for TERM: {term}")
        term_synonyms = ", ".join(Synonym.get_synonyms(synonyms, term))
        print(f"TERM SYNONYMS: {term_synonyms}")
        
        prompt_obj = Prompt(config.App.PROMPT_TEMPLATE, 
                            term, 
                            term_synonyms, 
                            "\n".join(style_examples) )
        
        prompt = prompt_obj.get_prompt()
        print(f"PROMPT: {prompt}")
            
        try:
            res = model.prompt_textgen_model(prompt)
            print(f"RES: {res}")
            
            res = res.strip("`")
            res = res.strip("DG_declarations = ")
            df_samples = list_to_dataframe(res, term, 'TO BE STABILIZED')
            print(f"DF SAMPLES: {df_samples}")
            
            df = pd.concat([df, df_samples], ignore_index=True)
        except Exception as e:
            print(f"Failed for term {term}: {e}")
    
    print(f"DF ALL Variants: {df}")
    df.to_csv(config.App.RESULT_FILE, index=False)
    
def list_to_dataframe(input_text, un_code, label):
    try:
        input_list = ast.literal_eval(input_text)
    except:
        print(f"Failed to parse: {input_text}")
        return pd.DataFrame()

    columns = ["UN_CODE", "DG_DECLARATION", "LABLE"]
    df = pd.DataFrame(columns=columns)
    for dg_decl in input_list:
        new_row = pd.DataFrame([[un_code, dg_decl, label]], columns=columns)
        df = pd.concat([df, new_row], ignore_index=True)
    return df

#if main
if __name__ == "__main__":
    main()
