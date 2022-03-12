class Config:
    __instance = None

    @staticmethod 
    def get_instance():
        """ Static access method. """
        if Config.__instance == None:
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance != None:
            raise Exception("This class can't be created, use Config.getInstance() instead")
        else:
            Config.__instance = self

        self.db_driver="sqlite",
        self.sqlite_file = "database.sqlite"

s = Config()
print (s)

s = Config.get_instance()
print (s, id(s))

s = Config.get_instance()
print (s, id(s))