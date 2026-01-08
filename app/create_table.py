from app.database import engine,Base
from app.models_sql import UserDB,HabitDB,HabitLogDB

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")