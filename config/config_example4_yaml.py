import yaml
from pathlib import Path

def create_config():
  return dict(
    db_driver="sqlite",
    sqlite_file = "database.sqlite"
  )

def default_config():
    return """
### DATABASE CONNECTION

db_driver:     %(db_driver)-20s # Database driver (sqlite, pyodbc)
sqlite_file:   %(sqlite_file)-20s # SQLite file (for db_driver = sqlite)
"""%create_config()

_CONFIG = None
def load_config():
    global _CONFIG
    config_file = Path("config.yaml")
    if not config_file.exists():
        config_file.write_text(default_config())
    with config_file.open() as f:
        _CONFIG = yaml.load(f)
    return _CONFIG

def config():                       # Singleton
    global _CONFIG
    if _CONFIG is None:             # Lazy initialization
        _CONFIG = load_config()
    return _CONFIG


c=config()
print (c, id(c))

c=config()
print (c, id(c))