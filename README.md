```markdown
# 🧠 AI-Powered Database Schema Optimizer

A smart backend system that converts plain English descriptions of entities, business logic, and data structures into a fully normalized SQL schema using advanced generative AI. Just describe your data needs — the system does the rest.

---

## 🚀 Features

- 📄 **Natural Language Input** — Write your schema requirements in plain English.
- ♻️ **Schema Generation** — Automatically builds tables, attributes, foreign keys, and junction tables.
- 🔗 **Relationship Detection** — Handles 1:1, 1:N, and N:M cardinalities with correct constraints.
- 🤖 **AI Models Powered by Gemini 1.5 Flash** — Ensures highly accurate interpretation.
- ⚡ **FastAPI Application** — Clean, fast REST API with full Swagger docs.
- 📦 **Dockerized Setup** — One-command launch with Docker & Docker Compose.

---

## 🧠 How it Works

1. ✍️ **User Input** – You provide the schema description using natural language.
2. 🧠 **AI Interpretation** – Google Gemini model extracts entities, attributes, and relationships.
3. 🛠️ **Schema Planning** – Translates the plan into fully normalized DDL.
4. 📤 **API Output** – Returns the complete SQL script as JSON.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ai-db-optimizer
```

### 2. Add your API key

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_google_api_key_here
```

Make sure `.env` is excluded in your `.gitignore`.

### 3. Launch the app

```bash
docker compose up --build
```

This will:
- Start the FastAPI server
- Connect a PostgreSQL database
- Expose the API at `http://localhost:8000`

---

## 🎯 Usage

Send a request to the `/process` endpoint:

### POST /process

#### Example Input

```json
{
  "text": "A Customer places many Orders. An Order can contain many Products, and a Product can be in many Orders. A Product has a name and a price."
}
```

#### Example Output

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
  "plan_id": "plan_xyz123"
}
```

You can also access interactive Swagger docs here:  
📄 `http://localhost:8000/docs`

---

## 🔌 API Reference

| Method | Endpoint    | Description                     |
|--------|-------------|---------------------------------|
| GET    | `/health`   | API health status               |
| POST   | `/process`  | Translate text to SQL schema    |

---

## 🧱 Project Structure

```
.
├── main.py               # FastAPI app with endpoints
├── models.py             # Request/response schema models
├── Dockerfile            # Application container config
├── docker-compose.yml    # Multi-service orchestration
├── requirements.txt      # Python dependencies
└── .env                  # Your Gemini API key
```

---

## 🔮 Future Improvements

- 🧪 **/schema/apply Endpoint** — Execute the generated schema directly into a sandbox database
- ⚙️ **Query Generation** — Auto-create common queries (SELECT/INSERT/UPDATE)
- 🚀 **Index Recommendation** — Suggest primary keys and performance indexes
- 📈 **Schema Migrations** — Safely alter existing database state on new input

---

## ✅ Health Check

Use `/health` to verify readiness:

```json
{ "status": "ok" }
```

---

## 🧾 License

MIT License — use freely, improve collaboratively.
```
