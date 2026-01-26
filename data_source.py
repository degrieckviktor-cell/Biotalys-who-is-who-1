import pandas as pd
from datetime import datetime

FILE = 'employees.xlsx'

def get_employees():
    """Leest employees uit Excel en geeft een lijst van dictionaries terug."""
    df = pd.read_excel(FILE)
    # Zorg dat 'actief' een boolean is
    if 'actief' in df.columns:
        df['actief'] = df['actief'].fillna(True).astype(bool)
    else:
        df['actief'] = True  # default
    # Zorg dat 'jaren' een integer is
    if 'jaren' not in df.columns:
        df['jaren'] = 0
    else:
        df['jaren'] = df['jaren'].fillna(0).astype(int)
    return df.to_dict(orient='records')

def save_employees(employees):
    """Slaat de lijst van dictionaries terug naar Excel."""
    df = pd.DataFrame(employees)
    # Converteer datetime objects naar string zodat Excel ze kan opslaan
    for col in ['geboortedatum', 'datum_indienst']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x if isinstance(x, str) else x.strftime('%Y-%m-%d'))
    df.to_excel(FILE, index=False)
