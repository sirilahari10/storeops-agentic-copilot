# StoreOps Agentic AI: Associate Copilot PoW

Machine learning is great, but as Mani Pantangi recently noted, real operational readiness requires prioritizing **"Tools over models."** 

I built this Proof of Work for the Associate Data Scientist role to demonstrate how I would bridge advanced analytics with Agentic AI to solve real-world Home Depot Store Operations problems.

## The Architecture
1. **The Context Layer (`bigquery_inventory_optimization.sql`):** 
   A foundational SQL pipeline (simulating BigQuery) that creates the "truth" for the agent—identifying out-of-stock risks and associate scheduling gaps.
2. **The Agentic Tool (`store_associate_agent.py`):** 
   A Python-based semantic router that takes a store associate's natural language query (e.g., *"Where is the overflow for SKU 123?"*) and routes it to the correct deterministic SQL tool, reducing hallucinations and driving real operational impact.
