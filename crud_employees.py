from nicegui import ui
from data_source import get_employees, insert_employee, update_employee, delete_employee
from datetime import datetime, date

# ================= EMPLOYEES TAB =================
def employee_tab(parent):
    FUNCTIES = ['HR', 'Developer', 'Designer', 'Marketing', 'Project manager']

    # ---------- HELPERS ----------
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

    # ---------- TAB CONTENT ----------
    with ui.column().bind_visibility_from(parent, 'value', lambda v: v == 'Employees')\
            .classes('items-center w-full'):

        ui.label('Werknemerslijst').classes('text-2xl font-bold mb-6 text-center')

        with ui.grid().classes(
            'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center max-w-7xl'
        ) as grid:
            pass

        employees = get_employees()

        def refresh():
            nonlocal employees
            employees = get_employees()
            show_employees()

        # ---------- DELETE ----------
        delete_dialog = ui.dialog()
        delete_id = None
        with delete_dialog, ui.card().classes('w-80'):
            ui.label('⚠️ Werknemer verwijderen').classes('text-lg font-bold')
            ui.label('Ben je zeker?')
            with ui.row().classes('justify-end gap-2'):
                ui.button('Annuleren', on_click=delete_dialog.close)
                ui.button('Verwijderen', color='red',
                          on_click=lambda: (delete_employee(delete_id), refresh(), delete_dialog.close()))

        def ask_delete(emp_id):
            nonlocal delete_id
            delete_id = emp_id
            delete_dialog.open()

        # ---------- EDIT ----------
        edit_dialog = ui.dialog()
        current = None
        with edit_dialog, ui.card().classes('w-[600px] p-6'):
            ui.label('Medewerker bewerken').classes('text-xl font-bold mb-4')

            with ui.grid().classes('grid-cols-2 gap-4'):
                naam_i = ui.input('Naam')
                functie_i = ui.select(FUNCTIES, label='Functie')
                email_i = ui.input('Email')
                location_i = ui.input('Location')
                language_i = ui.input('Language')
                mobile_phone_i = ui.input('Mobile phone')
                office_phone_i = ui.input('Office phone')
                work_groups_i = ui.input('Work groups')
                hobbies_i = ui.input('Hobbies')
                expertise_i = ui.input('Expertise')

                geboorte_i = ui.date('Geboortedatum')
                start_i = ui.date('Datum indienst')
                jaren_i = ui.number('Jaren ervaring', min=0, max=55, step=1)
                actief_i = ui.checkbox('Actief')

            ui.button('Opslaan', on_click=lambda: save_edit())\
                .classes('mt-4 w-full bg-blue-600 text-white')

        def open_edit(e):
            nonlocal current
            current = e
            naam_i.value = e['naam']
            functie_i.value = e['functie']
            expertise_i.value = e['expertise']
            geboorte_i.value = to_date(e['geboortedatum'])
            start_i.value = to_date(e['datum_indienst'])
            actief_i.value = e['actief']
            jaren_i.value = e['jaren']
            email_i.value = e.get('email','')
            location_i.value = e.get('location','')
            language_i.value = e.get('language','')
            hobbies_i.value = e.get('hobbies','')
            work_groups_i.value = e.get('work_groups','')
            mobile_phone_i.value = e.get('mobile_phone','')
            office_phone_i.value = e.get('office_phone','')
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
                'email': email_i.value,
                'location': location_i.value,
                'language': language_i.value,
                'hobbies': hobbies_i.value,
                'work_groups': work_groups_i.value,
                'mobile_phone': mobile_phone_i.value,
                'office_phone': office_phone_i.value
            })
            update_employee(current)
            refresh()
            edit_dialog.close()

        # ---------- DETAIL POPUP ----------
        def open_details(e):
            dialog = ui.dialog()
            with dialog, ui.card().classes('w-[700px] p-6'):
                ui.label(e['naam']).classes('text-2xl font-bold mb-4 text-center')

                with ui.grid().classes('grid-cols-2 gap-4 text-sm'):
                    ui.label(f"Status: {'Actief' if e['actief'] else 'Niet actief'}")
                    ui.label(f"Functie: {e['functie']}")
                    ui.label(f"Expertise: {e['expertise']}")
                    ui.label(f"Jaren ervaring: {e['jaren']}")
                    ui.label(f"Email: {e.get('email','')}")
                    ui.label(f"Location: {e.get('location','')}")
                    ui.label(f"Language: {e.get('language','')}")
                    ui.label(f"Work groups: {e.get('work_groups','')}")
                    ui.label(f"Hobbies: {e.get('hobbies','')}")
                    ui.label(f"Mobile phone: {e.get('mobile_phone','')}")
                    ui.label(f"Office phone: {e.get('office_phone','')}")
                    ui.label(f"Geboortedatum: {to_str(e['geboortedatum'])}")
                    ui.label(f"Datum indienst: {to_str(e['datum_indienst'])}")

                with ui.row().classes('justify-end gap-3 mt-6'):
                    ui.button('Bewerken', on_click=lambda: (dialog.close(), open_edit(e)))
                    ui.button('Verwijderen', color='red',
                              on_click=lambda: (dialog.close(), ask_delete(e['id'])))
                    ui.button('Sluiten', on_click=dialog.close)

            dialog.open()

        # ---------- DISPLAY ----------
        def show_employees():
            grid.clear()
            for e in employees:
                kleur = 'border-green-500' if e['actief'] else 'border-red-500'
                text = 'text-green-600' if e['actief'] else 'text-red-600'

                with grid:
                    with ui.card().classes(
                        f'w-64 p-4 border-2 rounded shadow items-center {kleur}'
                    ):
                        ui.label(e['naam']).classes(f'text-lg font-bold {text} text-center')
                        ui.label('Actief' if e['actief'] else 'Niet actief')\
                            .classes(f'text-sm {text} text-center')
                        ui.label(e['functie']).classes('text-sm text-center')
                        ui.label(f"{e['jaren']} jaar ervaring").classes('text-sm text-center')

                        ui.button('Details', on_click=lambda emp=e: open_details(emp))\
                            .classes('mt-3 w-full')

        show_employees()
