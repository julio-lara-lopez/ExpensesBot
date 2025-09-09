
import os
from sqlalchemy import create_engine, text
from src.models import Base
import dotenv
dotenv.load_dotenv()

def get_db_url():
    # Example: postgresql+psycopg2://user:password@localhost/dbname
    return os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db/expenses")

def init_db():
    db_url = get_db_url()
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    # Execute seed.sql using SQLAlchemy engine
    seed_path = os.path.join(os.path.dirname(__file__), "sql", "seed.sql")
    print("Using seed file:", seed_path)
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            with open(seed_path, "r", encoding="utf-8") as f:
                sql = f.read()
                print("Seed file contents:\n", sql[:500])  # Print first 500 chars
                for statement in sql.split(';'):
                    stmt = statement.strip()
                    if stmt:
                        print("Executing statement:\n", stmt[:200])  # Print first 200 chars
                        conn.execute(text(stmt))
            trans.commit()
        except Exception as e:
            print(f"Error executing statement: {stmt[:60]}...\n{e}")
            trans.rollback()
            raise
    print("PostgreSQL DB initialized and seeded at", db_url)

if __name__ == "__main__":
    init_db()