from nicegui import ui
from data_source import get_employees, insert_employee, update_employee, delete_employee, get_functies
from datetime import datetime, date

# ================= BUTTON STYLES =================
BTN_PRIMARY = '!bg-green-700 !text-white hover:!bg-green-800 rounded-lg'
BTN_SECONDARY = '!bg-emerald-600 !text-white hover:!bg-emerald-700 rounded-lg'
BTN_NEUTRAL = '!bg-gray-200 !text-gray-800 hover:!bg-gray-300 rounded-lg'
BTN_DANGER = '!bg-red-600 !text-white hover:!bg-red-700 rounded-lg'
BTN_SMALL = 'px-4 py-2'
BTN_FULL = 'w-full px-4 py-2'

def employee_tab(parent):

    # ---------- Helpers ----------
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

    def get_fun_options():
        return [f['naam'] for f in get_functies()]

    # ================= TAB CONTENT =================
    with ui.column().bind_visibility_from(parent, 'value', lambda v: v == 'Employees')\
            .classes('items-center w-full mt-6'):

        # ---------- Nonlocal vars ----------
        current = None
        employees = get_employees()

        # ================= POPUPS =================
        # ---------- Edit Dialog ----------
        edit_dialog = ui.dialog()
        with edit_dialog, ui.card().classes('w-[500px] max-h-[80vh] overflow-auto p-0'):
            with ui.row().classes('bg-green-600 text-white p-4 justify-center'):
                ui.label('Werknemer bewerken').classes('text-xl font-bold')

            with ui.column().classes('p-6 gap-3 items-center'):
                naam = ui.input('Naam').classes('w-full')
                functie = ui.select([], label='Functie').classes('w-full')
                expertise = ui.input('Expertise').classes('w-full')
                email = ui.input('Email').classes('w-full')
                location = ui.input('Location').classes('w-full')
                language = ui.input('Language').classes('w-full')
                work_groups = ui.input('Work groups').classes('w-full')
                hobbies = ui.input('Hobbies').classes('w-full')
                mobile_phone = ui.input('Mobile phone').classes('w-full')
                office_phone = ui.input('Office phone').classes('w-full')
                geboorte = ui.date('Geboortedatum').classes('w-full')
                start = ui.date('Datum indienst').classes('w-full')
                jaren = ui.number('Jaren ervaring', min=0, max=55).classes('w-full')
                actief = ui.checkbox('Actief')

                def save_edit():
                    current.update({
                        'naam': naam.value,
                        'functie': functie.value,
                        'expertise': expertise.value,
                        'email': email.value,
                        'location': location.value,
                        'language': language.value,
                        'work_groups': work_groups.value,
                        'hobbies': hobbies.value,
                        'mobile_phone': mobile_phone.value,
                        'office_phone': office_phone.value,
                        'geboortedatum': to_str(geboorte.value),
                        'datum_indienst': to_str(start.value),
                        'jaren': int(jaren.value or 0),
                        'actief': actief.value,
                    })
                    update_employee(current)
                    refresh()
                    edit_dialog.close()

                ui.button('Opslaan', on_click=save_edit).classes(f'{BTN_PRIMARY} {BTN_FULL} mt-4')

        # ---------- New Employee Dialog ----------
        new_dialog = ui.dialog()
        with new_dialog, ui.card().classes('w-[500px] max-h-[80vh] overflow-auto p-0'):
            with ui.row().classes('bg-green-600 text-white p-4 justify-center'):
                ui.label('Nieuwe medewerker').classes('text-xl font-bold')

            with ui.column().classes('p-6 gap-3 items-center'):
                n_naam = ui.input('Naam').classes('w-full')
                n_functie = ui.select(get_fun_options(), label='Functie').classes('w-full')
                n_expertise = ui.input('Expertise').classes('w-full')
                n_email = ui.input('Email').classes('w-full')
                n_location = ui.input('Location').classes('w-full')
                n_language = ui.input('Language').classes('w-full')
                n_work_groups = ui.input('Work groups').classes('w-full')
                n_hobbies = ui.input('Hobbies').classes('w-full')
                n_mobile_phone = ui.input('Mobile phone').classes('w-full')
                n_office_phone = ui.input('Office phone').classes('w-full')
                n_geboorte = ui.date('Geboortedatum').classes('w-full')
                n_start = ui.date('Datum indienst').classes('w-full')
                n_jaren = ui.number('Jaren ervaring', min=0, max=55).classes('w-full')
                n_actief = ui.checkbox('Actief', value=True)

                def save_new_employee():
                    new_emp = {
                        'naam': n_naam.value or '',
                        'functie': n_functie.value or '',
                        'expertise': n_expertise.value or '',
                        'email': n_email.value or '',
                        'location': n_location.value or '',
                        'language': n_language.value or '',
                        'work_groups': n_work_groups.value or '',
                        'hobbies': n_hobbies.value or '',
                        'mobile_phone': n_mobile_phone.value or '',
                        'office_phone': n_office_phone.value or '',
                        'geboortedatum': to_str(n_geboorte.value) if n_geboorte.value else '1900-01-01',
                        'datum_indienst': to_str(n_start.value) if n_start.value else '1900-01-01',
                        'jaren': int(n_jaren.value or 0),
                        'actief': n_actief.value,
                    }
                    insert_employee(new_emp)
                    refresh()
                    new_dialog.close()
                    ui.notify('Nieuwe medewerker toegevoegd!', color='green')

                ui.button('Opslaan', on_click=save_new_employee).classes(f'{BTN_PRIMARY} {BTN_FULL} mt-4')

        # ================= OPEN EDIT FUNCTION =================
        def open_edit(e):
            nonlocal current
            current = e
            naam.value = e['naam']
            functie.options = get_fun_options()
            functie.value = e['functie']
            expertise.value = e['expertise']
            email.value = e.get('email', '')
            location.value = e.get('location', '')
            language.value = e.get('language', '')
            work_groups.value = e.get('work_groups', '')
            hobbies.value = e.get('hobbies', '')
            mobile_phone.value = e.get('mobile_phone', '')
            office_phone.value = e.get('office_phone', '')
            geboorte.value = to_date(e['geboortedatum'])
            start.value = to_date(e['datum_indienst'])
            jaren.value = int(e.get('jaren', 0))
            actief.value = e.get('actief', True)
            edit_dialog.open()

        # ================= REFRESH =================
        def refresh():
            nonlocal employees
            employees = get_employees()
            filter_employees()

        # ================= TOPBAR =================
        with ui.row().classes('w-full max-w-7xl justify-between items-center mb-6'):
            ui.label('Werknemerslijst').classes('text-2xl font-bold')

            with ui.row().classes('items-center gap-2'):
                search_input = ui.input(placeholder='Zoek werknemer...').classes(
                    'w-64 transition-all duration-500 ease-in-out rounded-full px-4'
                )
                ui.button('Zoek', on_click=lambda: filter_employees()).classes(f'{BTN_SECONDARY} {BTN_SMALL}')
                ui.button('Reset', on_click=lambda: reset_employees()).classes(f'{BTN_NEUTRAL} {BTN_SMALL}')

        # ================= GRID =================
        with ui.grid().classes(
            'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center max-w-7xl'
        ) as grid:
            pass

        # ================= DISPLAY EMPLOYEES =================
        def show_employees(employee_list=None):
            grid.clear()
            data = employee_list or employees
            for e in data:
                actief = e['actief']
                kleur = 'text-green-600' if actief else 'text-red-600'
                border = 'border-green-500' if actief else 'border-red-500'

                with grid:
                    with ui.card().classes(
                        f'w-64 p-4 border-2 rounded shadow hover:scale-105 transition-transform duration-200 {border}'
                    ).on('click', lambda emp=e: open_details(emp)):
                        ui.label(e['naam']).classes('text-lg font-bold text-center')
                        ui.label('Actief' if actief else 'Niet actief').classes(f'text-sm {kleur} text-center')
                        ui.label(e['functie']).classes('text-sm text-center')
                        ui.label(f"{e['jaren']} jaar ervaring").classes('text-sm text-center')

        show_employees()

        # ================= SEARCH / RESET =================
        def filter_employees(e=None):
            query = search_input.value.lower().strip()
            if not query:
                show_employees(employees)
            else:
                filtered = [emp for emp in employees if query in emp['naam'].lower()]
                show_employees(filtered)

        def reset_employees():
            search_input.value = ''
            show_employees(employees)

        search_input.on('input', filter_employees)

        # ================= DETAILS POPUP =================
        def open_details(e):
            dialog = ui.dialog()
            with dialog, ui.card().classes('w-[900px] max-h-[80vh] overflow-auto p-0'):
                with ui.row().classes('bg-red-600 text-white p-4 justify-center items-center gap-4'):
                    ui.label(e['naam']).classes('text-2xl font-bold')
                    ui.label('Actief' if e['actief'] else 'Niet actief').classes(
                        'text-lg ' + ('text-green-200' if e['actief'] else 'text-red-400')
                    )

                with ui.grid().classes('grid-cols-2 gap-4 p-6 text-sm'):
                    items = [
                        ('🧩 Functie', e['functie']),
                        ('🕒 Jaren ervaring', e['jaren']),
                        ('📧 Email', e.get('email')),
                        ('📍 Location', e.get('location')),
                        ('🌍 Language', e.get('language')),
                        ('👥 Work groups', e.get('work_groups')),
                        ('🎯 Hobbies', e.get('hobbies')),
                        ('📱 Mobile phone', e.get('mobile_phone')),
                        ('☎️ Office phone', e.get('office_phone')),
                        ('🎂 Geboortedatum', to_str(e['geboortedatum'])),
                        ('🗓️ Datum indienst', to_str(e['datum_indienst'])),
                        ('💼 Expertise', e['expertise']),
                    ]
                    for label, value in items:
                        ui.label(label).classes('font-semibold')
                        ui.label(value or '-')

                with ui.row().classes('justify-end gap-3 p-4 border-t'):
                    ui.button('Bewerken', on_click=lambda emp=e: (dialog.close(), open_edit(emp))).classes(f'{BTN_PRIMARY} {BTN_SMALL}')
                    ui.button('Verwijderen', on_click=lambda emp=e: (dialog.close(), delete_employee(emp['id']), refresh())).classes(f'{BTN_DANGER} {BTN_SMALL}')
                    ui.button('Sluiten', on_click=dialog.close).classes(f'{BTN_NEUTRAL} {BTN_SMALL}')

            dialog.open()

        # ================= FLOATING NEW EMPLOYEE BUTTON =================
        ui.button('+ Nieuwe medewerker', on_click=new_dialog.open).classes(
            'fixed bottom-6 right-6 '
            '!bg-gradient-to-r from-emerald-600 to-green-700 '
            '!text-white font-semibold px-5 py-2.5 '
            'rounded-lg shadow-xl z-50 '
            'hover:from-emerald-700 hover:to-green-800 '
            'transition-all duration-200'
        )
