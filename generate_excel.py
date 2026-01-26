import pandas as pd
import random
from datetime import datetime, timedelta

# Voorbeelddata
namen = ['Anna Jansen', 'Bram de Vries', 'Clara Peters', 'Daan van Dijk', 'Eva Smits', 'Finn de Boer', 'Gwen Vos', 'Henk Bakker']
functies = ['Developer', 'Designer', 'Project Manager', 'HR', 'Marketing', 'Sales']
expertises = ['Python', 'UX/UI', 'Agile', 'Recruitment', 'SEO', 'Salesforce']

def random_date(start_year=1970, end_year=2000):
    """Geeft een random geboortedatum"""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# Maak 20 random employees
data = []
for _ in range(20):
    naam = random.choice(namen)
    functie = random.choice(functies)
    expertise = random.choice(expertises)
    geboortedatum = random_date()
    datum_indienst = random_date(2005, 2023)  # datum van indiensttreding
    data.append({
        'naam': naam,
        'functie': functie,
        'expertise': expertise,
        'geboortedatum': geboortedatum.date(),
        'datum_indienst': datum_indienst.date()
    })

# Maak dataframe
df = pd.DataFrame(data)

# Excel bestand opslaan
df.to_excel('employees.xlsx', index=False)

print("Excel bestand 'employees.xlsx' is aangemaakt!")
