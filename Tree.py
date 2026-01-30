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
        def add_node(parent_container, emp, level=0):
            children = [e for e in employees if e.get('manager_id') == emp['id']]
            is_open = {'value': False}

            with parent_container:
                # Node row
                with ui.row().classes('items-center gap-2 w-full px-2 py-1 hover:bg-gray-100 rounded') as node_row:
                    # Naam label → opent details popup
                    ui.label(f"{emp['naam']} ({emp['functie']})").classes('cursor-pointer').on(
                        'click', lambda e, emp=emp: show_info(emp)
                    )

                    # Pijltje rechts van de naam
                    arrow = None
                    if children:
                        arrow = ui.label('▶').classes('cursor-pointer font-bold')
                        # Klikbaar gebied: de hele rij
                        node_row.on('click', lambda e, arr=arrow, cont=None: toggle_children(arr, child_container))

                # Children container
                with ui.column().classes('gap-1 overflow-hidden transition-all duration-300') as child_container:
                    # start ingeklapt
                    child_container.style(f'max-height:0px; margin-left:{(level+1)*20}px')

                    # Voeg kinderen toe
                    for child in children:
                        add_node(child_container, child, level=level+1)

            # ---------------- TOGGLE FUNCTION ----------------
            def toggle_children(arrow, container):
                if not is_open['value']:
                    # openklappen
                    container.style(f'max-height:1000px; margin-left:{(level+1)*20}px')
                    arrow.set_text('▼')
                else:
                    # inklappen
                    container.style(f'max-height:0px; margin-left:{(level+1)*20}px')
                    arrow.set_text('▶')
                is_open['value'] = not is_open['value']

        # ---------------- TREE CONTAINER ----------------
        tree_container = ui.column().classes('w-full max-w-3xl border rounded shadow p-2 gap-1')

        # Voeg alle top-level medewerkers toe (zonder manager)
        top_level_emps = [e for e in employees if not e.get('manager_id')]
        for emp in top_level_emps:
            add_node(tree_container, emp)
