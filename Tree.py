from nicegui import ui
from data_source import get_employees

def org_tree_tab(parent):
    with ui.column().bind_visibility_from(parent, 'value', lambda v: v == 'Tree')\
            .classes('items-center w-full mt-6'):

        ui.label("Organigram / Boomstructuur").classes('text-2xl font-bold mb-4')

        employees = get_employees()
        employee_dict = {emp['id']: emp for emp in employees}

        # ---------------- INFO POPUP ----------------
        def show_info(emp):
            dialog = ui.dialog()
            with dialog, ui.card().classes('w-[400px] p-4'):
                ui.label(f"{emp['naam']} {emp['achternaam']}").classes('text-xl font-bold')
                ui.label(f"Functie: {emp['functie']}")
                ui.label(f"Email: {emp.get('email', '-')}")
                ui.label(f"Location: {emp.get('location', '-')}")
                ui.label(f"Jaren ervaring: {emp.get('jaren', 0)}")
                ui.label(f"Actief: {'Ja' if emp.get('actief') else 'Nee'}")
                ui.button('Sluiten', on_click=dialog.close).classes('mt-4')
            dialog.open()

        # ---------------- NODE FUNCTION ----------------
        def add_node(parent_container, emp):
            children = [e for e in employees if e.get('manager_id') == emp['id']]
            is_open = {'value': False}

            with parent_container:
                with ui.row().classes('items-center gap-2 w-full px-2 py-1 hover:bg-gray-100 rounded'):
                    # Naam label → alleen popup
                    ui.label(f"{emp['naam']} ({emp['functie']})").classes(
                        'cursor-pointer'
                    ).on('click', lambda e, emp=emp: show_info(emp))

                    # Container voor pijltje die de rest van de ruimte vult
                    if children:
                        with ui.row().classes('flex-1 justify-start items-center cursor-pointer') as toggle_area:
                            arrow = ui.label('▶').classes('font-bold mr-1')

                            def toggle(e):
                                if not is_open['value']:
                                    child_container.style('max-height:1000px')
                                    arrow.set_text('▼')
                                else:
                                    child_container.style('max-height:0px')
                                    arrow.set_text('▶')
                                is_open['value'] = not is_open['value']

                            toggle_area.on('click', toggle)

                # Child container
                with ui.column().classes('ml-6 gap-1 overflow-hidden transition-all duration-300') as child_container:
                    child_container.style('max-height:0px')
                    for child in children:
                        add_node(child_container, child)

        # ---------------- TREE CONTAINER ----------------
        tree_container = ui.column().classes('w-full max-w-3xl border rounded shadow p-2 gap-1')

        # Voeg alle top-level medewerkers toe (zonder manager)
        top_level_emps = [e for e in employees if not e.get('manager_id')]
        for emp in top_level_emps:
            add_node(tree_container, emp)
