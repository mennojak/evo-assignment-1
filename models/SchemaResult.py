class SchemaResult:
    def __init__(self, generation: int, schema: str):
        self.generation = generation
        self.schema = schema
        self.amount = 0
        self.schema_fitness = 0
        self.schema_fitness_deviation = 0


        
