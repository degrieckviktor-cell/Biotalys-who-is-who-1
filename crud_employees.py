from nicegui import ui
from data_source import get_employees, insert_employee, update_employee, delete_employee
from datetime import datetime, date

# ================= EMPLOYEES TAB =================
def employee_tab(parent):
    FUNCTIES = ['HR', 'Developer', 'Designer', 'Marketing', 'Project manager']

    # Helpers
    def to_date(d):
        if isinstance(d, date):
            return d
        if isinstance(d, datetime):
            return d.date()
        if isinstance(d, str):
            return datetime.strptime(d.split(' ')[0], '%Y-%m-%d').date()
        return date.today()

    def to_str(d):
        return to_date(d).strftime('%Y-%m-%d')

    def validate_date(d):
        if to_date(d) > date.today():
            ui.notify('Datum kan niet in de toekomst liggen', color='red')
            return False
        return True

    # ================= TAB CONTENT =================
    with ui.column().bind_visibility_from(parent, 'value', lambda v: v == 'Employees')\
            .classes('items-center w-full'):

        ui.label('Employee List').classes('text-2xl font-bold mb-6 text-center')

        # Grid
        with ui.grid().classes(
            'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center max-w-7xl'
        ) as grid:
            pass

        # ================ CRUD FUNCTIONS ================
        def refresh_employees():
            nonlocal employees
            employees = get_employees()
            show_employees()

        employees = get_employees()

        # DELETE DIALOG
        delete_dialog = ui.dialog()
        delete_id = None
        with delete_dialog, ui.card():
            ui.label('⚠️ Medewerker verwijderen').classes('text-lg font-bold')
            ui.label('Ben je zeker dat je deze medewerker wil verwijderen?')
            with ui.row().classes('justify-end gap-2'):
                ui.button('Annuleren', on_click=lambda: delete_dialog.close())
                ui.button(
                    'Verwijderen',
                    color='red',
                    on_click=lambda: (
                        delete_employee(delete_id),
                        refresh_employees(),
                        delete_dialog.close()
                    )
                )

        def ask_delete(emp_id):
            nonlocal delete_id
            delete_id = emp_id
            delete_dialog.open()

        # EDIT DIALOG
        edit_dialog = ui.dialog()
        current = None
        with edit_dialog, ui.card().classes('w-96'):
            ui.label('Medewerker bewerken').classes('text-lg font-bold')
            naam_i = ui.input('Naam').classes('w-full')
            functie_i = ui.select(FUNCTIES, label='Functie').classes('w-full')
            expertise_i = ui.input('Expertise').classes('w-full')
            with ui.column().classes('items-center w-full'):
                geboorte_i = ui.date('Geboortedatum').classes('w-64')
                start_i = ui.date('Datum indienst').classes('w-64')
            actief_i = ui.checkbox('Actief')
            jaren_i = ui.number('Aantal jaren ervaring', min=0, max=55, step=1, format='%.0f')\
                .props('outlined').classes('w-full')
            ui.label('Aantal volledige jaren dat de medewerker in dienst is (0–55).')\
                .classes('text-sm text-gray-500 -mt-3')
            ui.button('Opslaan', on_click=lambda: save_edit()).classes('mt-4 w-full')

        def open_edit(e):
            nonlocal current
            current = e
            naam_i.value = e['naam']
            functie_i.value = e['functie']
            expertise_i.value = e['expertise']
            geboorte_i.value = to_date(e['geboortedatum'])
            start_i.value = to_date(e['datum_indienst'])
            actief_i.value = e.get('actief', True)
            jaren_i.value = e.get('jaren', 0)
            edit_dialog.open()

        def save_edit():
            if not (validate_date(geboorte_i.value) and validate_date(start_i.value)):
                return
            current.update({
                'naam': naam_i.value,
                'functie': functie_i.value,
                'expertise': expertise_i.value,
                'geboortedatum': to_str(geboorte_i.value),
                'datum_indienst': to_str(start_i.value),
                'actief': actief_i.value,
                'jaren': int(jaren_i.value),
            })
            update_employee(current)
            refresh_employees()
            edit_dialog.close()

        # NEW DIALOG
        new_dialog = ui.dialog()
        with new_dialog, ui.card().classes('w-96'):
            ui.label('Nieuwe medewerker').classes('text-lg font-bold')
            n_naam = ui.input('Naam').classes('w-full')
            n_functie = ui.select(FUNCTIES, label='Functie').classes('w-full')
            n_expertise = ui.input('Expertise').classes('w-full')
            with ui.column().classes('items-center w-full'):
                n_geboorte = ui.date('Geboortedatum').classes('w-64')
                n_start = ui.date('Datum indienst').classes('w-64')
            n_actief = ui.checkbox('Actief', value=True)
            n_jaren = ui.number('Aantal jaren ervaring', min=0, max=55, step=1, format='%.0f')\
                .props('outlined').classes('w-full')
            ui.label('Aantal volledige jaren dat de medewerker in dienst is (0–55).')\
                .classes('text-sm text-gray-500 -mt-3')
            ui.button('Opslaan', on_click=lambda: save_new()).classes('mt-4 w-full')

        def save_new():
            if not (validate_date(n_geboorte.value) and validate_date(n_start.value)):
                return
            new_emp = {
                'naam': n_naam.value,
                'functie': n_functie.value,
                'expertise': n_expertise.value,
                'geboortedatum': to_str(n_geboorte.value),
                'datum_indienst': to_str(n_start.value),
                'actief': n_actief.value,
                'jaren': int(n_jaren.value),
            }
            insert_employee(new_emp)
            refresh_employees()
            new_dialog.close()

        # ================= DISPLAY =================
        def show_employees():
            grid.clear()
            for e in employees:
                actief = e.get('actief', True)
                border = 'border-green-500' if actief else 'border-red-500'
                name_color = 'text-green-600' if actief else 'text-red-600'
                status_text = 'Actief' if actief else 'Niet actief'

                with grid:
                    with ui.column().classes(
                        f'mx-auto p-4 border-2 rounded shadow {border} w-64 items-center'
                    ):
                        ui.label(e['naam']).classes(f'text-lg font-bold {name_color} text-center')
                        ui.label(status_text).classes(f'text-sm {name_color} mb-1 text-center')
                        ui.label(f"Functie: {e['functie']}").classes('text-sm text-center')
                        ui.label(f"Expertise: {e['expertise']}").classes('text-sm text-center')
                        ui.label(f"Geboortedatum: {to_str(e['geboortedatum'])}").classes('text-sm text-center')
                        ui.label(f"Datum indienst: {to_str(e['datum_indienst'])}").classes('text-sm text-center')
                        ui.label(f"Aantal jaren: {e['jaren']}").classes('text-sm text-center')

                        with ui.row().classes('mt-2 gap-2'):
                            ui.button('Edit', on_click=lambda emp=e: open_edit(emp))
                            ui.button('Delete', color='red', on_click=lambda emp_id=e['id']: ask_delete(emp_id))

        # Sticky New button
        ui.button('Nieuwe medewerker', on_click=lambda: new_dialog.open())\
            .classes('fixed bottom-6 right-6 bg-blue-600 text-white rounded-full px-4 py-2 shadow-lg z-50')

        show_employees()

