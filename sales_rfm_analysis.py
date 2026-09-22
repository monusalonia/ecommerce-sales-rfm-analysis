"""
E-Commerce Sales Performance & RFM Segmentation
Author: Monu Salonia
Tools: Python (Pandas, NumPy)
"""

from datetime import timedelta
import numpy as np
import pandas as pd


def generate_sales_data(n_orders: int = 15000) -> pd.DataFrame:
    """Generates synthetic transactional e-commerce order records."""
    np.random.seed(42)

    order_ids = [f"ORD-{i:06d}" for i in range(1, n_orders + 1)]
    customer_pool = [f"USER-{i:04d}" for i in range(1, 1201)]
    customer_ids = np.random.choice(customer_pool, size=n_orders)

    order_dates = pd.date_range("2025-01-01", "2025-12-31", periods=n_orders)

    categories = [
        "Electronics",
        "Home & Kitchen",
        "Fashion",
        "Sports",
        "Beauty",
    ]
    product_category = np.random.choice(
        categories, size=n_orders, p=[0.25, 0.25, 0.20, 0.15, 0.15]
    )

    quantity = np.random.choice([1, 2, 3, 4, 5], size=n_orders, p=[0.5, 0.25, 0.15, 0.07, 0.03])
    price_per_unit = np.where(
        product_category == "Electronics",
        np.random.uniform(800.0, 5000.0, size=n_orders),
        np.where(
            product_category == "Fashion",
            np.random.uniform(400.0, 2000.0, size=n_orders),
            np.random.uniform(200.0, 1500.0, size=n_orders),
        ),
    )
    order_amount = np.round(quantity * price_per_unit, 2)

    df = pd.DataFrame(
        {
            "order_id": order_ids,
            "customer_id": customer_ids,
            "order_date": order_dates,
            "category": product_category,
            "quantity": quantity,
            "total_amount": order_amount,
        }
    )

    # Simulate dirty data (canceled returns with negative amounts & missing dates)
    df.loc[10:14, "total_amount"] = -100.0
    df.loc[20:23, "category"] = None
    return df


def clean_order_data(df: pd.DataFrame) -> pd.DataFrame:
    """Filters invalid transactions and cleans missing records."""
    initial_len = len(df)
    df_clean = df.dropna(subset=["category", "customer_id", "order_date"]).copy()
    df_clean = df_clean[df_clean["total_amount"] > 0]
    df_clean["order_date"] = pd.to_datetime(df_clean["order_date"])
    print(
        f"[INFO] Cleaned orders: {len(df_clean)} / {initial_len} ({len(df_clean)/initial_len:.2%})"
    )
    return df_clean


def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Computes Recency, Frequency, and Monetary metrics for each customer."""
    snapshot_date = df["order_date"].max() + timedelta(days=1)

    rfm = (
        df.groupby("customer_id")
        .agg(
            Recency=("order_date", lambda x: (snapshot_date - x.max()).days),
            Frequency=("order_id", "count"),
            Monetary=("total_amount", "sum"),
        )
        .reset_index()
    )

    # Score RFM from 1 to 4 using quartiles
    rfm["R_Score"] = pd.qcut(rfm["Recency"], q=4, labels=[4, 3, 2, 1]).astype(int)
    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"), q=4, labels=[1, 2, 3, 4]
    ).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], q=4, labels=[1, 2, 3, 4]).astype(int)

    rfm["RFM_Total"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

    # Customer Tier Assignment
    def assign_segment(score):
        if score >= 10:
            return "Champions / VIP"
        elif score >= 8:
            return "Loyal Customers"
        elif score >= 5:
            return "Potential / Regular"
        else:
            return "At-Risk / Inactive"

    rfm["Customer_Segment"] = rfm["RFM_Total"].apply(assign_segment)
    return rfm


def run_summary(orders_df: pd.DataFrame, rfm_df: pd.DataFrame):
    """Outputs high-level business analytics."""
    print("\n--- 1. Category Performance & Revenue ---")
    cat_summary = (
        orders_df.groupby("category")
        .agg(Total_Sales=("total_amount", "sum"), Total_Orders=("order_id", "count"))
        .reset_index()
    )
    cat_summary["Total_Sales"] = cat_summary["Total_Sales"].map("₹{:,.2f}".format)
    print(cat_summary.to_string(index=False))

    print("\n--- 2. RFM Customer Segments Breakdown ---")
    segment_counts = (
        rfm_df.groupby("Customer_Segment")
        .agg(
            Customer_Count=("customer_id", "count"),
            Avg_Spend=("Monetary", "mean"),
            Avg_Orders=("Frequency", "mean"),
        )
        .reset_index()
    )
    segment_counts["Avg_Spend"] = segment_counts["Avg_Spend"].map("₹{:,.2f}".format)
    print(segment_counts.to_string(index=False))

    rfm_df.to_csv("rfm_customer_segments.csv", index=False)
    print("\n[SUCCESS] Exported 'rfm_customer_segments.csv' for Tableau ingestion.")


if __name__ == "__main__":
    raw_orders = generate_sales_data(n_orders=15000)
    cleaned_orders = clean_order_data(raw_orders)
    rfm_results = calculate_rfm(cleaned_orders)
    run_summary(cleaned_orders, rfm_results)
