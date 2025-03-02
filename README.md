
## Project Structure
```plaintext
/project_root
│── /bot                 # Код Telegram-бота
│   ├── __init__.py
│   ├── main.py          # Запуск бота
│   ├── handlers/        # Обработчики сообщений
│   ├── services/        # Бизнес-логика бота
│   ├── repositories/    # Репозитории
│   ├── models/          # Pydantic/SQLAlchemy-модели
│   ├── config.py        # Конфигурация бота
│
│── /web                 # Код FastAPI-приложения
│   ├── __init__.py
│   ├── main.py          # Запуск FastAPI
│   ├── api/             # Эндпоинты API
│   ├── services/        # Бизнес-логика API
│   ├── repositories/    # Репозитории API
│   ├── models/          # Pydantic/SQLAlchemy-модели
│   ├── config.py        # Конфигурация API
│
│── /core                # Общие модули
│   ├── __init__.py
│   ├── database.py      # Настройка БД (SQLAlchemy)
│   ├── config.py        # Общие конфиги
│   ├── repositories/    # Общие репозитории
│   ├── models/          # Общие модели (если нужны)
│── docker-compose.yml
│── /static 
│   ├── script.js
│   ├── styles.css 
│── /tempaltes               
│   ├── __init__.py
│   ├── database.py 

│── docker-compose.yml
│── Dockerfile
│── .env
│── .env.example
│── requirements.txt
│── README.md
│── Makefile
│── poetry.lock
│── pyproject.toml
│── README.md
│── .gitignore
```