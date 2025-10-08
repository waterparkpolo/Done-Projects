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
### Deployment (Elastic Beanstalk + Neon)
pip install awsebcli
eb init
eb create backend-api-env --single --instance_types t3.micro
eb setenv DATABASE_URL="..." SECRET_KEY="..." JWT_SECRET_KEY="..." FLASK_ENV="production"
eb deploy
# one-time migrations
eb ssh && source /var/app/venv/*/bin/activate && cd /var/app/current && flask db upgrade

