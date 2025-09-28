# AI-Powered Database Schema Optimizer

## Overview
An intelligent system that ingests natural-language descriptions of data and business rules and generates a complete, optimized, and normalized SQL database schema. This project leverages Google's Gemini AI model to understand complex requirements and translate them into concrete, ready-to-use DDL (Data Definition Language) scripts.

## Features
- **Natural Language Processing**: Converts plain English descriptions into structured database schemas
- **Automatic Schema Generation**: Creates complete CREATE TABLE statements with proper data types
- **Relationship Inference**: Identifies 1:1, 1:N, and N:M relationships, generating appropriate foreign keys and junction tables
- **RESTful API**: Clean FastAPI interface for easy integration
- **Containerized**: Docker-based deployment for consistent environments

## Tech Stack
- **Backend**: Python 3.11 with FastAPI
- **AI Model**: Google Gemini 1.5 Flash
- **Database**: PostgreSQL (for testing)
- **Containerization**: Docker & Docker Compose

## Architecture
The system follows a simple pipeline:
1. Receives natural language input via API
2. Processes text through Gemini AI to extract entities and relationships
3. Generates normalized SQL schema with proper constraints
4. Returns complete DDL bundle ready for execution

## Installation

### Prerequisites
- Docker Desktop installed and running
- Google AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-db-optimizer
   ```

2. **Configure environment**
   Create `.env` file in project root:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

3. **Update docker-compose.yml**
   Replace the placeholder API key in the environment section:
   ```yaml
   environment:
     - GOOGLE_API_KEY=${GOOGLE_API_KEY}
   ```

4. **Launch the application**
   ```bash
   docker compose up --build
   ```

5. **Verify installation**
   Navigate to `http://localhost:8000/docs` to access the interactive API documentation

## API Usage

### Health Check
```bash
GET /health
```
Verifies the service and AI model are properly configured.

### Process Text to Schema
```bash
POST /process
```

**Request Body:**
```json
{
  "text": "A Customer places many Orders. An Order contains many Products. Products have name and price."
}
```

**Response:**
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
  "plan_id": "plan_uuid"
}
```

## How It Works

### 1. Text Analysis
The system uses Gemini AI to parse natural language and extract:
- **Entities**: Business objects (Customer, Order, Product)
- **Attributes**: Properties of entities (name, price)
- **Relationships**: Connections between entities with cardinality

### 2. Schema Generation
Based on the extracted information:
- Creates tables with appropriate columns and data types
- Adds primary keys to all tables
- Generates foreign keys for 1:N relationships
- Creates junction tables for N:M relationships

### 3. Data Type Inference
- Attributes containing "price" → `DECIMAL(10, 2)`
- All other attributes → `VARCHAR(255)`
- Primary keys → `SERIAL PRIMARY KEY`
- Foreign keys → `INTEGER REFERENCES`

## Example Use Cases

### E-commerce System
```
Input: "Customers have email and name. They place Orders with order_date. Orders contain Products with name, price, and description. Products belong to Categories with name."

Output: Complete schema with customers, orders, products, categories tables and appropriate relationships.
```

### Blog Platform
```
Input: "Users write Posts with title and content. Posts have many Comments with text. Users can like many Posts."

Output: Schema with users, posts, comments tables plus a user_post_likes junction table.
```

## Project Structure
```
ai-db-optimizer/
├── main.py              # FastAPI application and core logic
├── models.py            # Pydantic models for validation
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── docker-compose.yml  # Multi-container orchestration
└── .env               # Environment variables (create this)
```

## Development

### Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GOOGLE_API_KEY=your_key

# Run the application
uvicorn main:app --reload
```

### Adding New Features
1. Extend the IR model in `models.py` for additional metadata
2. Enhance the prompt in `parse_text_to_ir()` for better extraction
3. Modify `generate_ddl_from_ir()` to support new SQL features

## Troubleshooting

### Common Issues
- **503 Service Unavailable**: Check if GOOGLE_API_KEY is properly set
- **JSON Parse Error**: The AI response may be malformed; try rephrasing the input
- **Missing Relationships**: Be explicit about connections between entities

### Debug Mode
View container logs:
```bash
docker compose logs -f api
```

## Future Enhancements
- Schema migration support
- Index recommendation engine
- Query generation from natural language
- Support for multiple database dialects
- Schema visualization
- Data validation rules extraction

## License
This project is open source and available under the MIT License.
