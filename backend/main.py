from app import create_app
from dotenv import load_dotenv  # Import load_dotenv to load the .env file

# Load environment variables from .env file
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
