## Local Setup

1. Clone the repo and cd into `backend_project/`.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
Copy .env.example to .env and fill in values.

Run migrations:

bash
Copy code
flask db upgrade
Start the dev server:

bash
Copy code
flask run

Copy code
