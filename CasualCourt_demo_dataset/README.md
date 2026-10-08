# CasualCourt Demo Dataset

Synthetic data for the e-commerce cancellation investigation.

Files:
- orders.csv
- supplier_events.csv
- inventory.csv
- payments.csv
- tickets.csv
- competitor_prices.csv (optional)
- investigation_config.json

Expected story:
Cancellation rate is normally about 8% and rises sharply to about 31% around day 42. Supplier B lead time increases around day 38; its SKU inventory falls around day 41; delivery problems and cancellations then increase.

Payment-related tickets are intentionally noisy: payment success remains about 99% and many tickets occur after cancellation.

Expected ranking:
1. Supplier / Delivery Disruption
2. Inventory Shortage (contributing factor/mediator)
3. Payment Failure (noisy/conflicting signal)
4. Competitor Pricing

The dataset supports an evidence-based investigation; it does not prove causality.
