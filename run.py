# Import from the app/ directory.
# app is a package because it contains
# an __init__.py file.
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    