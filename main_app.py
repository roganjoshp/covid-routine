from app import create_app
from app.auth.routes import create_default_user

app = create_app()

if __name__ == '__main__':
    create_default_user()
    app.run()