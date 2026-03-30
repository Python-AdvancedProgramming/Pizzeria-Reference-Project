"""Invoice generation service (PDF).

The invoice is generated on checkout and stored in `invoices/` as `invoice_<order_id>.pdf`.
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from ..domain.models import Order


class InvoiceService:
    """Create invoice PDF files for orders."""

    def __init__(self, invoice_dir: str) -> None:
        self.invoice_dir = invoice_dir

    def generate_pdf(self, order: Order) -> Path:
        """Generate and save an invoice PDF for a persisted order.

        Args:
            order: Order with items loaded, and an id.

        Returns:
            Path to the generated PDF.
        """
        if order.id is None:
            raise ValueError("Order must be persisted (needs an id) before invoice generation.")

        out_dir = Path(self.invoice_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"invoice_{order.id}.pdf"

        c = canvas.Canvas(str(out_path), pagesize=A4)
        width, height = A4

        y = height - 50
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "PizzaRP Invoice")
        y -= 25

        c.setFont("Helvetica", 10)
        created_str = order.created_at.isoformat(timespec="seconds")
        c.drawString(50, y, f"Order ID: {order.id}")
        y -= 15
        c.drawString(50, y, f"Date: {created_str}")
        y -= 25

        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Items")
        y -= 15
        c.setFont("Helvetica", 10)

        c.drawString(50, y, "Qty")
        c.drawString(90, y, "Pizza")
        c.drawRightString(width - 50, y, "Line total (CHF)")
        y -= 12
        c.line(50, y, width - 50, y)
        y -= 15

        for item in order.items:
            if y < 120:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            c.drawString(50, y, str(item.quantity))
            c.drawString(90, y, item.pizza.name if item.pizza else f"Pizza #{item.pizza_id}")
            c.drawRightString(width - 50, y, f"{item.line_total_chf:.2f}")
            y -= 14

        y -= 10
        c.line(50, y, width - 50, y)
        y -= 18

        c.drawRightString(width - 50, y, f"Subtotal: CHF {order.subtotal_chf:.2f}")
        y -= 14
        c.drawRightString(width - 50, y, f"Discount: CHF {order.discount_chf:.2f}")
        y -= 14
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(width - 50, y, f"Total: CHF {order.total_chf:.2f}")

        c.showPage()
        c.save()
        return out_path
