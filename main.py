from nicegui import ui
from crud_employees import employee_tab
from crud_functions import functions_tab
from data_source import get_employees

# ================== PAGE TITLE ==================
ui.add_head_html('<title>Biotalys Employee Dashboard</title>')

# ================== TABS ==================
with ui.tabs(value='Home').classes(  # Home-tab standaard actief
    'w-full max-w-7xl mx-auto bg-gray-100 rounded-xl shadow-lg p-1'
) as tabs:
    ui.tab('Home').classes(
        'text-lg font-semibold px-4 py-2 rounded-lg hover:bg-blue-200 transition-colors'
    )
    ui.tab('Employees').classes(
        'text-lg font-semibold px-4 py-2 rounded-lg hover:bg-blue-200 transition-colors'
    )
    ui.tab('Functions').classes(
        'text-lg font-semibold px-4 py-2 rounded-lg hover:bg-blue-200 transition-colors'
    )

# ================== HOME TAB ==================
with ui.column().bind_visibility_from(tabs, 'value', lambda v: v == 'Home')\
        .classes('items-center w-full mt-6'):

    # Logo bovenaan, grotere cirkel
    ui.image('Afbeeldingen/BTLS.BR-54d7a278.png').classes(
        'w-48 h-48 rounded-full shadow-lg border-4 border-green-600 mx-auto mb-4'
    )

    # Subtitel
    ui.label("Welkom op het Biotalys Werknemers Dashboard!").classes(
        'text-2xl font-semibold text-center mb-2 text-gray-800'
    )
    ui.label("Gebruik de tabs bovenaan om medewerkers en functies te bekijken.").classes(
        'text-center text-gray-600 mb-6'
    )

    # Statistiek-kaarten
    employees = get_employees()
    totaal = len(employees)
    functies = set(e['functie'] for e in employees)

    with ui.row().classes('gap-6 justify-center'):
        with ui.card().classes('p-4 w-48 bg-blue-100 rounded shadow'):
            ui.label('Totaal medewerkers').classes('text-center font-semibold text-gray-800')
            ui.label(f"{totaal}").classes('text-center text-xl font-bold text-gray-900')

        with ui.card().classes('p-4 w-48 bg-blue-100 rounded shadow'):
            ui.label('Aantal functies').classes('text-center font-semibold text-gray-800')
            ui.label(f"{len(functies)}").classes('text-center text-xl font-bold text-gray-900')

# ================== EMPLOYEES TAB ==================
employee_tab(tabs)  # Nieuwe medewerker knop alleen hier zichtbaar

# ================== FUNCTIONS TAB ==================
functions_tab(tabs)  # Blauwe kaarten met bulletpoints en hover-effect

# ================== FOOTER ==================
ui.label('© 2026 Biotalys').classes('text-center text-gray-500 mt-8 mb-6')

# ================== START UI ==================
ui.run(title='Biotalys Employee Dashboard')
