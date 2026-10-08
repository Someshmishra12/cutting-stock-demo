# Cutting-stock demo (synthetic data)

A small, self-contained demo of how to **benchmark** a cutting-stock solver
against a baseline, using paired comparisons on identical randomly generated jobs.

**All data is synthetic. It is not real company data, and the numbers say
nothing about any real business.**

## Run
```
python3 cutting_stock_demo.py
```
No dependencies (Python 3 standard library only). Seed is fixed, so results repeat.

## What it compares (200 jobs, 12 m bars, 3 mm kerf, 30-80 parts per job)
| Method | Idea |
|---|---|
| `naive` | Cut parts in the order given; start a new bar when the next part doesn't fit; leftovers are discarded |
| `ffd` | First-fit decreasing |
| `ffd+reuse` | First-fit decreasing, filling from an inventory of offcuts carried over from earlier jobs |

## Result (see `results.txt`)
| Method | Bars bought | Waste % |
|---|---|---|
| naive | 3667 | 17.97 |
| ffd | 3144 | 4.32 |
| ffd+reuse | 3055 | 1.51 |

`ffd+reuse` bought fewer bars than `naive` on 200 of 200 jobs.

## What this does and does not show
- **Shows:** the evaluation method: same inputs for every method, a paired
  per-job comparison, and waste defined as steel bought minus parts cut minus
  offcuts still usable.
- **Does not show:** how much a real operation would save. The `naive` baseline
  is deliberately weak. A skilled planner nesting by hand would beat it by a
  wide margin, so the real test is against actual historical nests, with the
  planners' own rules and constraints.
- Offcut reuse here ignores material grade, certificates, cost allocation
  between projects and physical location, which matter in practice.
