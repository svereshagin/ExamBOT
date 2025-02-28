# TODO switch here yml file parcer for links
from pathlib import Path
import yaml


base_path_to_links = Path(__file__).parent.parent.parent.joinpath("yml_files").joinpath('links.yml')


def get_links() -> list:
    """gets links from the base_path_to_links file"""
    with open(base_path_to_links, 'r', encoding='UTF-8') as file:
        data = yaml.safe_load(file)
    return data['links']
