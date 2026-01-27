from nicegui import ui
from data_source import get_employees

# ================= FUNCTIONS TAB =================
def functions_tab(parent):
    FUNCTIES = ['HR', 'Developer', 'Designer', 'Marketing', 'Project manager']

    # ================= TAB CONTENT =================
    with ui.column().bind_visibility_from(parent, 'value', lambda v: v == 'Functions')\
            .classes('items-center w-full'):

        # Titel gecentreerd
        ui.label('Werknemers per functie').classes('text-2xl font-bold mb-6 text-center')

        # Grid voor functie-kaarten, horizontaal gecentreerd
        with ui.grid().classes(
            'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center max-w-7xl'
        ) as grid:
            pass

        # ================= DISPLAY FUNCTIONS =================
        def show_functions():
            grid.clear()
            employees = get_employees()

            for functie in FUNCTIES:
                emps = [e for e in employees if e['functie'] == functie]
                if not emps:
                    continue

                with grid:
                    # Kaart per functie, blauwe achtergrond
                    with ui.card().classes(
                        'p-4 w-80 min-h-24 rounded shadow h-auto bg-blue-100'
                    ):
                        # Functienaam bovenaan
                        ui.label(f"{functie}").classes('text-lg font-bold mb-2 text-center break-words text-blue-900')

                        # Namen netjes onder elkaar met bulletpoints
                        for e in emps:
                            ui.label(f"• {e['naam']}").classes('text-sm text-center break-words mb-1 text-gray-800')

        show_functions()


