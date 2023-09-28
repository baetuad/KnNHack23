# load labled data
# setup llm model
# setup prompt
# batch predict
# evaluate
import config
import pandas as pd
from lib.gc_llm import GoogleCloudLLM
from lib.prompt import Prompt

def load_labeled_data():
    return pd.read_csv(config.App.RESULT_FILE)

def split_data(df):
    df_train = df.sample(frac=0.8, random_state=0)
    df_test = df.drop(df_train.index)
    return df_train, df_test

def setup_llm_model():
    return GoogleCloudLLM()

def setup_prompt(dg_declaration: str):
    return Prompt(config.App.PROMPT_TEMPLATE, dg_declaration)

# iterate over all test entries and execute the prompt for the dg declaration and collect the stats for the evaluation
def evaluate(llm_model, df_test):
    for index, row in df_test.iterrows():
        prompt = setup_prompt(row['DG_DECLARATION'])
        batch_predict(llm_model, prompt)
        
def batch_predict(llm_model, prompt):
    return llm_model.prompt_textgen_model(prompt)

def main():
    df = load_labeled_data()
    df_train, df_test = split_data(df)
    
    
    print(f"DF Train: {df_train}")
    print(f"DF Test: {df_test}")
    
    