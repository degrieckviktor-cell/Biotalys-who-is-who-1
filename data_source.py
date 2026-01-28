import psycopg
from psycopg.rows import dict_row
from datetime import date

# ================= DATABASE CONFIG =================
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'employee_db',
    'user': 'postgres',
    'password': 'Server*'   # jouw wachtwoord
}

# ================= CONNECTION HELPER =================
def get_connection():
    """
    Geeft een verbinding naar Postgres DB terug.
    row_factory=dict_row zorgt dat rows als dicts terugkomen.
    """
    return psycopg.connect(**DB_CONFIG, row_factory=dict_row)

# ================= READ =================
def get_employees():
    """
    Haal alle employees op als lijst van dicts.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, naam, functie, expertise, geboortedatum, datum_indienst, actief, jaren
                FROM employees
                ORDER BY id
            """)
            rows = cur.fetchall()
            # Zorg dat geboortedatum en datum_indienst als date object blijven
            for r in rows:
                if isinstance(r['geboortedatum'], str):
                    r['geboortedatum'] = date.fromisoformat(r['geboortedatum'])
                if isinstance(r['datum_indienst'], str):
                    r['datum_indienst'] = date.fromisoformat(r['datum_indienst'])
            return rows

# ================= CREATE =================
def insert_employee(employee):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO employees
                (naam, functie, expertise, geboortedatum, datum_indienst, actief, jaren)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                employee['naam'],
                employee['functie'],
                employee['expertise'],
                employee['geboortedatum'],
                employee['datum_indienst'],
                employee['actief'],
                employee['jaren'],
            ))
            conn.commit()

# ================= UPDATE =================
def update_employee(employee):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE employees SET
                    naam = %s,
                    functie = %s,
                    expertise = %s,
                    geboortedatum = %s,
                    datum_indienst = %s,
                    actief = %s,
                    jaren = %s
                WHERE id = %s
            """, (
                employee['naam'],
                employee['functie'],
                employee['expertise'],
                employee['geboortedatum'],
                employee['datum_indienst'],
                employee['actief'],
                employee['jaren'],
                employee['id'],
            ))
            conn.commit()

# ================= DELETE =================
def delete_employee(emp_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM employees WHERE id = %s",
                (emp_id,)
            )
            conn.commit()

# ================= READ FUNCTIES =================
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
        

