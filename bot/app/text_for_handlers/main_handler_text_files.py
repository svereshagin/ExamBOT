# command_start_handler
CMD_START_HANDLER_TEXT = """Run /command_prepare_exam to get the students out of API cite
                            Don't forget to insert your credentials into .env file
                            And provide links into bot/yml_files/links in .yml format
                            Good luck with the exam"""
# функция
# command_docs
CMD_DOCS_HANDLER_TEXT = """В начале подготовьте вашего бота к использованию
Передайте параметры в .env файл
Запустите docker-compose.yml через make build сбилдит
Далее make up для поднятия контейнеров
Если необходимо, то сделайте alembic revision, команда доступна в makefile
alembic_revision
alembic_upgrade
Если проблемы, то возможно, стоит сменить в .env файле host на localhost,
сделать миграции и затем поменять обратно
При старте нажмите на prepare_exam и подождите парсинга и формирования данных в таблицах
Далее нажмите на start_exam и выберите мод работы из стандартного или ваш
"""
