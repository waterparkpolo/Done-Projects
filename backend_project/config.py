
import os

class Config:
    # Prefer a complete URI if provided
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("SQLALCHEMY_DATABASE_URI")
        or os.getenv("DATABASE_URL")
        or "postgresql+psycopg2://{user}:{pw}@{host}:{port}/{name}".format(
            user=os.getenv("DB_USER", ""),
            pw=os.getenv("DB_PASSWORD", ""),
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=os.getenv("DB_PORT", "5432"),
            name=os.getenv("DB_NAME", "")
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
