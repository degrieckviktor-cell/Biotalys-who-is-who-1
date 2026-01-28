from nicegui import ui
from data_source import get_functies, update_functie, delete_functie, insert_functie  # update_functie moet je in data_source.py aanmaken
from ui_table import simple_table


def functions_tab(parent):
    """Functions tab DB-driven met Edit/Delete per rij"""

    with ui.column().bind_visibility_from(parent, 'value', lambda v: v == 'Functions')\
            .classes('w-full max-w-7xl mx-auto'):

        ui.label('Functies').classes(
            'text-2xl font-bold mb-4'
        )

        # ---------- REFRESH FUNCTIES ----------
        functies = get_functies()
        rows = [[str(f['id']), f['naam']] for f in functies]

        table = None  # ✅ definieer hier

        # ---------- CALLBACKS ----------
        def edit_function(row_index):
            nonlocal table
            f = functies[row_index]
            dialog = ui.dialog()
            with dialog, ui.card().classes('w-[400px] p-4'):
                ui.label(f"Functie bewerken (ID: {f['id']})").classes('text-lg font-bold mb-4')
                naam_input = ui.input('Naam', value=f['naam']).classes('w-full')

                def save():
                    new_name = naam_input.value.strip()
                    if new_name:
                        update_functie(f['id'], new_name)
                        dialog.close()
                        refresh()

                ui.button('Opslaan', on_click=save).classes('bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mr-2')
                ui.button('Annuleren', on_click=dialog.close).classes('bg-gray-300 px-4 py-2 rounded hover:bg-gray-400')

            dialog.open()

        def delete_function(row_index):
            nonlocal table
            f = functies[row_index]
            dialog = ui.dialog()
            with dialog, ui.card().classes('w-[300px] p-4'):
                ui.label(f"Weet je zeker dat je functie '{f['naam']}' wilt verwijderen?").classes('text-center mb-4')

                def confirm_delete():
                    delete_functie(f['id'])
                    dialog.close()
                    refresh()

                with ui.row().classes('justify-center gap-2'):
                    ui.button('Verwijderen', on_click=confirm_delete).classes('bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600')
                    ui.button('Annuleren', on_click=dialog.close).classes('bg-gray-300 px-4 py-2 rounded hover:bg-gray-400')

            dialog.open()

        # ---------- REFRESH FUNCTIES TABLE ----------
        def refresh():
            nonlocal table, functies, rows
            functies = get_functies()
            rows = [[str(f['id']), f['naam']] for f in functies]
            if table:
                table.clear()
            render_table()

        # ---------- RENDER TABLE ----------
        def render_table():
            nonlocal table
            table = simple_table(
                headers=['ID', 'Functie'],
                rows=rows,
                on_edit=edit_function,
                on_delete=delete_function
            )

        render_table()
        # ---------- FLOATING NEW FUNCTION BUTTON ----------
        def open_new_function_dialog():
            dialog = ui.dialog()
            with dialog, ui.card().classes('w-[400px] p-4'):
                ui.label("Nieuwe functie toevoegen").classes('text-lg font-bold mb-4')
                naam_input = ui.input('Functienaam').classes('w-full')

                def save():
                    new_name = naam_input.value.strip()
                    if new_name:
                        insert_functie(new_name)  # Voeg toe in database
                        dialog.close()
                        refresh()  # tabel refreshen

                ui.button('Opslaan', on_click=save).classes(
                    'bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 mr-2'
                )
                ui.button('Annuleren', on_click=dialog.close).classes(
                    'bg-gray-300 px-4 py-2 rounded hover:bg-gray-400'
                )

            dialog.open()

        # Floating button rechtsonder
        ui.button(
            '+ Nieuwe functie',
            on_click=open_new_function_dialog
        ).classes(
            'fixed bottom-6 right-6 bg-green-500 text-white font-semibold px-5 py-3 rounded-xl shadow-lg z-50 hover:bg-green-600'
        )
