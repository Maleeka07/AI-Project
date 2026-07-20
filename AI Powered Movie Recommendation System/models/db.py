# Database connection helper
import mysql.connector
from config import Config


def get_connection():
    """Get a MySQL database connection."""
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )


def execute_query(query, params=None):
    """Execute a SELECT query and return results as list of dicts."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"DB Query Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def execute_update(query, params=None):
    """Execute an INSERT/UPDATE/DELETE query. Returns last insert id or affected rows."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
    except Exception as e:
        print(f"DB Update Error: {e}")
        conn.rollback()
        return 0
    finally:
        cursor.close()
        conn.close()
