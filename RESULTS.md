# Results, traced to the notebook

Every number in the README comes from one run of
[`tanay_singh_reglab_takehome.ipynb`](tanay_singh_reglab_takehome.ipynb) on
30 September 2026, before submission. Each row below gives the text that cell
printed and the cell's execution count, so it can be found by searching the
notebook for `In [n]`. `python scripts/check_results.py` confirms that every
snippet is in the output of the cell it cites, and CI runs it on every push.

The dataset is not in this repository, so these are the saved outputs, not a
rerun. Values are as printed, usually rounded to three places.

## Data

| Quantity | Printed | Cell |
|---|---|---|
| Inspections, restaurants and date range | `13299 inspections, 1756 restaurants, 2006-01-03 to 2013-02-08` | In [2] |
| Inspections left after dropping the two -1 placeholder rows | `13297 inspections left` | In [3] |
| Rows sharing a restaurant and date (kept, different inspection IDs) | `171 rows share a restaurant and date` | In [3] |
| Share of inspections scoring exactly 0 | `share scoring 0: 0.217` | In [4] |
| Share serious (score 10 or more) | `share serious (10+): 0.674` | In [4] |
| Highest score | `max 124.000` | In [4] |
| Restaurants never serious | `never serious: 0.119` | In [5] |
| Restaurants serious at every inspection | `serious every time: 0.449` | In [5] |
| Correlation of score with previous score | `corr with previous score: 0.707` | In [5] |
| Share of score variance explained by restaurant | `share of variance explained by restaurant: 0.751` | In [5] |
| Serious share after a previous score of 0 | `(-1, 0] 0.308` | In [6] |
| Serious share after a previous score of 50 or more | `(49, 200] 0.974` | In [6] |
| Zip codes with 100 or more inspections | `23 zips with 100+ inspections` | In [6] |
| Lowest serious share among those zips | `98126 0.461` | In [6] |
| Highest serious share among those zips | `98144 0.859` | In [6] |
| Correlation of score with Yelp review count | `review_count -0.040` | In [7] |
| Correlation of score with Yelp rating | `avg_rating -0.023` | In [7] |
