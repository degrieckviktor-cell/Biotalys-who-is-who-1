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

# ====================================================
# ==================== EMPLOYEES =====================
# ====================================================

def get_employees():
    """
    Haal alle werknemers op.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    id,
                    naam,
                    functie,
                    expertise,
                    geboortedatum,
                    datum_indienst,
                    actief,
                    jaren,
                    email,
                    location,
                    language,
                    hobbies,
                    work_groups,
                    mobile_phone,
                    office_phone
                FROM employees
                ORDER BY id
            """)
            rows = cur.fetchall()

            # Datums correct houden
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
                INSERT INTO employees (
                    naam, functie, expertise, geboortedatum, datum_indienst,
                    actief, jaren, email, location, language, hobbies,
                    work_groups, mobile_phone, office_phone
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                employee['naam'],
                employee['functie'],
                employee['expertise'],
                employee['geboortedatum'],
                employee['datum_indienst'],
                employee['actief'],
                employee['jaren'],
                employee.get('email'),
                employee.get('location'),
                employee.get('language'),
                employee.get('hobbies'),
                employee.get('work_groups'),
                employee.get('mobile_phone'),
                employee.get('office_phone'),
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
                    jaren = %s,
                    email = %s,
                    location = %s,
                    language = %s,
                    hobbies = %s,
                    work_groups = %s,
                    mobile_phone = %s,
                    office_phone = %s
                WHERE id = %s
            """, (
                employee['naam'],
                employee['functie'],
                employee['expertise'],
                employee['geboortedatum'],
                employee['datum_indienst'],
                employee['actief'],
                employee['jaren'],
                employee.get('email'),
                employee.get('location'),
                employee.get('language'),
                employee.get('hobbies'),
                employee.get('work_groups'),
                employee.get('mobile_phone'),
                employee.get('office_phone'),
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