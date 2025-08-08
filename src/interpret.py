# src/interpret.py
import arviz as az
import pymc as pm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the saved trace
trace = az.from_netcdf('Data/trace.nc')

# Print model summary
print(pm.summary(trace, var_names=['mu1', 'mu2', 'sigma1', 'sigma2', 'tau']))

# Plot trace plots
pm.plot_trace(trace, var_names=['mu1', 'mu2', 'sigma1', 'sigma2'])
plt.suptitle("Trace Plots (Check Convergence)")
plt.tight_layout()
plt.show()

# Extract posterior of tau (change point)
tau_posterior = trace.posterior['tau'].values.flatten()
median_tau = int(np.median(tau_posterior))

# Load the original data and ensure Date is parsed as datetime
df = pd.read_csv('Data/BrentOilPrices.csv')

# ✅ Critical: Parse Date again with mixed format support
df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)

# Sort by date
df = df.sort_values('Date').reset_index(drop=True)

# Compute LogReturn to align index
df['LogReturn'] = np.log(df['Price'] / df['Price'].shift(1))
df.dropna(subset=['LogReturn'], inplace=True)

# Now safely get the change date
change_date = df['Date'].iloc[median_tau]

# ✅ Now this will work
print(f"Most probable change point: Day {median_tau} → {change_date.strftime('%d-%b-%Y')}")

# Plot posterior distribution of tau
plt.figure(figsize=(10, 4))
plt.hist(tau_posterior, bins=50, density=True, alpha=0.7, color='skyblue')
plt.axvline(median_tau, color='red', linestyle='--', label=f'Median: {change_date.strftime("%d-%b-%Y")}')
plt.title('Posterior Distribution of Change Point (tau)')
plt.xlabel('Time Index')
plt.ylabel('Density')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plots/change_point_posterior.png', dpi=150)
plt.show()

# Quantify impact
mu1_samples = trace.posterior['mu1'].values.flatten()
mu2_samples = trace.posterior['mu2'].values.flatten()
sigma1_samples = trace.posterior['sigma1'].values.flatten()
sigma2_samples = trace.posterior['sigma2'].values.flatten()

prob_vol_increase = (sigma2_samples > sigma1_samples).mean()
avg_mean_shift = np.mean(mu2_samples - mu1_samples)
avg_volatility_change = np.mean(sigma2_samples - sigma1_samples)

print("\n" + "="*50)
print("         CHANGE POINT ANALYSIS RESULTS")
print("="*50)
print(f"Most Probable Change Date: {change_date.strftime('%d-%b-%Y')} (Index: {median_tau})")
print(f"Probability volatility increased: {prob_vol_increase:.1%}")
print(f"Average mean shift: {avg_mean_shift:.6f}")
print(f"Average volatility change: {avg_volatility_change:.6f}")
print("="*50)

# Save results to JSON for dashboard
results = {
    "change_date": change_date.strftime('%Y-%m-%d'),
    "change_date_str": change_date.strftime('%d-%b-%Y'),
    "median_tau": median_tau,
    "prob_vol_increase": float(prob_vol_increase),
    "mean_shift": float(avg_mean_shift),
    "volatility_change": float(avg_volatility_change)
}

import json
with open('Data/results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("✅ Results saved to Data/results.json")