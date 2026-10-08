"""Synthetic demo: 1-D cutting stock (beams/profiles) with offcut reuse.

All data is randomly generated. It is NOT real client data and the numbers
say nothing about any real company. The point it proves: a simple solver
(first-fit decreasing) plus reusing earlier offcuts cuts waste versus a
naive "cut in drawing order" baseline, and the gap is measurable per job.
"""
import random
import statistics as st

STOCK = 12.0      # metres, standard bar length
KERF = 0.003      # metres lost per cut
MIN_REMNANT = 1.0 # offcuts shorter than this count as scrap


def naive(parts, stock_pool):
    """Cut in drawing order; open a new full bar when the part doesn't fit."""
    bars, left = [], None
    used_new = 0
    for p in parts:
        if left is not None and left >= p + KERF:
            left -= p + KERF
        else:
            if left is not None and left >= MIN_REMNANT:
                bars.append(left)
            left = STOCK - p - KERF
            used_new += 1
    if left is not None and left >= MIN_REMNANT:
        bars.append(left)
    return used_new, bars, [] 


def ffd(parts, stock_pool):
    """First-fit decreasing, optionally filling from existing offcuts first."""
    open_bars = sorted(stock_pool)         # reuse offcuts, smallest first
    reused_from = len(open_bars)
    used_new = 0
    for p in sorted(parts, reverse=True):
        for i, r in enumerate(open_bars):
            if r >= p + KERF:
                open_bars[i] = r - p - KERF
                break
        else:
            open_bars.append(STOCK - p - KERF)
            used_new += 1
    leftovers = [r for r in open_bars if r >= MIN_REMNANT]
    return used_new, leftovers, reused_from


def job(rng):
    n = rng.randint(30, 80)
    return [round(rng.uniform(0.6, 6.0), 2) for _ in range(n)]


def run(n_jobs=200, seed=7):
    """Same synthetic parts for every method. Methods that do not keep an
    offcut inventory throw leftovers away (they are scrap); the reuse method
    carries offcuts to the next job. Steel bought is what the client pays for."""
    rng = random.Random(seed)
    bought = {"naive": 0, "ffd": 0, "ffd+reuse": 0}
    per_job = {"naive": [], "ffd": [], "ffd+reuse": []}
    total_parts, pool = 0.0, []
    for _ in range(n_jobs):
        parts = job(rng)
        total_parts += sum(parts)
        for name, fn, p in (("naive", naive, []), ("ffd", ffd, []),
                            ("ffd+reuse", ffd, pool)):
            u, left, _ = fn(parts, p)
            bought[name] += u
            per_job[name].append(u)
            if name == "ffd+reuse":
                new_pool = left[-40:]
        pool = new_pool
    end_inventory = sum(pool)
    return total_parts, bought, per_job, end_inventory


if __name__ == "__main__":
    parts_len, bought, per_job, inv = run()
    print(f"{'method':<12}{'bars bought':>12}{'waste %':>10}{'gain vs naive (pts)':>22}")
    base_waste = None
    for k, nbars in bought.items():
        credit = inv if k == "ffd+reuse" else 0.0   # unused offcuts still on the shelf
        waste = 100 * (nbars * STOCK - parts_len - credit) / (nbars * STOCK)
        base_waste = waste if base_waste is None else base_waste
        print(f"{k:<12}{nbars:>12}{waste:>10.2f}{base_waste - waste:>22.2f}")
    wins = sum(1 for a, b in zip(per_job["naive"], per_job["ffd+reuse"]) if b < a)
    ties = sum(1 for a, b in zip(per_job["naive"], per_job["ffd+reuse"]) if b == a)
    print(f"\nffd+reuse bought fewer bars on {wins}/200 jobs, same on {ties} (paired, same parts)")
