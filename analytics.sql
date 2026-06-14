-- Query 1: Regional Carrier Reliability and Performance KPI Matrix
SELECT 
    region,
    delivery_partner,
    COUNT(*) AS total_consignments,
    ROUND(SUM(target_delayed) * 100.0 / COUNT(*), 2) AS sla_breach_rate_pct,
    ROUND(AVG(delivery_cost), 2) AS avg_cost_inr,
    ROUND(AVG(delivery_rating), 2) AS average_customer_rating
FROM india_logistics_warehouse
GROUP BY region, delivery_partner
ORDER BY region, sla_breach_rate_pct DESC;

-- Query 2: Weather Interferences and System Disruption Index
SELECT 
    weather_condition,
    COUNT(*) AS tracking_count,
    ROUND(AVG(delivery_time_hours_clean), 2) AS average_transit_hours,
    ROUND(AVG(delivery_cost), 2) AS average_cost_inr,
    ROUND(SUM(CASE WHEN delivery_status = 'failed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS return_failure_rate_pct
FROM india_logistics_warehouse
GROUP BY weather_condition
ORDER BY average_transit_hours DESC;
