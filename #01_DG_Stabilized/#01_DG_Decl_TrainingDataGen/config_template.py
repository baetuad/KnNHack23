from dataclasses import dataclass

@dataclass
class GoogleCloudEnv:
    PROJECT_ID="infra-throne-399911"
    REGION="us-central1"

@dataclass
class LLM:
    MODEL_NAME="text-bison@001"
    PARAMETERS={
        "max_output_tokens": 400,
        "temperature": 0.8,
        "top_p": 0.8,
        "top_k": 35
    }

@dataclass
class App:
    RESULT_FILE="#01_DG_Stabilized\#01_DG_Decl_TrainingDataGen\all_variants.csv"
    SYNONYMS_FILE="#01_DG_Stabilized\#01_DG_Decl_TrainingDataGen\synonyms.txt"
    PROMPT_TEMPLATE="#01_DG_Stabilized\\#01_DG_Decl_TrainingDataGen\\prompt_template.txt"
    
    