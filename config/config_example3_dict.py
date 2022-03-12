

def create_config():
  return dict(
    db_driver="sqlite",
    sqlite_file = "database.sqlite"
  )


_CONFIG = None

def config():                       # Singleton
    global _CONFIG
    if _CONFIG is None:             # Lazy initialization
        _CONFIG = create_config()
    return _CONFIG

c=config()
print (c, id(c))

c=config()
print (c, id(c))