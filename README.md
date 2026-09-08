# StoreOps: Inventory Discrepancy & Task Optimization

In high-volume retail environments, associates juggle customer queries, shelf replenishment, and localized stock discrepancies. 

This repository models a lightweight operational analytics layer designed to bridge store telemetry with associate task workflows:
1. **Discrepancy Analytics (`inventory_risk.sql`):** Identifies high-shrink, low-stock bays where velocity outpaces automated inventory counts.
2. **Function-Calling Task Dispatcher (`copilot_dispatcher.py`):** Uses structured function schemas to route operational intents to analytical queries.

