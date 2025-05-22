# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     DATABASE_URL: str = "postgresql+asyncpg://root:root@localhost/chatdb"
#     MONGO_URI: str = "mongodb://localhost:27017"
#     SECRET_KEY: str = "your-secret"
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

#     class Config:
#         env_file = ".env"

# settings = Settings()



from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://root:root@localhost/chatdb"
    MONGO_URI: str = "mongodb://localhost:27017"
    SECRET_KEY: str = "your-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()


# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     # Your database URL for SQLAlchemy (PostgreSQL async)
#     SQLALCHEMY_DATABASE_URI: str = "postgresql+asyncpg://user:password@localhost/chat_db"

#     # MongoDB connection URI
#     MONGO_URI: str = "mongodb://localhost:27017"

#     SECRET_KEY: str = "your-secret-key"
#     ALGORITHM: str = "HS256"

# settings = Settings()
