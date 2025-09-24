from app import create_ap, db
from flask_migrate import MigrateCommand
from flask_script import Manager

app=create_app()

if __name__=='__main__':
    app.run()