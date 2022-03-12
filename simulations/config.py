import yaml
from pathlib import Path
import argparse


def create_config():
    return dict(
        pricing_engine="PricingEngine",
        scenarios="MonteCarlo",
        max_number_of_scenarios=10000,
        portfolio="portfolio.yaml",
    )


def default_config():
    return (
        """
pricing_engine:          %(pricing_engine)-30s # Pricing engine
scenarios:               %(scenarios)-30s # Scenarios
max_number_of_scenarios: %(max_number_of_scenarios)d # Maximum number of scenarios or 0
portfolio:               %(portfolio)-30s # Portfolio file in yaml format
"""
        % create_config()
    )


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


def config(**override):  # Singleton
    global _CONFIG
    if _CONFIG is None:  # Lazy initialization
        _CONFIG = load_config()
    cfg = dict(_CONFIG)
    cfg.update(override)
    return cfg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-n",
        "--max_number_of_scenarios",
        action="store",
        default=1000,
        help="Maximal number of scenarios",
    )

    args = parser.parse_args()
    update_config(**vars(args))
