  Brent_Oil_Price_Movement_With_Political_and_Economic_Events
The main goal of this analysis is to study how important events affect Brent oil prices. This will focus on finding out how changes in oil prices are linked to big events like political decisions, conflicts in oil-producing regions, global economic sanctions, and changes in Organization of the Petroleum Exporting Countries (OPEC) policies.


   ✅ Interim Deliverables

This submission includes:

1.   1–2 Page Interim Report    
   - Data analysis workflow  
   - Event dataset (`events.csv`) with dates, types, and expected impacts  
   - Assumptions and limitations (including correlation vs. causation)  
   - Communication strategy for stakeholders  
   - Understanding of time series properties and Bayesian modeling  

2.   Structured Event Dataset (`data/events.csv`)    
   - 15 key events from 1987–2022 (e.g., OPEC cuts, wars, sanctions, pandemics)  
   - Fields: `event_name`, `event_date`, `event_type`, `description`, `expected_impact`

3.   GitHub Repository with Initial Code    
   - `src/EDA.py`: Loads data, parses mixed date formats, plots price trends and log returns  
   - Ready for Bayesian modeling in PyMC3

🔍 Key Insights from EDA

-   Non-stationary trend  : Brent prices show long-term fluctuations with sharp shocks (e.g., 2008 crisis, 2020 crash).
-   Volatility clustering  : Log returns reveal periods of high uncertainty (e.g., 2020, 2022).
-   Mixed date formats  : Data contains both `20-May-87` and `Apr 22, 2020` → handled using `pd.to_datetime(..., format='mixed', dayfirst=True)`.

> 📈 Plots generated:  
> - Raw price over time  
> - Log returns  
> - 30-day rolling volatility

🧠 Modeling Approach (Planned for Final Submission)

Bayesian Change Point Detection with PyMC3
- Detect structural breaks in mean or volatility of log returns
- Define `tau` (change point) ~ DiscreteUniform
- Use `pm.math.switch()` to model pre/post behavior
- Sample posterior with MCMC to get probabilistic insights

 Expected Outputs
- Most probable change point dates
- Parameter shifts (e.g., mean, volatility)
- Probabilistic statements (e.g., “95% chance of increased volatility after Mar 8, 2020”)
- Event correlation and impact quantification

⚠️ Assumptions & Limitations

| Category | Details |
|--------|-------|
|   Assumptions   | - Structural breaks are linked to major events<br>- Log returns are approximately stationary<br>- One or few abrupt changes explain key shifts |
|   Limitations   | - Correlation ≠ Causation<br>- Latency effects not modeled<br>- Multiple concurrent events hard to isolate<br>- Model assumes abrupt changes; may miss gradual shifts |

> 🔍   Critical Note  : This analysis generates   hypotheses  , not proof of causation. Results should be interpreted alongside domain expertise.

📣 Communication Strategy

| Stakeholder | Format | Key Message |
|-----------|--------|-----------|
|   Investors   | Interactive Dashboard + Summary Cards | Highlight volatility windows and trading signals |
|   Policymakers   | PDF Report + Executive Summary | Emphasize energy security and market stability |
|   Energy Executives   | Dashboard + Operational Brief | Focus on cost forecasting and supply chain risk |
|   Internal Team   | Jupyter Notebooks + GitHub | Full code, reproducibility, model diagnostics |

🚀 Next Steps (Final Submission Plan)

- [ ] Build Bayesian change point model in PyMC3
- [ ] Identify 3–5 major change points and link to events
- [ ] Quantify impacts (e.g., price shift, volatility increase)
- [ ] Develop interactive dashboard using   Flask (backend)   and   React (frontend)  
- [ ] Publish final   blog post or PDF report  

📚 References

- [Change Point Detection with PyMC3](https://forecastegy.com/posts/change-point-detection-time-series-python/)
- [Bayesian Inference with PyMC](https://www.pymc.io/blog/chris_F_pydata2022.html)
- [Data Science Workflow](https://towardsdatascience.com/mastering-the-data-science-workflow-2a47d8b613c4)
- [MCMC Explained](https://towardsdatascience.com/monte-carlo-markov-chain-mcmc-explained-94e3a6c8de11)

 🧑‍💻 Author

Firaol Delesa  
Data Scientist | 10 Academy: Artificial Intelligence Mastery  
Email: [firaoldelesa18@gmail.com]  
LinkedIn: [linkedin.com/in/firaoldelesa] 
GitHub: [FiraolD](https://github.com/FiraolD)