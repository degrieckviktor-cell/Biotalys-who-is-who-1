from nicegui import ui


def simple_table(
    headers: list[str],
    rows: list[list[str]],
    on_edit=None,
    on_delete=None,
):
    """
    Universele simpele tabel (database-stijl) met automatische Edit/Delete knoppen per rij.
    - headers: lijst van kolomnamen
    - rows: lijst van rijen, elke rij = lijst van celwaarden
    - on_edit/on_delete: callbacks met row_index als argument
    """

    # ---------- HEADER ----------
    with ui.row().classes(
        'w-full bg-gray-100 border-b font-semibold text-sm text-gray-700 px-4 py-2'
    ):
        for h in headers:
            ui.label(h).classes('flex-1')

        # Acties-kop automatisch toevoegen
        if on_edit or on_delete:
            ui.label('Acties').classes('w-32 text-center')

    # ---------- ROWS ----------
    for row_index, row in enumerate(rows):
        with ui.row().classes(
            'w-full px-4 py-2 border-b text-sm items-center hover:bg-gray-50'
        ):
            # cellen
            for cell in row:
                ui.label(cell).classes('flex-1 text-gray-800')

            # acties
            if on_edit or on_delete:
                with ui.row().classes('w-32 justify-center gap-2'):
                    if on_edit:
                        ui.button(
                            'Edit',
                            on_click=lambda i=row_index: on_edit(i)
                        ).classes(
                            '!bg-green-700 !text-white hover:!bg-green-800 px-2 py-1 rounded'
                        )

                    if on_delete:
                        ui.button(
                            'Delete',
                            on_click=lambda i=row_index: on_delete(i)
                        ).classes(
                            '!bg-red-500 text-white px-2 py-1 rounded hover:!bg-red-600'
                        )
