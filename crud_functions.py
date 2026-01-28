from nicegui import ui
from data_source import get_functies

# ================= FUNCTIES TAB =================
def functions_tab(parent):

    with ui.column().bind_visibility_from(parent, 'value', lambda v: v == 'Functions')\
            .classes('items-center w-full max-w-xl mx-auto'):

        ui.label('Functies').classes(
            'text-2xl font-bold mb-6 text-center'
        )

        functies = get_functies()

        if not functies:
            ui.label('Geen functies gevonden').classes(
                'text-gray-500 italic'
            )
        else:
            with ui.column().classes(
                'w-full bg-blue-100 rounded shadow p-4'
            ):
                for f in functies:
                    ui.label(f"• {f['naam']}").classes(
                        'text-base text-gray-800'
                    )
