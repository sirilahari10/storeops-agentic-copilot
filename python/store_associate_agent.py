"""
StoreOps Agentic Router
Demonstrates 'Tools over models' by routing associate queries to deterministic functions 
rather than relying on LLM hallucinations.
"""

def tool_check_inventory(sku: str, store_id: str) -> str:
    # In production, this executes the BigQuery logic to find exact aisle/bay locations
    return f"Executing BigQuery Search: SKU {sku} is in Overhead Bay 4, Aisle 12."

def tool_optimize_schedule(store_id: str, day: str) -> str:
    # In production, this triggers an optimization algorithm for associate staffing
    return f"Executing Staffing Model: Peak traffic expected at 2 PM. Recommend moving 2 associates to Garden."

def associate_copilot_router(user_query: str):
    """
    Simulates the Context Layer. Parses intent and triggers the right tool.
    """
    query = user_query.lower()
    
    if "where is" in query or "sku" in query:
        print("[Agent Context] Intent: Inventory Location. Triggering SQL Tool.")
        return tool_check_inventory(sku="1001-234", store_id="09090")
        
    elif "schedule" in query or "busy" in query:
        print("[Agent Context] Intent: Workforce Optimization. Triggering ML Tool.")
        return tool_optimize_schedule(store_id="09090", day="Saturday")
        
    else:
        return "I can help with Inventory Location and Staffing Optimization. What do you need?"

# Example Associate Interaction
print(associate_copilot_router("Where is the overstock for SKU 1001-234?"))
