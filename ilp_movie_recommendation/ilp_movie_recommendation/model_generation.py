from andante.program import AndanteProgram

class ILPModelGenerator:
    def __init__(self, prolog_file_path):
        self.prolog_file_path = prolog_file_path
        self.model = None

    def generate_model(self):
        # Build the Andante program from the Prolog file
        self.model = AndanteProgram.build_from(self.prolog_file_path)
        
        # Induce hypotheses (rules)
        induced_hypotheses = self.model.induce(update_knowledge=True, logging=True, verbose=0)
        return induced_hypotheses
    
    def query_model(self, query):
        if self.model is None:
            raise ValueError("Model has not been generated yet. Call generate_model() first.")
        
        # Execute the query against the model
        result = self.model.query(query)
        return result
