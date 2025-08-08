# src/model.py
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az

def run_model():
    # Load the raw data
    df = pd.read_csv('Data/BrentOilPrices.csv')

    # Parse mixed date formats
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)

    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)

    # ✅ Compute Log Returns
    df['LogReturn'] = np.log(df['Price'] / df['Price'].shift(1))
    df.dropna(subset=['LogReturn'], inplace=True)

    # Extract returns for modeling
    returns = df['LogReturn'].values

    # Define the Bayesian Change Point Model
    with pm.Model() as model:
        # Prior for change point (tau)
        tau = pm.DiscreteUniform('tau', lower=100, upper=len(returns) - 100)

        # Priors for mean before and after
        mu1 = pm.Normal('mu1', mu=0, sigma=0.1)
        mu2 = pm.Normal('mu2', mu=0, sigma=0.1)

        # Priors for volatility (sigma)
        sigma1 = pm.HalfNormal('sigma1', sigma=0.1)
        sigma2 = pm.HalfNormal('sigma2', sigma=0.1)

        # Use switch to change parameters at tau
        mu = pm.math.switch(tau >= np.arange(len(returns)), mu1, mu2)
        sigma = pm.math.switch(tau >= np.arange(len(returns)), sigma1, sigma2)

        # Likelihood
        obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=returns)

        # Sample from posterior
        trace = pm.sample(
            draws=2000,
            tune=1000,
            return_inferencedata=True,
            progressbar=True,
            random_seed=42,
            cores=1  # Optional: reduce to 1 core if issues persist
        )

    # Save inference data
    az.to_netcdf(trace, 'Data/trace.nc')
    print("✅ Model sampling completed and saved.")

# 🔑 MUST HAVE: Protect the entry point
if __name__ == '__main__':
    run_model()