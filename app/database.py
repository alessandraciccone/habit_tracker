from app.database import engine, Base
from app.models_sql import *

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")