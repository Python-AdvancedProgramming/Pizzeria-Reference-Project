# 🍕 PizzaRP – Pizzeria Reference Project (Browser App)

---

> 🚧 This is a template repository for student project in the course Advanced Programming at FHNW, BSc BIT.  
> 🚧 Do not keep this section in your final submission.

---

This project is intended to:

- Practice the complete process from **problem analysis to implementation**
- Apply basic **Python** programming concepts learned in the Programming Foundations module
- Demonstrate the use of **console interaction, data validation, and file processing**
- Produce clean, well-structured, and documented code
- Prepare students for **teamwork and documentation** in later modules
- Use this repository as a starting point by importing it into your own GitHub account  
- Work only within your own copy — do not push to the original template  
- Commit regularly to track your progress

---

# 🍕 TEMPLATE for documentation

> 🚧 Please remove this paragraphs having "🚧". These are comments for preparing the documentation.

---

## 📝 Analysis

---

### Problem

> 🚧 Describe the real-world problem your application solves. (Not HOW, but WHAT)

💡 Example: In a small local pizzeria, the staff writes orders and calculates totals by hand. This causes mistakes and inconsistent orders or discounts.

---

### Scenario

> 🚧 Describe when and how a user will use your application

💡 Example: PizzaRP solves the part of the problem where orders and totals are created by letting a user select items from a menu and automatically generating a correct invoice.

---

### User stories

1. As a user, I want to see the pizza menu in the Browser App.
2. As a user, I want to select pizzas and see the running total.
3. As a user, I want discounts to be applied automatically.
4. As a user, I want an invoice to be created and saved as a file.

---

### Use cases

- Show Menu
- Create Order (choose pizzas)
- Show Current Order and Total
- Print Invoice (saved to `invoice_xxx.txt`)

---

## ✅ Project Requirements

---

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

---

### 2. Data Validation

The application validates all user input to ensure data integrity and a smooth user experience.
These checks prevent crashes and guide the user to provide correct input, matching the validation requirements described in the project guidelines.

---

### 3. Database Management

All relevant data is managed via an ORM (e.g. SQLModel or SQLAlchemy). For the pizza example this includes users, pizzas, and orders.

---

## ⚙️ Implementation

---

### Technology

- Python 3.x
- Environment: GitHub Codespaces
- External libraries (e.g. NiceGUI, SQLAlchemy, Pydantic)

---

### 📂 Repository Structure

```text
pizza-nicegui/
├─ README.md
├─ pyproject.toml                 # or requirements.txt
├─ .env.example                   # DATABASE_URL=sqlite:///data/pizza.db
├─ .gitignore
│
├─ app/
│  ├─ main.py                     # NiceGUI UI (menu + cart + checkout)
│  ├─ db.py                       # create_engine + session factory + init_db()
│  ├─ models.py                   # SQLAlchemy ORM models (User, Pizza, Order, OrderItem)
│  ├─ queries.py                  # query helpers (menu, orders)
│  ├─ pricing.py                  # subtotal/discount/total logic
│  ├─ invoice.py                  # generate invoice file
│  └─ seed.py                     # seed pizzas/users (optional)
│
├─ data/                          # sqlite database (gitignored)
├─ invoices/                      # generated invoices (gitignored)
└─ tests/
   ├─ test_pricing.py
   └─ test_invoice.py
```

---

### How to Run

> 🚧 Adjust if needed.

How to launch the NiceGUI app ...

---

### Libraries Used

- nicegui
- sqlalchemy / sqlmodel
- pydantic
- ...

---

## 👥 Team & Contributions

---

> 🚧 Fill in the names of all team members and describe their individual contributions below.

| Name      | Contribution |
|-----------|--------------|
| Student A | NiceGUI UI + documentation |
| Student B | Database & ORM + documentation |
| Student C | Business logic + documentation |

---

## 🤝 Contributing

---

> 🚧 This is a template repository for student projects.  
> 🚧 Do not change this section in your final submission.

- Use this repository as a starting point by importing it into your own GitHub account
- Work only within your own copy — do not push to the original template
- Commit regularly to track your progress

---

## 📝 License

---

This project is provided for **educational use only** as part of the Programming Foundations module.

[MIT License](LICENSE)
