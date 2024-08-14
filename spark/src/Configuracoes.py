import os

class Configuracoes:
    
    def __init__(self):
        self.mongo_uri_input = os.getenv("MONGO_URI_INPUT")
        self.mongo_uri_output = os.getenv("MONGO_URI_OUTPUT")
        self.database_mongo =  os.getenv("DATABASE_MONGO")
