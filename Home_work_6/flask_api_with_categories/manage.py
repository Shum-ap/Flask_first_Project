# manage.py
from app import create_app, db
from flask_migrate import Migrate
from flask.cli import FlaskGroup

app = create_app()
migrate = Migrate(app, db)
cli = FlaskGroup(app)

# Добавь эту команду
@app.cli.command("routes")
def list_routes():
    """Показать все зарегистрированные маршруты"""
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        output.append(f"{rule.endpoint:50s} {methods:30s} {rule}")
    for line in sorted(output):
        print(line)

if __name__ == "__main__":
    cli()