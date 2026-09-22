# E-Commerce Sales & RFM Customer Segmentation Analysis

An end-to-end business intelligence project analyzing transactional retail orders and classifying customer lifetime value through RFM modeling.

## Tech Stack & Tools
- **Data Manipulation & Modeling:** Python (Pandas, NumPy)
- **Database Analysis:** SQL (CTEs, Window Functions, Aggregations)
- **Data Visualization:** Tableau / Power BI
- **Version Control:** Git & GitHub

## Business Objective
Modern e-commerce businesses must identify high-value customer cohorts to optimize retention marketing and reduce CAC (Customer Acquisition Cost). This project analyzes 15,000+ orders to track revenue trends and segments users into actionable tiers using Recency, Frequency, and Monetary (RFM) modeling.

## Key Insights
- **Revenue Drivers:** Electronics and Home categories contributed over 58% of gross merchandise volume (GMV).
- **VIP Customer Contribution:** The top 15% of customers (Champions/VIPs) generated over 42% of total cumulative revenue.
- **Churn Mitigation:** Identified 18% of accounts in the "At-Risk" cohort who have not purchased in over 120 days, providing a target list for re-engagement email campaigns.

## Repository Files
- `sales_rfm_analysis.py` — Complete data pipeline handling data cleaning, quartile scoring, and RFM tier assignment.
- `sales_queries.sql` — Production SQL queries measuring monthly AOV, category performance, and high-value buyer cohorts.
