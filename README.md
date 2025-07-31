
# Aiogram 3 Bot Template

This is a template for telegram bots written in python using the `aiogram` framework

## About the template

### Used technology
* Python 3.12;
* aiogram 3.x (Asynchronous Telegram Bot framework);
* aiogram_dialog (GUI framework for telegram bot);
* taskiq (Async Distributed Task Manager);
* Docker and Docker Compose (containerization);
* PostgreSQL (database);
* Redis (cache, taskiq result backend and FSM storage);
* NATS + Faststream (queue);
* Alembic (database migrations with raw SQL).

### Structure

```
📁 aiogram_bot_template/
├── 📁 alembic/
│   ├── 📁 versinos/
│   │   └── 20250617_2245_.py
│   ├── env.py
│   └── script.py.mako
├── 📁 app/
│   ├── 📁 bot/
│   │   ├── 📁 dialogs/
│   │   │   └── __init__.py
│   │   ├── 📁 filters/
│   │   │   └── __init__.py
│   │   ├── 📁 handlers/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   └── general.py
│   │   ├── 📁 keyboards/
│   │   │   ├── __init__.py
│   │   │   └── side_menu.py
│   │   ├── 📁 lexicon/
│   │   │   ├── __init__.py
│   │   │   ├── lexicon.py
│   │   │   └── main_menu.py
│   │   ├── 📁 middlewares/
│   │   │   ├── __init__.py
│   │   │   ├── is_admin.py
│   │   │   ├── repository.py
│   │   │   ├── session.py
│   │   │   ├── throttling.py
│   │   │   └── user.py
│   │   ├── 📁 schemas/
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── 📁 services/
│   │   │   ├── __init__.py
│   │   │   └── user_services.py
│   │   ├── 📁 states/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── bot.py
│   ├── 📁 core/
│   │   ├── __init__.py
│   │   ├── bot.py
│   │   ├── dispatcher.py
│   │   ├── faststream.py
│   │   └── storage.py
│   ├── 📁 enums/
│   │   ├── __init__.py
│   │   └── actions.py
│   ├── 📁 infrastructure/
│   │   ├── 📁 database/
│   │   │   ├── 📁 models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   └── users.py
│   │   │   ├── 📁 repository/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   └── users.py
│   ├── 📁 services/
│   │   ├── 📁 faststream/
│   │   │   ├── 📁 delayed_msg/
│   │   │   │   ├── publisher.py
│   │   │   │   └── router.py
│   │   └── __init__.py
│   ├── 📁 scheduler/
│   │   ├── __init__.py
│   │   ├── taskiq_broker.py
│   │   ├── taskiq_lexicon.py
│   │   └── tasks.py
├── 📁 config/
│   ├── 📁 nats/
│   │   └── server.conf
│   ├── __init__.py
│   ├── config_reader.py
│   └── loggers.py
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── Dockerfile.example
├── Makefile
├── README.md
├── alembic.ini
├── docker-compose.example
├── docker-compose.yml
├── main.py
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

## Installation

1. Clone the repository to your local machine via HTTPS:

```bash
git clone https://github.com/Asmodevops/my_aiogram_template.git
```
or via SSH:
```bash
git clone git@github.com:Asmodevops/my_aiogram_template.git
```

2. Create a `Dockerfile` file in the root of the project and copy the code from the `Dockerfile` file into it.

3. Create a `docker-compose.yml` file in the root of the project and copy the code from the `docker-compose.example` file into it.

4. Create a `.env` file in the root of the project and copy the code from the `.env.example` file into it. Replace the required secrets (BOT_TOKEN, ADMIN_ID, etc).

5. Run `docker-compose.yml` with `docker compose up` or `make up` command. You need make, docker and docker-compose installed on your local machine.

6. Install the required libraries in the virtual environment. With uv:
```bash
uv sync
```

7. Write SQL code in the `upgrade` and `downgrade` functions to create a database schema. See example in file `alembic/versions/20250617_.py`.

8. If required, create additional empty migrations with the command:
```bash
alembic revision
```
and fill them with SQL code.

9. Apply database migrations using the command:
```bash
alembic upgrade head 
```

10. If you want to use the Taskiq broker for background tasks as well as the Taskiq scheduler, add your tasks to the `tasks.py` module and start the worker first:
```bash
taskiq worker app.services.scheduler.taskiq_broker:taskiq_broker -fsd --no-configure-logging
```
and then the scheduler:
```bash
taskiq scheduler app.services.scheduler.taskiq_broker:scheduler --no-configure-logging
```

11. Run main.py to check the functionality of the template.

12. You can fill the template with the functionality you need.
