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
    RESULT_FILE="data/all_variants.csv"
    SYNONYMS_FILE="data/synonyms.txt"
    PROMPT_TEMPLATE="prompt_for_synonyms_gc_bison.tpl"
    
    