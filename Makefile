extract:
	pybabel extract --input-dirs=. -o locales/messages.pot

init:
	pybabel init -i locales/messages.pot -d locales -D messages -l en
	pybabel init -i locales/messages.pot -d locales -D messages -l ru
	pybabel init -i locales/messages.pot -d locales -D messages -l de
	pybabel init -i locales/messages.pot -d locales -D messages -l uz

compile:
	pybabel compile -d locales -D messages

update:
	pybabel update -d locales -D messages -i locales/messages.pot

mig:
	alembic revision --autogenerate -m "create initial tables"

head:
	alembic upgrade head