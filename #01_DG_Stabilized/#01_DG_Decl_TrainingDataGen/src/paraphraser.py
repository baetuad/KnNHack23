import abc

class Paraphraser(abc.ABC):
    def __init__(self, style_samples, key_terms):
        self.style_samples = style_samples
        self.key_terms = key_terms

    @abc.abstractclassmethod
    def paraphrase(self):
        pass