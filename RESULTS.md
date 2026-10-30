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
| Highest yearly serious share (a full year) | `2007 0.695` | In [6] |
| Lowest yearly serious share (a full year) | `2011 0.653` | In [6] |
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

## Models

| Quantity | Printed | Cell |
|---|---|---|
| Training years | `train 2006-01-03 to 2010-12-30 7053 rows` | In [13] |
| Tuning and calibration year | `valid 2011-01-03 to 2011-12-30 2578 rows` | In [13] |
| Test period | `test 2012-01-03 to 2013-02-08 3666 rows, 0.676 serious` | In [13] |
| Logistic regression, best 2011 AUC (C = 0.01) | `0.01: 0.878` | In [14] |
| Gradient boosting, best 2011 AUC (learning rate 0.02, 15 leaves) | `(0.02, 15): 0.873` | In [14] |
| Text model, best 2011 AUC (C = 1) | `text, by C: {0.1: 0.828, 1: 0.837` | In [14] |
| Accuracy of always guessing serious on the test years | `always guessing serious: 0.676` | In [15] |
| Neither: share of test rows, share serious | `Neither: 0.542 of test rows, 0.405 serious` | In [15] |
| Boosting gives every Asian and Other ethnic test inspection one value | `boosting test: 1 distinct value(s) for Asian/Other ethnic (0.953)` | In [15] |
| All inspections, previous score: AUC and 95% interval | `All inspections Previous score 0.870 0.856 0.884` | In [16] |
| All inspections, cuisine flag only | `Cuisine flag only 0.836 0.823 0.850` | In [16] |
| All inspections, logistic regression | `Logistic regression 0.885 0.872 0.897` | In [16] |
| All inspections, gradient boosting | `Gradient boosting 0.886 0.875 0.899` | In [16] |
| All inspections, review text | `Review text 0.845 0.829 0.860` | In [16] |
| Neither, previous score: AUC and 95% interval | `Neither only Previous score 0.639 0.613 0.662` | In [16] |
| Neither, cuisine flag only | `Cuisine flag only 0.500 0.500 0.500` | In [16] |
| Neither, logistic regression | `Logistic regression 0.651 0.626 0.677` | In [16] |
| Neither, gradient boosting | `Gradient boosting 0.657 0.631 0.684` | In [16] |
| Neither, review text | `Review text 0.576 0.549 0.603` | In [16] |
| Neither, precision in the riskiest 20%: previous score | `Neither only Previous score 0.594` | In [16] |
| Neither, precision in the riskiest 20%: cuisine flag only | `Cuisine flag only 0.418` | In [16] |
| Neither, precision in the riskiest 20%: gradient boosting | `Gradient boosting 0.617` | In [16] |
| Neither, precision in the riskiest 20%: review text | `Review text 0.489` | In [16] |
| Boosting Brier score before and after calibration, all inspections | `Gradient boosting All inspections 0.126 0.123` | In [18] |
| Boosting Brier score before and after calibration, Neither | `Neither only 0.228 0.224` | In [18] |
| Brier score of the 2011 base rate, Neither | `base rate, Neither: 0.241` | In [18] |
| Boosting on history only: 2011 AUC, test AUC, test AUC within Neither | `only history 0.875 0.894 0.685` | In [20] |
| Boosting on Yelp only | `only Yelp 0.527 0.515 0.504` | In [20] |
| Boosting without the cuisine flags | `all but cuisine flags 0.872 0.889 0.671` | In [20] |
| Asian and Other ethnic share of the riskiest 20%, all inputs | `all inputs 1.000` | In [20] |
| The same share with the cuisine flags removed | `all but cuisine flags 0.997` | In [20] |
| Words pushing the text model toward serious | `toward serious: rice, sushi, mexican, pho, chinese, teriyaki, thai` | In [21] |
| Words pushing it away | `toward not serious: pizza, subway, burger, sandwich, pie` | In [21] |

## Targeting

| Quantity | Printed | Cell |
|---|---|---|
| Riskiest 20% overall: visits and serious violations found | `riskiest 20% overall: 733 visits, 730 serious found` | In [22] |
| Asian share of those visits | `Asian: 0.701 of visits` | In [22] |
| Neither share of those visits | `Neither: 0.000 of visits` | In [22] |
| Riskiest 20% within each group: visits and serious violations found | `riskiest 20% within each group: 733 visits, 580 serious found` | In [22] |
| Neither share of visits under the per group rule | `Neither: 0.542 of visits` | In [22] |
| Score regression, mean absolute error | `mean abs error: model 12.7` | In [23] |
| Mean absolute error of predicting the last score again | `same as last time 15.9` | In [23] |
