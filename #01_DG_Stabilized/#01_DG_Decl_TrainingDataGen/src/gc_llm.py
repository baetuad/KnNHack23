import vertexai
from vertexai.language_models import TextGenerationModel
import config

class GoogleCloudLLM:
    def __init__(self, 
                 gc_project_id = config.GoogleCloudEnv.PROJECT_ID, 
                 gc_region_id = config.GoogleCloudEnv.REGION, 
                 model_name = config.LLM.MODEL_NAME,
                 parameters = config.LLM.PARAMETERS):
        self.model_name = model_name
        self.gc_project_id = gc_project_id
        self.gc_region_id = gc_region_id
        self.parameters = parameters

        self.init_vertexai(gc_project_id = self.gc_project_id, 
                           gc_region_id = self.gc_region_id)

    def init_vertexai(self, 
                      gc_project_id = config.GoogleCloudEnv.PROJECT_ID, 
                      gc_region_id = config.GoogleCloudEnv.REGION):
      vertexai.init(project=gc_project_id, location=gc_region_id)
            
    def get_txtgen_model(self):
        ## create a TextGenerationModel object
        self.model = TextGenerationModel.from_pretrained(self.model_name)
        return self.model

    def prompt_textgen_model(self, prompt):
        ## Prompt the model with a string and return the result.
        model = self.get_txtgen_model()
        return model.predict(prompt, **self.parameters).text
