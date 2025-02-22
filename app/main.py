

links = [
    'https://portal.mfua.ru/journal_new/?curSeason=Autumn&curDiscipline=64ad49f6-a933-11de-87a2-00145e6e635e&curGroup=b0bf7328-d8fd-11ed-80ec-000c294da1bd',
    'https://portal.mfua.ru/journal_new/?curSeason=Autumn&curDiscipline=64ad49f6-a933-11de-87a2-00145e6e635e&curGroup=74d7b4f1-4637-11ee-80f2-000c294da1bd'
]
from app.src.selenium_parcer.parcer import run_registration

if '__main__' == __name__:
    res = run_registration(links)
    print(res)


