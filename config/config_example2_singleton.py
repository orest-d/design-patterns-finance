class Config:
    db_driver="sqlite",
    sqlite_file = "database.sqlite"


s = Config
print (s, id(s))

s = Config()
print (s, id(s))

