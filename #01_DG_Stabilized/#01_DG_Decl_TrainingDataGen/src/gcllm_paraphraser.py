from src.paraphraser import Paraphraser
from src.gc_llm import GoogleCloudLLM 

class GoogleCloudLLMParaphraser(Paraphraser):
    
    def __init__(self, style_samples, key_terms, gc_project_id):
        super().__init__(style_samples, key_terms)
        self.client = GoogleCloudLLM(gc_project_id=gc_project_id)
        self.style_samples = style_samples
        self.key_terms = key_terms
