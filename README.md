# Seattle food safety: the strongest predictor was a label the file contradicts

My take home assessment for the Stanford RegLab predoctoral Research Fellow
application, submitted on 30 September 2026. The task: predict which Seattle
restaurant inspections find a serious food safety violation, using only what is
known before the inspection, add flags for Asian and ethnic cuisines, and say
whether a health department should use the result.

[`tanay_singh_reglab_takehome.ipynb`](tanay_singh_reglab_takehome.ipynb) is the
notebook I submitted, unchanged, with every output from its one run saved.
Every number below was printed by a cell of that notebook.
[RESULTS.md](RESULTS.md) maps each one to its cell, and
`scripts/check_results.py` checks that mapping in CI.

## In one paragraph

Adding the cuisine flags appears to give the best model in the file. It does
not hold up. For Asian and Other ethnic restaurants, the file's own "previous
score" column agrees with the earlier score it records in 1.3% of back to back
inspections, against 95.1% for every other restaurant, and their scores do not
persist from one inspection to the next. Those rows behave like random numbers
centered near 60, so most of the headline test AUC of 0.886 comes from a label
problem. On the restaurants whose records look sound, the best model reaches an
AUC of 0.657, against 0.639 for ranking by the last inspection score.
Inspection history does almost all the work, Yelp adds nothing, and the model
as trained would send every priority inspection to Asian and Other ethnic
restaurants.

## The data

13,299 inspections of 1,756 restaurants, January 2006 to February 2013. Each
row is one inspection: its penalty score, the previous score, an average of
earlier scores, the Yelp reviews posted since the last inspection, the zip code
and the restaurant's Yelp cuisine labels. An inspection is serious if it scores
10 or more. Two rows carry a -1 placeholder and are dropped, leaving 13,297.

- **The cutoff sits low.** 67.4% of inspections are serious and 21.7% score
  exactly 0, so "serious" separates the cleanest third from everyone else.
  Always guessing serious is already 67.6% accurate on the test years, so I
  report AUC and precision among the riskiest 20% instead of accuracy.
- **Scores stick to restaurants.** The correlation with the previous score is
  0.707, and which restaurant it is explains 75.1% of the variance in scores.
  After a clean previous inspection 30.8% of inspections are serious; after a
  previous score of 50 or more, 97.4% are. So the evaluation splits by time and
  resamples whole restaurants.
- **Yelp barely moves.** The score's correlations with review count,
  non positive reviews and rating are all between -0.040 and 0. This matches
  Altenburger and Ho (2019), who found that Yelp adds little to the Seattle
  data behind Kang et al. (2013) once inspection history is known.
