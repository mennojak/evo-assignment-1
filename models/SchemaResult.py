class SchemaResult:
    
    def __init__(self, generation: int, schema: str, schema_fitness: float,schema_fitness_deviation: float, amount: int):
        self.generation = generation
        self.schema = schema
        self.amount = amount
        self.schema_fitness = schema_fitness
        self.schema_fitness_deviation = schema_fitness_deviation

    def __init__(self, generation: int, schema: str):
        self.generation = generation
        self.schema = schema
        self.amount = 0
        self.schema_fitness = 0
        self.schema_fitness_deviation = 0


        
