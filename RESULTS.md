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

## The label check

| Quantity | Printed | Cell |
|---|---|---|
| Restaurants with no Asian or ethnic label | `Neither 1022` | In [8] |
| Restaurants with an Asian label | `Asian 499` | In [8] |
| Restaurants with an ethnic but not Asian label | `Other ethnic 234` | In [8] |
| Asian: restaurants, inspections, mean score, mean previous score | `Asian 499 4060 59.765 59.115` | In [9] |
| Neither: restaurants, inspections, mean score, mean previous score | `Neither 1022 7438 10.022 9.597` | In [9] |
| Other ethnic: restaurants, inspections, mean score, mean previous score | `Other ethnic 234 1799 60.806 58.713` | In [9] |
| Asian: share scoring 0, share serious | `Asian 0.001 0.995` | In [9] |
| Neither: share scoring 0, share serious | `Neither 0.387 0.422` | In [9] |
| Other ethnic: share scoring 0, share serious | `Other ethnic 0.003 0.994` | In [9] |
| Asian: previous score column matches the file's earlier score, back to back pairs | `Asian 0.013 3137` | In [10] |
| Neither: the same match rate and pair count | `Neither 0.951 5709` | In [10] |
| Other ethnic: the same match rate and pair count | `Other ethnic 0.013 1346` | In [10] |
| Match rate after an earlier score of 46 or more (Asian, Neither, Other ethnic) | `(45, 200] 0.013 0.930 0.014` | In [10] |
| Nonzero scores on a multiple of 5, scores 21 to 45 (Asian, Neither, Other ethnic) | `(20, 45] 0.202 0.658 0.257` | In [11] |
| Nonzero scores on a multiple of 5, scores 46 and up (Asian, Neither, Other ethnic) | `(45, 200] 0.196 0.483 0.190` | In [11] |
| Neither: earlier score against score, itself, and previous score column | `earlier_score 0.245 1.000 0.921` | In [12] |
| Other ethnic: score against itself, earlier score, previous score column | `Other ethnic score 1.000 0.002 -0.066` | In [12] |
