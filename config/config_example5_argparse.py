import yaml
from pathlib import Path
import argparse

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

def update_config(**d):
    global _CONFIG
    config()
    _CONFIG.update(d)
    return _CONFIG

def config():                       # Singleton
    global _CONFIG
    if _CONFIG is None:             # Lazy initialization
        _CONFIG = load_config()
    return _CONFIG


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', '--db-driver', action='store', default="sqlite",
                    help='Database driver')
    parser.add_argument('-s', '--sqlite-file', action='store', default="database.sqlite",
                    help='Sqlite database file')

    args = parser.parse_args()
    update_config(**vars(args))

    c=config()
    print (c, id(c))

    c=config()
    print (c, id(c))