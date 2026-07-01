# lg-market-intelligence-pipelines
Portfolio look-through and competitor asset flow data pipelines
# Asset Management Market Intelligence Pipelines

This repository houses the structural data architecture designed to process institutional fund metrics, simulate competitor tracking, and build semantic layers for BI visualization.

## Engineering Architecture
* **Batch Data Pipelines:** The `/pipelines/portfolio_xray.py` script utilizes `pandas` transformation logic to perform an automated look-through analysis of multi-asset fund wrappers, calculating true net client concentrations.
* **Modern Data Warehousing (BigQuery):** The `/queries/competitor_flows.sql` production script uses advanced analytical window functions (`LAG()`) to isolate organic Net New Business (NNB) trends from market volatility, creating a clean semantic layer optimized for direct ingestion into Power BI.
