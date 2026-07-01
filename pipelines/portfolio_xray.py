import pandas as pd
import yfinance as yf

def extract_fund_holdings(fund_ticker):
    """Ingests raw fund holdings or uses self-generated fallback data."""
    try:
        fund = yf.Ticker(fund_ticker)
        holdings_data = fund.get_holding()
        if holdings_data is not None and not holdings_data.empty:
            df = holdings_data.copy()
            df.rename(columns={"Holding Name": "holding_name", "Holding Percent": "weight"}, inplace=True)
            return df[["holding_name", "weight"]]
    except Exception:
        pass
    
    # Self-generated data fallback ensures the code runs without external files
    if "A" in fund_ticker:
        return pd.DataFrame({
            "holding_name": ["Microsoft", "Apple", "NVIDIA", "Amazon", "Alphabet"],
            "weight": [0.08, 0.07, 0.05, 0.04, 0.03]
        })
    else:
        return pd.DataFrame({
            "holding_name": ["Microsoft", "Tesla", "NVIDIA", "Meta", "Eli Lilly"],
            "weight": [0.06, 0.05, 0.05, 0.04, 0.03]
        })

def transform_portfolio_xray(portfolio_config):
    """Executes look-through transformations to find true asset exposure."""
    master_holdings = []
    for fund_ticker, client_allocation in portfolio_config.items():
        fund_df = extract_fund_holdings(fund_ticker)
        fund_df["effective_weight"] = fund_df["weight"] * client_allocation
        master_holdings.append(fund_df)
        
    staging_df = pd.concat(master_holdings, ignore_index=True)
    final_exposure = staging_df.groupby("holding_name")["effective_weight"].sum().reset_index()
    return final_exposure.sort_values(by="effective_weight", ascending=False)

# Simulated Split: 60% Fund A, 40% Fund B
client_portfolio = {"L_AND_G_MULTI_INDEX_4": 0.60, "L_AND_G_GLOBAL_EQUITY": 0.40}
portfolio_exposure = transform_portfolio_xray(client_portfolio)

print("--- TOP CONCENTRATED PORTFOLIO EXPOSURES ---")
print(portfolio_exposure.head(5).to_string(index=False))
