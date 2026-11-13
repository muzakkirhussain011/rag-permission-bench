# (c) Exploratory: the registered intervals when questions are resampled too

**Exploratory. This is not the registered analysis and does not replace its verdicts.** The registered analysis (`bench.report`, pre-registration section 8) bootstraps users only. In W2 and W3 every user draws questions from one pool of 300 MS MARCO questions, so several users answer the same question, and in W1 some subjects are asked by more than one user (`workloads.md`, users per question). When recall depends on the question as well as on the user, an interval that resamples users alone can be too narrow. Here every interval of H1 to H8 is recomputed at the registered level (99.375%, 10,000 resamples) under three schemes and judged by the registered rule; a hypothesis over several parts is combined by the registered intersection-union rule.

- `users`: users resampled, questions fixed: the registered scheme, recomputed here with its own generator.
- `questions`: questions resampled as clusters (all pairs of a drawn question, over every user and job), users fixed.
- `users_x_questions`: users and questions resampled independently, each pair weighted by the product of the two draws (the pigeonhole bootstrap of Owen 2007, which tends to overstate the variance).

Every scheme uses `bench.report`'s estimator (each user's mean over their questions and jobs, then the mean over users; a failed query counts as 0). The `users` column is a check of this code: it should agree with the registered interval up to Monte Carlo error.

## Verdicts

| hypothesis | parts | registered | users (this code) | questions | users x questions | parts whose verdict differs from the registered one under a cluster scheme |
|---|---|---|---|---|---|---|
| H1 | 10 | supported | supported | supported | supported | 0 |
| H2 | 10 | supported | supported | supported | supported | 0 |
| H3 | 90 | supported | supported | supported | supported | 0 |
| H4 | - | supported | supported | supported | supported | 0 (judged on counts and medians, not on an interval, so no resampling scheme changes it) |
| H5 | 3 | supported | supported | supported | supported | 0 |
| H6 | 75 | not supported | not supported | not supported | not supported | 7 |
| H7 | 30 | supported | supported | supported | supported | 0 |
| H8 | - | supported | supported | supported | supported | 0 (judged on counts and medians, not on an interval, so no resampling scheme changes it) |

Verdict changes: none: every hypothesis keeps its registered verdict under both cluster schemes.

## Interval widths against the registered ones

| hypothesis | users scheme: largest gap to a registered endpoint | parts where the users scheme's verdict differs from the registered one | width ratio, questions: median (max) | width ratio, users x questions: median (max) |
|---|---|---|---|---|
| H1 | 0.0019 | 0 | 0.53 (0.56) | 1.22 (1.24) |
| H2 | 0.0024 | 0 | 0.57 (0.61) | 1.25 (1.28) |
| H3 | 0.0029 | 0 | 1.34 (1.63) | 2.05 (2.29) |
| H5 | 0.0007 | 0 | 1.14 (1.49) | 2.04 (2.12) |
| H6 | 0.0013 | 0 | 1.38 (2.00) | 1.99 (2.55) |
| H7 | 0.0000 | 0 | n/a (n/a) | n/a (n/a) |

A ratio is a part's interval width under the scheme over its registered width (parts with a registered width of 0 are left out).

## H6: parts whose verdict differs under some scheme

| store | layout | estimate | registered | users | questions | users x questions |
|---|---|---|---|---|---|---|
| pgvector | w3_s0p2_none | 0.876 | [0.859, 0.892] not supported | [0.860, 0.892] not supported | [0.854, 0.898] not supported | [0.840, 0.906] inconclusive |
| pgvector | w3_s0p2_pos | 0.919 | [0.908, 0.930] supported | [0.908, 0.931] supported | [0.899, 0.940] inconclusive | [0.890, 0.944] inconclusive |
| pgvector | w3_s0p5_neg | 0.880 | [0.865, 0.895] not supported | [0.864, 0.894] not supported | [0.855, 0.904] inconclusive | [0.846, 0.911] inconclusive |
| pgvector | w3_s0p5_none | 0.928 | [0.917, 0.940] supported | [0.917, 0.940] supported | [0.906, 0.948] supported | [0.899, 0.952] inconclusive |
| weaviate | w3_s0p05_none | 0.917 | [0.904, 0.928] supported | [0.905, 0.928] supported | [0.901, 0.931] supported | [0.893, 0.937] inconclusive |
| weaviate | w3_s0p2_neg | 0.883 | [0.868, 0.897] not supported | [0.868, 0.897] not supported | [0.861, 0.902] inconclusive | [0.852, 0.909] inconclusive |
| opensearch | w3_s0p2_neg | 0.878 | [0.860, 0.894] not supported | [0.860, 0.893] not supported | [0.855, 0.899] not supported | [0.844, 0.906] inconclusive |

