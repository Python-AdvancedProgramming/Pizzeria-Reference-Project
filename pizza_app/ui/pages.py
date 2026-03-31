"""NiceGUI pages.

This module is object-oriented: pages are registered by a `Pages` object which
holds the controllers it needs.
"""

from __future__ import annotations
from datetime import timezone
from zoneinfo import ZoneInfo

from nicegui import ui

from .controllers import AdminController, ShoppingController


class Pages:
    """Registers all NiceGUI routes (UI boundary)."""

    def __init__(self, shopping_controller: ShoppingController, admin_controller: AdminController) -> None:
        self._shopping_controller = shopping_controller
        self._admin_controller = admin_controller

    def register(self) -> None:
        order_controller = self._shopping_controller
        admin_controller = self._admin_controller

        @ui.page("/")
        def menu_page() -> None:
            ui.markdown("# 🍕 PizzaRP – Menu")

            with ui.row().classes("w-full items-start gap-8"):
                # left: menu list
                with ui.column().classes("w-2/3"):
                    ui.markdown("## Menu")

                    pizzas = order_controller.menu()

                    # Table with action buttons
                    columns = [
                        {"name": "name", "label": "Pizza", "field": "name", "align": "left"},
                        {"name": "ingredients", "label": "Ingredients", "field": "ingredients", "align": "left"},
                        {"name": "price", "label": "Price (CHF)", "field": "price", "align": "right"},
                        {"name": "actions", "label": "Actions", "field": "actions", "align": "center"},
                    ]
                    rows = []
                    for p in pizzas:
                        rows.append(
                            {
                                "id": p.id,
                                "name": p.name,
                                "ingredients": p.ingredients,
                                "price": f"{float(p.price_chf):.2f}",
                            }
                        )

                    table = ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")

                    table.add_slot(
                        "body-cell-actions",
                        r"""
                        <q-td :props="props">
                            <div class="row items-center justify-center q-gutter-sm">
                                <q-btn dense outline label="−" @click="$parent.$emit('remove_one', props.row.id)" />
                                <q-btn dense outline label="+" @click="$parent.$emit('add_one', props.row.id)" />
                            </div>
                        </q-td>
                        """,
                    )
                    table.on("add_one", lambda e: (order_controller.add_one(e.args), refresh_cart()))
                    table.on("remove_one", lambda e: (order_controller.remove_one(e.args), refresh_cart()))

                # right: cart
                with ui.column().classes("w-1/3"):
                    ui.markdown("## Current order")
                    cart_container = ui.column().classes("w-full")

                    def refresh_cart() -> None:
                        cart_container.clear()
                        lines = order_controller.cart_lines()
                        subtotal, discount, total = order_controller.totals()

                        with cart_container:
                            if not lines:
                                ui.label("Cart is empty. Add pizzas from the menu 👈")
                            else:
                                for line in lines:
                                    with ui.row().classes("w-full items-center justify-between"):
                                        ui.label(f"{line.quantity}× {line.pizza.name}")
                                        ui.label(f"CHF {line.line_total_chf:.2f}")
                                ui.separator()
                                ui.label(f"Subtotal: CHF {subtotal:.2f}")
                                if discount > 0:
                                    ui.label(f"Discount (10% > CHF 50): −CHF {discount:.2f}")
                                else:
                                    ui.label("Discount: CHF 0.00")
                                ui.label(f"Total: CHF {total:.2f}").classes("text-lg font-bold")

                                with ui.row().classes("gap-2"):
                                    ui.button("Clear", on_click=lambda: (order_controller.clear_cart(), refresh_cart())).props("outline")
                                    ui.button("Checkout & create invoice", on_click=lambda: do_checkout()).props("color=primary")

                    def do_checkout() -> None:
                        try:
                            order, invoice_path = order_controller.checkout()
                        except ValueError as ex:
                            ui.notify(str(ex), type="warning")
                            return
                        ui.notify(f"Order #{order.id} saved. Invoice created: {invoice_path}", type="positive")
                        refresh_cart()

                    refresh_cart()

            ui.link("Admin: Past transactions", "/admin").classes("mt-6")

        @ui.page("/admin")
        def admin_page() -> None:
            ui.markdown("# 🔐 Admin – Past transactions")
            ui.link("← Back to menu", "/")

            orders = admin_controller.list_transactions(limit=200)
            if not orders:
                ui.label("No transactions yet.")
                return

            columns = [
                {"name": "id", "label": "Order", "field": "id", "align": "left"},
                {"name": "created_at", "label": "Created (UTC)", "field": "created_at", "align": "left"},
                {"name": "subtotal", "label": "Subtotal (CHF)", "field": "subtotal", "align": "right"},
                {"name": "discount", "label": "Discount (CHF)", "field": "discount", "align": "right"},
                {"name": "total", "label": "Total (CHF)", "field": "total", "align": "right"},
            ]
            rows = []
            for o in orders:
                local_time = o.created_at.replace(tzinfo=timezone.utc).astimezone(ZoneInfo("Europe/Zurich"))
                rows.append(
                    {
                        "id": o.id,
                        "created_at": local_time.strftime("%d.%m.%Y %H:%M"),
                        "subtotal": f"{o.subtotal_chf:.2f}",
                        "discount": f"{o.discount_chf:.2f}",
                        "total": f"{o.total_chf:.2f}",
                    }
                )

            ui.table(columns=columns, rows=rows, row_key="id").classes("w-full")
            ui.label("Invoices are saved in the local 'invoices/' folder as invoice_<order_id>.pdf.")
