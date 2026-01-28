from nicegui import ui
from data_source import get_employees, insert_employee, update_employee, delete_employee
from datetime import datetime, date

# ================= EMPLOYEES TAB =================
def employee_tab(parent):
    FUNCTIES = ['HR', 'Developer', 'Designer', 'Marketing', 'Project manager']

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

    # ================= TAB CONTENT =================
    with ui.column().bind_visibility_from(parent, 'value', lambda v: v == 'Employees')\
            .classes('items-center w-full'):

        ui.label('Werknemerslijst').classes('text-2xl font-bold mb-6')

        # ---------- Zoekbalk ----------
        with ui.row().classes('justify-center mb-6 relative'):
            search_input = ui.input(placeholder='Zoek werknemer...').classes(
                'w-10 transition-all duration-300 rounded-full px-2'
            )

            search_input.on('focus', lambda e: search_input.classes('w-64 px-4'))
            search_input.on('blur', lambda e: search_input.classes('w-10 px-2'))
            search_input.on('mouseenter', lambda e: search_input.classes('w-64 px-4'))
            search_input.on('mouseleave', lambda e: search_input.classes('w-10 px-2'))
            search_input.props('prefix="🔍"')

        employees = get_employees()

        # ---------- Grid voor kaarten ----------
        with ui.grid().classes(
            'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-items-center max-w-7xl'
        ) as grid:
            pass

        # ================= DETAILS POPUP =================
        def open_details(e):
            dialog = ui.dialog()
            with dialog, ui.card().classes('w-[900px] max-h-[80vh] overflow-auto p-0'):
                with ui.row().classes('bg-green-600 text-white p-4 justify-center items-center gap-4'):
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
                    ui.button('Bewerken', on_click=lambda: (dialog.close(), open_edit(e)))
                    ui.button(
                        'Verwijderen',
                        color='red',
                        on_click=lambda: (dialog.close(), delete_employee(e['id']), refresh())
                    )
                    ui.button('Sluiten', on_click=dialog.close)

            dialog.open()

        # ================= EDIT POPUP =================
        edit_dialog = ui.dialog()
        current = None

        with edit_dialog, ui.card().classes('w-[600px] max-h-[80vh] overflow-auto p-0'):
            with ui.row().classes('bg-green-600 text-white p-4 justify-center'):
                ui.label('Werknemer bewerken').classes('text-xl font-bold')

            with ui.column().classes('p-6 gap-3 items-center'):
                naam = ui.input('Naam').classes('w-full')
                functie = ui.select(FUNCTIES, label='Functie').classes('w-full')
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

                ui.button('Opslaan', on_click=save_edit).classes('mt-4 w-full bg-green-600 text-white')

        def open_edit(e):
            nonlocal current
            current = e
            naam.value = e['naam']
            functie.value = e['functie']
            expertise.value = e['expertise']
            email.value = e.get('email')
            location.value = e.get('location')
            language.value = e.get('language')
            work_groups.value = e.get('work_groups')
            hobbies.value = e.get('hobbies')
            mobile_phone.value = e.get('mobile_phone')
            office_phone.value = e.get('office_phone')
            geboorte.value = to_date(e['geboortedatum'])
            start.value = to_date(e['datum_indienst'])
            jaren.value = e['jaren']
            actief.value = e['actief']
            edit_dialog.open()

        # ================= NEW EMPLOYEE POPUP =================
        new_dialog = ui.dialog()
        with new_dialog, ui.card().classes('w-[600px] max-h-[80vh] overflow-auto p-0'):
            with ui.row().classes('bg-green-600 text-white p-4 justify-center'):
                ui.label('Nieuwe medewerker').classes('text-xl font-bold')

            with ui.column().classes('p-6 gap-3 items-center'):
                n_naam = ui.input('Naam').classes('w-full')
                n_functie = ui.select(FUNCTIES, label='Functie').classes('w-full')
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

                ui.button('Opslaan', on_click=save_new_employee).classes('mt-4 w-full bg-green-600 text-white')

        # ================= CARDS =================
        def show_employees(employee_list=None):
            grid.clear()
            data = employee_list or employees
            for e in data:
                actief = e['actief']
                kleur = 'text-green-600' if actief else 'text-red-600'
                border = 'border-green-500' if actief else 'border-red-500'

                with grid:
                    with ui.card().classes(f'w-64 p-4 border-2 rounded shadow {border}'):
                        ui.label(e['naam']).classes('text-lg font-bold text-center')
                        ui.label('Actief' if actief else 'Niet actief').classes(f'text-sm {kleur} text-center')
                        ui.label(e['functie']).classes('text-sm text-center')
                        ui.label(f"{e['jaren']} jaar ervaring").classes('text-sm text-center')
                        ui.button(
                            'Details',
                            on_click=lambda emp=e: open_details(emp)
                        ).classes('mt-3 w-full')

        show_employees()

        # ================= FLOATING NEW BUTTON =================
        ui.button(
            '+ Nieuwe medewerker',
            on_click=new_dialog.open
        ).bind_visibility_from(parent, 'value', lambda v: v == 'Employees')\
         .classes(
            'fixed bottom-6 right-6 bg-green-600 text-white px-5 py-3 '
            'rounded-full shadow-lg hover:bg-green-700 z-50'
        )

        # ================= ZOEKFUNCTIE =================
        def filter_employees():
            query = search_input.value.lower()
            filtered = [e for e in employees if query in e['naam'].lower()]
            show_employees(filtered)

        search_input.on('input', lambda e: filter_employees())
