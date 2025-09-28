```markdown
# 🧠 AI-Powered Database Schema Optimizer

An intelligent system that transforms human-written descriptions of data and business logic into fully optimized, normalized SQL database schemas. By leveraging generative AI (Google Gemini 1.5 Flash), this tool understands plain language requirements and delivers production-ready DDL scripts.

---

## 🚀 Features

- **Natural Language to Schema**: Translate business rules and entity relationships from plain English to SQL.
- **Schema Synthesis**: Generates `CREATE TABLE` statements with appropriate columns and data types.
- **Relationship Inference**: Detects `1:N` and `N:M` relationships and creates foreign keys or junction tables accordingly.
- **AI-Powered Understanding**: Uses Gemini for deep, contextual interpretation of user input.
- **FastAPI Backend**: Modern and interactive API layer built with Python and FastAPI.
- **Containerized Setup**: Easily deployable using Docker and Docker Compose.

---

## 🧱 Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **AI/NLP**: Google Gemini 1.5 Flash
- **Database**: PostgreSQL (Dockerized for sandbox)
- **Containerization**: Docker & Docker Compose

---

## ⚙️ Getting Started

Follow the steps below to spin up the environment locally.

### 1. Prerequisites

- Docker & Docker Compose
- Google Generative AI API key (get from [Google AI Studio](https://makersuite.google.com/))

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd ai-db-optimizer
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

Make sure `.env` is added to `.gitignore`.

### 4. Run the Application

```bash
docker compose up --build
```

This will build everything and start:

- FastAPI app (at `http://localhost:8000`)
- PostgreSQL database

---

## 🔍 Usage

### Primary Endpoint

**`POST /process`**

Sends natural language input and receives an auto-generated SQL schema.

#### Request Body

```json
{
  "text": "A Customer places many Orders. An Order can contain many Products, and a Product can be in many Orders. A Product has a name and a price."
}
```

#### Response

```json
{
  "tables": [
    "CREATE TABLE customers (\n    id SERIAL PRIMARY KEY\n);",
    "CREATE TABLE orders (\n    id SERIAL PRIMARY KEY\n);",
    "CREATE TABLE products (\n    id SERIAL PRIMARY KEY,\n    name VARCHAR(255),\n    price DECIMAL(10, 2)\n);"
  ],
  "junctions": [
    "CREATE TABLE order_products (\n    order_id INTEGER REFERENCES orders(id),\n    product_id INTEGER REFERENCES products(id),\n    PRIMARY KEY (order_id, product_id)\n);"
  ],
  "foreign_keys": [
    "ALTER TABLE orders ADD COLUMN customer_id INTEGER REFERENCES customers(id);"
  ],
  "plan_id": "plan_xxx..."
}
```

Explore and test via FastAPI Swagger docs at:  
**`http://localhost:8000/docs`**

---

## 📦 Project Structure

```
.
├── main.py              # FastAPI application
├── models.py            # Pydantic data models
├── Dockerfile           # Application Docker image
├── docker-compose.yml   # Docker Compose setup
├── requirements.txt     # Python dependencies
└── .env                 # API key (not checked into version control)
```

---

## 🔮 Future Work

- **Schema Execution**: Add endpoint to apply schema directly to a connected DB.
- **Query & Index Generation**: Auto-create CRUD operations and recommend indexes.
- **Migration Scripts**: Generate safe DDL migrations based on updated input.

---

## ✅ Health Check

**GET `/health`**  
Returns `{"status": "ok"}` if model is properly configured and running.

---

## 📖 License

This project is open-source and licensed under the MIT License.
```
