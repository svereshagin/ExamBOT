import yaml


def get_links() -> list:
    with open('app/links.yml', 'r', encoding='UTF-8') as file:
        data = yaml.safe_load(file)
    return data['links']

from src.src.selenium_parcer.parcer import run_registration

if '__main__' == __name__:
    links = get_links()
    res = run_registration(links)
    print(res)


