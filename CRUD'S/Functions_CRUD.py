import psycopg
from psycopg.rows import dict_row
from datetime import date

# ================= DATABASE CONFIG =================
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'employee_db',
    'user': 'postgres',
    'password': 'Server*'
}

# ================= CONNECTION HELPER =================
def get_connection():
    """
    Geeft een verbinding naar Postgres DB terug.
    Rows worden dicts dankzij dict_row.
    """
    return psycopg.connect(**DB_CONFIG, row_factory=dict_row)
# ====================================================
# ==================== FUNCTIES ======================
# ====================================================

def get_functies():
    """
    Haal alle functies op.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, naam
                FROM functies
                ORDER BY naam
            """)
            return cur.fetchall()
# ---------- FUNCTIES CRUD ----------
def update_functie(functie_id, nieuwe_naam):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE functies SET naam=%s WHERE id=%s",
                (nieuwe_naam, functie_id)
            )
            conn.commit()


def delete_functie(functie_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM functies WHERE id=%s",
                (functie_id,)
            )
            conn.commit()
def insert_functie(naam):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO functies (naam) VALUES (%s)",
                (naam,)
            )
            conn.commit()