import os
import json
import uuid  
from fastapi import FastAPI, HTTPException
from models import FullProcessRequest, IR, DDLBundle
import google.generativeai as genai


app = FastAPI(title="AI-Powered Database Schema Optimizer", version="2.1.1") # Final version
try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    model = None


def parse_text_to_ir(text: str) -> IR:
    prompt = f"""
    You are an expert database architect. Analyze the following user requirements and extract the database schema as a single, minified JSON object with no markdown.
    Requirements: "{text}"
    The JSON must have "entities" and "relationships" keys.
    - "entities" is an object where keys are singular, capitalized entity names and values are lists of their lowercase attributes.
    - If an entity has no attributes, its value MUST be an empty list: [].
    - Do not include primary key id fields in the attributes.
    - "relationships" is a list of objects, each with "from_entity", "to_entity", and "cardinality" keys ('1:1', '1:N', or 'N:M').
    Example: {{"entities":{{"User":["name"],"Post":[]}},"relationships":[{{"from_entity":"User","to_entity":"Post","cardinality":"1:N"}}]}}
    """
    try:
        response = model.generate_content(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        ir_data = json.loads(json_text)
        return IR(**ir_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse requirements: {str(e)}")

def generate_ddl_from_ir(ir: IR) -> DDLBundle:
    tables, junctions, foreign_keys = [], [], []
    def get_sql_type(attr): return "DECIMAL(10, 2)" if "price" in attr else "VARCHAR(255)"
    for entity, attributes in ir.entities.items():
        safe_attributes = [attr for attr in attributes if attr and attr.lower() != 'null']
        cols = [f"    id SERIAL PRIMARY KEY"] + [f"    {attr.lower()} {get_sql_type(attr)}" for attr in safe_attributes]
        tables.append(f"CREATE TABLE {entity.lower()}s (\n" + ",\n".join(cols) + "\n);")
    for rel in ir.relationships:
        from_table, to_table = f"{rel.from_entity.lower()}s", f"{rel.to_entity.lower()}s"
        if rel.cardinality == "1:N":
            fk_col = f"{rel.from_entity.lower()}_id"
            foreign_keys.append(f"ALTER TABLE {to_table} ADD COLUMN {fk_col} INTEGER REFERENCES {from_table}(id);")
        elif rel.cardinality == "N:M":
            j_table = f"{rel.from_entity.lower()}_{rel.to_entity.lower()}"
            fk1, fk2 = f"{rel.from_entity.lower()}_id", f"{rel.to_entity.lower()}_id"
            junctions.append(f"CREATE TABLE {j_table} (\n    {fk1} INTEGER REFERENCES {from_table}(id),\n    {fk2} INTEGER REFERENCES {to_table}(id),\n    PRIMARY KEY ({fk1}, {fk2})\n);")
    return DDLBundle(tables=tables, junctions=junctions, foreign_keys=foreign_keys, plan_id=f"plan_{uuid.uuid4()}")

#API Endpoints
@app.get("/health", tags=["System"])
def get_health():
    if not model: raise HTTPException(status_code=503, detail="Generative AI model is not configured.")
    return {"status": "ok"}

@app.post("/process", response_model=DDLBundle, tags=["Main Workflow"])
def process_text_to_schema(request: FullProcessRequest):
    if not model: raise HTTPException(status_code=503, detail="Generative AI model is not configured.")
    ir = parse_text_to_ir(request.text)
    ddl_bundle = generate_ddl_from_ir(ir)
    return ddl_bundle