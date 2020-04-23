from app import create_app

app = create_app()

if __name__ == '__main__':
    create_default_user()
    app.run()