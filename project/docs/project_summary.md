# Project Summary for a Non-Technical Reader

## The Decision Problem

An investment committee that holds broad China equities faces a recurring practical question: should it keep its normal CSI 300 exposure for the next month, or temporarily reduce exposure because market conditions have changed? The committee already has portfolio limits and experienced managers, but those controls do not always summarize how return, volatility, and trading participation are evolving together. A systematic regime signal can provide a consistent second opinion.

This project develops that second opinion. It studies whether the CSI 300 repeatedly moves through hidden market states and whether those states contain useful information for a 20-trading-day exposure decision. The result is deliberately simple: `risk_on` means maintain full benchmark exposure, while `risk_off` means use cash until the next scheduled review. The signal is advisory. It does not place an order, short the market, use leverage, or override the committee.

## What Was Built

The analysis starts with daily CSI 300 open, high, low, close, and volume history from January 2005 through August 2026. The live acquisition process first attempts Yahoo Finance and then uses an AkShare public index endpoint if Yahoo is unavailable. During the final data pull, Yahoo was rate-limited and AkShare supplied 5,261 daily observations. The exact source, retrieval time, date range, fallback result, and file checksum are preserved next to the raw data.

The raw file is validated and never manually edited. Cleaning code checks duplicate dates, price positivity, daily high/low consistency, volume, missing values, and chronological ordering. Genuine extreme market movements are retained because crisis observations are part of the problem, not automatically bad data. Seventy-one daily returns receive broad outlier flags for review. For model stability, the main scenario clips feature values using percentile boundaries calculated only inside each historical training window. A second scenario removes this treatment so its effect is visible.

Every 20 trading days, the pipeline creates four measurements using only information known on that date: the previous 20-day return, a return-to-volatility statistic, a change in recent trading volume, and the previous 10-day return. The future 20-day return is stored separately as the evaluation target. This separation is essential: a model that accidentally sees future information can appear impressive while being unusable in practice.

The model is a five-state Gaussian Hidden Markov Model. In plain language, it groups similar combinations of the four measurements into recurring hidden states. State numbers themselves have no fixed meaning; after each training update, the model examines the forward returns historically associated with each state. A positive state estimate leads to full exposure, and a negative estimate leads to cash. Training uses the most recent 100 period observations, updates every five signals, and never includes the return being predicted.

## What the Analysis Found

The chronological test contains 182 non-overlapping 20-day periods from September 2011 through August 2026. The model pays a simplified cost of five basis points whenever exposure changes. Over this test, the five-state signal produced an annualized return of 6.68%, annualized volatility of 16.27%, and a Sharpe ratio of 0.48. Its maximum drawdown was -39.98%. The CSI 300 buy-and-hold comparison produced a 3.45% annualized return, 21.15% volatility, a 0.26 Sharpe ratio, and a -42.64% maximum drawdown.

The model predicted the sign of the next period correctly 54.95% of the time. It was invested for 62.09% of test periods and changed exposure 71 times. These numbers describe a modest edge, not reliable foresight. The signal's apparent value comes from a combination of participation and avoidance, not from consistently forecasting the size of every return.

Alternative assumptions matter. A three-state model produced a 0.29 Sharpe ratio, and a four-state model produced 0.20. Keeping five states but removing feature clipping produced 0.23. Maximum drawdowns also changed across scenarios. This spread shows that the conclusion is not a universal property of HMMs; it depends on reasonable but contestable design choices.

Uncertainty is the strongest reason for restraint. A bootstrap analysis estimated the mean strategy-minus-benchmark return per 20-day period at about 0.17%, but its 95% interval ranged from approximately -0.41% to 0.74%. Because zero lies inside that interval, the evidence does not establish a dependable positive active return. The historical point estimate is encouraging, but it is not sufficient for production approval.

## What Should Not Be Relied On

The hidden states should not be interpreted as permanent economic regimes. Their numeric labels can change when the model is retrained, and a five-state Gaussian structure is only an approximation. The data are an index price series rather than a total-return investment product. Dividends, cash interest, taxes, market impact, and detailed implementation costs are omitted. The simplified full-exposure/cash portfolio also ignores the committee's actual holdings and constraints.

Historical relationships can change. Public data providers can revise records or alter schemas. Repeatedly comparing parameter choices creates selection risk, especially when the best historical scenario is emphasized. Finally, the local Flask API demonstrates reuse but is not authenticated, hardened, or approved for an investment-production network.

## Recommended Next Steps

The appropriate next step is a shadow run, not capital deployment. Generate the signal on schedule without trading, preserve every forecast before its outcome is known, and review a pre-registered forward sample. Independently validate the price series against a licensed source and replace simplified costs with the intended investment vehicle's full implementation assumptions. Test dividend-aware benchmarks and a nonzero cash return.

During shadow operation, monitor data freshness and schema, feature drift, rolling direction accuracy and Sharpe ratio, pipeline success, API latency, exposure concentration, and switching frequency. The project includes thresholds, alert recipients, rollback ownership, and a handoff plan. Any breached model threshold should suspend decision use until the risk chair reviews the data, assumptions, and scenario pack.

The project succeeds as a lifecycle artifact even if the model is ultimately rejected: it turns a stakeholder question into traceable data, leakage-safe features, a reproducible time-series model, explicit uncertainty, a decision-ready report, a reusable API, and operational controls. Its present recommendation is disciplined continuation of research with clear evidence requirements.
