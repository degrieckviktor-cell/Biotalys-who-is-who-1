from nicegui import ui
from crud_employees import employee_tab
from crud_functions import functions_tab
from data_source import get_employees
ui.add_head_html('<link rel="stylesheet" href="Globale.css">')
# ================== PAGE TITLE ==================
ui.add_head_html('<title>Biotalys Employee Dashboard</title>')

# ================== TABS ==================
with ui.row().classes(
    'w-full max-w-7xl mx-auto bg-gray-100 rounded-xl shadow-lg p-1 items-center justify-between'
):
    with ui.tabs(value='Home') as tabs:
        ui.tab('Home').classes('text-lg font-semibold px-4 py-2 rounded-lg hover:bg-blue-200 transition-colors')
        ui.tab('Employees').classes('text-lg font-semibold px-4 py-2 rounded-lg hover:bg-blue-200 transition-colors')
        ui.tab('Functions').classes('text-lg font-semibold px-4 py-2 rounded-lg hover:bg-blue-200 transition-colors')

    ui.button(
    '🔄',
    on_click=lambda: ui.run_javascript('location.reload()')
).classes(
    '!bg-gray-200 !text-gray-800 hover:!bg-gray-300 px-3 py-2 text-sm rounded-xl mr-2 transition-all duration-200'
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
    from data_source import get_functies

    employees = get_employees()
    totaal = len(employees)

    functies = get_functies()  # haalt nu alle functies uit de functies-tabel
    aantal_functies = len(functies)

    with ui.row().classes('gap-6 justify-center'):
        with ui.card().classes('p-4 w-48 bg-blue-100 rounded shadow'):
            ui.label('Totaal medewerkers').classes('text-center font-semibold text-gray-800')
            ui.label(f"{totaal}").classes('text-center text-xl font-bold text-gray-900')

        with ui.card().classes('p-4 w-48 bg-blue-100 rounded shadow'):
            ui.label('Aantal functies').classes('text-center font-semibold text-gray-800')
            ui.label(f"{aantal_functies}").classes('text-center text-xl font-bold text-gray-900')


# ================== EMPLOYEES TAB ==================
employee_tab(tabs)  # Nieuwe medewerker knop alleen hier zichtbaar

# ================== FUNCTIONS TAB ==================
functions_tab(tabs)  # Blauwe kaarten met bulletpoints en hover-effect

# ================== FOOTER ==================
ui.label('© 2026 Biotalys').classes('text-center text-gray-500 mt-8 mb-6')

# ================== START UI ==================
ui.run(title='Biotalys Employee Dashboard')