"""
StoreOps Dispatcher: Demonstrates structured function schema routing
and deterministic execution against local store data.
"""
import duckdb
import json

# Setup in-memory database simulating BigQuery StoreOps tables
con = duckdb.connect(database=':memory:')

con.execute("""
CREATE TABLE store_inventory (
    sku VARCHAR,
    description VARCHAR,
    bay_location VARCHAR,
    on_hand INT,
    safety_stock INT
);

INSERT INTO store_inventory VALUES 
('SKU-101', 'DeWalt 20V Cordless Drill', 'Aisle 4, Bay 12', 3, 10),
('SKU-102', 'Milwaukee M18 Fuel Saw', 'Aisle 4, Bay 15', 18, 5),
('SKU-103', '3-in-1 Interior Primer 1Gal', 'Aisle 9, Bay 02', 1, 8);
""")

def get_inventory_status(sku: str) -> dict:
    """Deterministic lookup tool executed by the agent layer."""
    query = f"SELECT * FROM store_inventory WHERE sku = '{sku}'"
    result = con.execute(query).df()
    if result.empty:
        return {"status": "NOT_FOUND", "message": f"No records for {sku}"}
    
    row = result.iloc[0].to_dict()
    row["needs_restock"] = bool(row["on_hand"] < row["safety_stock"])
    return row

def list_restock_priorities() -> list:
    """Pulls bays where inventory has fallen below critical thresholds."""
    query = """
    SELECT bay_location, sku, description, on_hand, safety_stock
    FROM store_inventory
    WHERE on_hand < safety_stock
    ORDER BY (safety_stock - on_hand) DESC
    """
    return con.execute(query).df().to_dict(orient='records')

# Available Tool Schemas (Matches OpenAI/Vertex AI Function Calling format)
TOOLS = [
    {
        "name": "get_inventory_status",
        "description": "Look up physical location and on-hand counts for a specific SKU",
        "parameters": {"type": "object", "properties": {"sku": {"type": "string"}}}
    },
    {
        "name": "list_restock_priorities",
        "description": "Retrieve prioritized bays requiring immediate shelf replenishment",
        "parameters": {"type": "object", "properties": {}}
    }
]

if __name__ == "__main__":
    print("--- Executing Sample Tool Dispatch ---")
    print("Priority Restocks:", json.dumps(list_restock_priorities(), indent=2))
    print("\nSKU-101 Lookup:", json.dumps(get_inventory_status("SKU-101"), indent=2))
