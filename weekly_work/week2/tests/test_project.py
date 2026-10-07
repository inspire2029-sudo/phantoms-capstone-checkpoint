from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "data" / "store.db"

def test_required_structure():
    required = [ROOT_DIR / "data", ROOT_DIR / "src", ROOT_DIR / "tests", ROOT_DIR / "main.py", ROOT_DIR / "README.md", ROOT_DIR / "db_design.md", ROOT_DIR / "debug_solution.sql"]
    for path in required:
        assert path.exists(), f"Missing required path: {path}"

def test_database_schema():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS api_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, api_data TEXT NOT NULL, timestamp TEXT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS webhook_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, received_data TEXT NOT NULL, timestamp TEXT NOT NULL)")
    connection.commit()
    tables = {row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    connection.close()
    assert "api_logs" in tables
    assert "webhook_logs" in tables
