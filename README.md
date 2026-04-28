# 🍕 PizzaRP – Pizzeria Reference Project (Browser App)

![UI Showcase](docs/ui-images/ui_showcase.png)

---

This project demonstrates the development of a browser-based application using **NiceGUI**, focusing on clean architecture, data validation, and database integration via an ORM.

It aims to:

- Cover the full process from **requirements analysis to implementation**
- Apply advanced **Python** concepts in a web-based application
- Demonstrate **data validation**, layered architecture, and ORM usage
- Produce clean, maintainable, and well-tested code
- Support **teamwork and professional documentation**

---

## 📝 Application Requirements

### Problem

In small pizzerias, orders and totals are often calculated manually. This leads to errors, inconsistent pricing, and incorrect discounts.

---

### Scenario

The application allows users to:
- select pizzas from a menu
- manage their order
- automatically calculate totals (including discounts)
- store orders in a database
- generate invoices as PDF files

---

## 📖 User Stories

### 1. View Pizza Menu
**As a user, I want to see the pizza menu in the browser app.**

- **Inputs:** none  
- **Outputs:** list of pizzas (`list[Pizza]`)

---

### 2. Manage Order and View Running Total
**As a user, I want to add or remove pizzas and see the running total.**

- **Inputs:** pizza ID (`int`), action (`add | remove`)  
- **Outputs:** updated order, subtotal, discount, total  

---

### 3. Automatic Discount
**As a user, I want a 10% discount applied automatically if the subtotal exceeds 50 CHF.**

- **Inputs:** subtotal (`float`)  
- **Outputs:** discount, total  

---

### 4. Generate Invoice
**As a user, I want an invoice to be created and saved as a file.**

- **Inputs:** completed order  
- **Outputs:** PDF invoice, file path  

---

### 5. View Past Transactions (Admin)
**As an admin, I want to view past transactions ordered by date.**

- **Inputs:** optional limit (`int`)  
- **Outputs:** list of orders (`list[Order]`)  

---

## 🧩 Use Cases

![UML Use Case Diagram](docs/architecture-diagrams/uml_use_case_diagram.png)

### Main Use Cases
- Show Menu (Customer)  
- Manage Order (Customer)  
- View Order and Total (Customer)  
- Checkout & Generate Invoice (Customer)  
- View Transactions (Admin)  

### Actors
- Customer  
- Admin  

---

### Wireframes / Mockups

> 🚧 Add screenshots of the wireframe mockups you chose to implement.

![Wireframes – Home/Transactions](docs/ui-images/wireframes.png)

---

## 🏛️ Architecture

![UML Class Diagram](docs/architecture-diagrams/uml_class_architecture.png)

### Layers
- **UI:** NiceGUI (browser-based interface)  
- **Application logic:** controllers and services  
- **Persistence:** SQLite + ORM + data access (DAO)  

### Design Decisions
- MVC structure (Model–View–Controller)
- Clear separation of concerns
- Business logic independent of UI

### Design Patterns Used
- Model-View-Controller / Layered MVC Variant: MVC makes sense here because the application has a graphical user interface, user interactions, business objects, and database access. Separating these responsibilities makes the project easier to understand, test, and extend.  
- Facade Pattern:  Facade makes sense because database setup involves several technical details. The rest of the application should not need to know how the database engine, tables, initial data, and sessions are created.   
---

## 🗄️ Database and ORM

![ER Diagram](docs/architecture-diagrams/er_diagram.png)

The application uses **SQLModel** to map domain objects to a SQLite database.

### Entities
- `Pizza`
- `Order`
- `OrderItem`

### Relationships
- One `Order` → many `OrderItem`
- Each `OrderItem` references one `Pizza`

---


## ✅ Project Requirements

---

> 🚧 Requirements act as a contract: implement and demonstrate each point below.

Each app must meet the following criteria in order to be accepted (see also the official project guidelines PDF on Moodle):

1. Using NiceGUI for building an interactive web app
2. Data validation in the app
3. Using an ORM for database management

---

### 1. Browser-based App (NiceGUI)

> 🚧 In this section, document how your project fulfills each criterion.

The application interacts with the user via the browser. Users can:

- View the pizza menu
- Select pizzas and quantities
- See the running total
- Receive an invoice generated as a file

**Architecture note (per SS26 guidelines):** the browser is a thin client; UI state + business logic live on the server-side NiceGUI app.

---

### 2. Data Validation

The application validates all user input to ensure data integrity and a smooth user experience.
These checks prevent crashes and guide the user to provide correct input, matching the validation requirements described in the project guidelines.

---

### 3. Database Management

All relevant data is managed via an ORM (e.g. SQLModel or SQLAlchemy). For the pizza example this includes users, pizzas, and orders.

---

## ⚙️ Implementation

### Technology

- Python 3.x  
- NiceGUI  
- SQLModel / SQLAlchemy  
- ReportLab  
- pytest  

---

### 📚 Libraries Used

- **nicegui** – UI framework  
- **sqlmodel** – ORM  
- **sqlalchemy** – database toolkit  
- **reportlab** – PDF generation  
- **python-dotenv** – configuration  
- **pytest** – testing  
- **pytest-cov** – coverage  

---

## 📂 Repository Structure

```text
pizza_app/
├── __init__.py
├── __main__.py
├── application.py
├── data_access/
│   ├── __init__.py
│   ├── dao.py
│   ├── db.py
│   └── seed.py
├── domain/
│   ├── __init__.py
│   └── models.py
├── services/
│   ├── __init__.py
│   ├── invoice_service.py
│   ├── order_service.py
│   ├── pizza_service.py
│   └── pricing_service.py

└── ui/
    ├── __init__.py
    ├── controllers.py
    └── pages.py
```
---

### How to Run

> 🚧 Adjust to your project.

### 1. Project Setup
- Python 3.13 (or the course version) is required
- Create and activate a virtual environment:
   - **macOS/Linux:**
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```
   - **Windows:**
      ```bash
      python -m venv .venv
      .venv\Scripts\Activate
      ```
- Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 2. Configuration
- E.g., setup of parameters or environment variables

### 3. Launch
- Start the NiceGUI app (example):
   ```bash
   py -m pizza_app
   ```
- Open the URL printed in the console.

### 4. Usage (document as steps)

> 🚧 Describe the usage of the main functions

Order Pizza:
1. Open the menu page and browse pizzas.
2. Add items (with quantities) to the current order.
3. Review total (incl. discounts) and validate inputs.
4. Checkout to persist the order and generate the invoice.

> 🚧 Add UI screenshots of the main screens (or a short video link):

![UI – Checkout](docs/ui-images/ui_checkout_screen.png)
![UI – Past Transactions](docs/ui-images/ui_past_transactions_screen.png)

---

## 🧪 Testing

> 🚧 Explain what you test and how to run tests.

**Test mix:**
- Overall 12 tests
- 6 Unit tests: e.g. subtotal calculation, discount application above CHF 50, no discount at or below threshold, total calculation
- 3 DB tests: e.g. menu query returns seeded pizzas, saving an order persists order + order items, empty DB / empty transactions behavior
- 3 Integration tests: e.g. checkout with one pizza creates order and invoice, checkout with multiple pizzas applies discount correctly

**Template for writing test cases**
1. Test case ID – unique identifier (e.g., TC_001)
2. Test case title/description – What is the test about?
3. Preconditions: Requirements before executing the test
4. Test steps: Actions to perform
5. Test data/input
6. Expected result
7. Actual result
8. Status – pass or fail
9. Comments – Additional notes or defect found

---

## 👥 Team & Contributions

> 🚧 Fill in the names of all team members and describe their individual contributions below.

| Name      | Contribution |
|-----------|--------------|
| Student A | NiceGUI UI + documentation |
| Student B | Database & ORM + documentation |
| Student C | Business logic + documentation |

---

## 📝 License

This project is provided for **educational use only** as part of the Advanced Programming module.

[MIT License](LICENSE)