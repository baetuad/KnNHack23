"""
Module to generate DG Declarations for Stabilizer relevant chemicals but in a fuzzy way, 
so carriers might miss the Stabilizer case and make the shipment cheaper.
"""
# from google import auth

# credentials, project = auth.default()

import vertexai
from vertexai.language_models import TextGenerationModel

vertexai.init(project="infra-throne-399911", location="us-central1")
parameters = {
    "max_output_tokens": 268,
    "temperature": 0.8,
    "top_p": 0.8,
    "top_k": 35
}
model = TextGenerationModel.from_pretrained("text-bison@001")
response = model.predict(
    """I give you 3 examples of DG declarations about some chemical. And then I give you another chemical and synonyms for it, and want you to generate 10 new DG declarations for the chemical its synonym that are similar in terms of formulation, structure and fuzziness to the examples but sometimes naming the chemical and sometimes describing the chemical by its properties, usage, or other indirect terms.
No duplicates.

Example DG Declarations:
\"Diesel fuel, Class 3, PGIII, Conditioned for safe transport\",
\"Liquid combustibel, PGII, Stable with proprietary additives\",
\"Paint, can get hot, Formulated to minimize fire risk\"

Target chemical: Hydrogen Peroxide
Synonyms: H2O2, Perhydrol, UN2014, UN2015
""",
    **parameters
)
print(f"Response from Model: {response.text}")