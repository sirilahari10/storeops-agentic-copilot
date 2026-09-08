-- BigQuery Model: Store Associate Workload & Inventory Gap Detection
-- Creates the Context Layer for the Agentic Copilot

WITH hourly_foot_traffic AS (
    SELECT 
        store_id,
        EXTRACT(HOUR FROM transaction_timestamp) AS hour_of_day,
        COUNT(DISTINCT transaction_id) AS checkout_volume
    FROM `homedepot-prod.store_ops.pos_transactions`
    WHERE transaction_date >= CURRENT_DATE() - 30
    GROUP BY 1, 2
),

inventory_health AS (
    SELECT 
        store_id,
        department_id,
        sku,
        on_hand_qty,
        safety_stock_threshold,
        -- Identify items that need immediate associate restocking
        IF(on_hand_qty < safety_stock_threshold, TRUE, FALSE) AS requires_restock_action
    FROM `homedepot-prod.supply_chain.store_inventory`
)

SELECT 
    t.store_id,
    t.hour_of_day,
    t.checkout_volume,
    COUNT(i.sku) AS high_priority_restocks
FROM hourly_foot_traffic t
LEFT JOIN inventory_health i ON t.store_id = i.store_id
WHERE i.requires_restock_action = TRUE
GROUP BY 1, 2, 3
ORDER BY high_priority_restocks DESC;
