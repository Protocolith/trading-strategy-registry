# Trading Strategy Registry

Reproducible, pre-registered evaluations of trading strategies, recorded on a tamper-evident
[Protocolith](https://github.com/Protocolith/protocolith) ledger. Every entry holds a verdict and an
**ARL (Alpha Readiness Level)** from the open-source verifier
[Monte-Neo](https://github.com/NeoZorK/Monte-Neo). Failed strategies are recorded too.

> **Not investment advice. No trading signals.** An entry says how much evidence a backtest
> carries under a stated protocol, not that a strategy will make money.

**Status:** under construction. The record schema is a draft.

## Try a strategy yourself in five minutes

Records with public code can be imported into [Monte-Neo](https://github.com/NeoZorK/Monte-Neo), re-verified on
public data on your machine, and run as a forward record on the Binance spot demo testnet:

```bash
pip install monte-neo                       # Python 3.11+
monte-neo registry list                     # what is in the registry
monte-neo registry show MN-TSM-CRY-002      # the evaluation and why it passed or failed
monte-neo registry try MN-TSM-CRY-002       # download, check every hash against the ledger, re-run the verification
monte-neo deploy init --strategy strategies/MN-TSM-CRY-002/strategy.py \
  --certificate strategies/MN-TSM-CRY-002/certificate.json --symbols BTCUSDT --rebalance daily --mode dry
monte-neo deploy run                        # a dry forward record with a dashboard: monte-neo deploy serve
```

Every imported file is checked against `index.json` and against this ledger, so what you run is exactly what was
evaluated. Step by step: [docs/try.md](docs/try.md).

If this is useful, a star on [Monte-Neo](https://github.com/NeoZorK/Monte-Neo) and on this repository helps others find it.

## Records

| Id | Strategy | Verdict (full period) | Pre-registered gate | Result |
|---|---|---|---|---|
| [MN-TSM-CRY-001](records/MN-TSM-CRY-001.json) | Donchian channel basket, 18 crypto spot pairs | PASS_WITH_WARNINGS, ARL 5 | holdout 2025-01..2026-10, net Sharpe at 2x costs > 0 | **failed** (Sharpe -0.06 at 2x costs) |
| [MN-ALC-MLT-001](records/MN-ALC-MLT-001.json) | Multi-asset ETF book: trend, risk parity, bond trend-carry | NEEDS_MORE_EVIDENCE (returns only) | holdout 2021-01..2026-11, net Sharpe at 2x costs >= 0.30, max DD >= -20 % | **passed** (Sharpe 0.70 at 2x costs, max DD -4.1 %, 2.4 % a year) |

## Strategy Lab results under Monte-Neo v0.57.0 (55 records)

Every public strategy of the Monte-Neo Strategy Lab (code in `examples/strategies/` of Monte-Neo, tag `v0.57.0`) re-validated
with Monte-Neo 0.57.0 under `arl-rules/2`, with the lab-wide trial count (`n_trials` = 164). Validation window only
(2021-01..2024-12); the sealed holdout (2025-01 on) was **not** opened for any of them. Each record is frozen and recorded on the
ledger with the hashes of its spec, record, public code and data manifest.

- Verdicts: NEEDS_MORE_EVIDENCE 36, REJECT 14, PASS_WITH_WARNINGS 5.
- ARL: level 1: 3, level 2: 14, level 3: 38. No strategy reaches level 4: after paying for 164 trials no
  signal is significant (`timing_significance`, `selection_adjusted_sharpe`).
- Lab validation gate (not REJECT and positive net Sharpe also at doubled costs): 29 passed, 26 failed. A passed gate
  is not a holdout result and not evidence of a tradable edge.

The records are in `records/` (ids `MN-<category>-CRY-NNN`), the list with ledger status in `index.json`. The code is not copied
here: each spec's `public_code` names the Monte-Neo file and its SHA-256 at `v0.57.0`.

## What is stored

Not code and not market data. Each entry is a **reproducible experiment**:

| Part | Content |
|---|---|
| Specification | exact rules (entry, exit, sizing, rebalancing), universe, instruments, costs |
| Data manifest | data source, instruments, period, content hash (the data itself is not published) |
| Pre-registration | parameter grid, number of trials, discovery / validation / holdout split, frozen before validation is read |
| Evaluation | Monte-Neo verdict, ARL level and depth, key metrics, signed certificate id |
| Ledger record | Protocolith freeze and record, hash-chained, anchored in time |

Some entries are **result-only**: the strategy idea stays private and only the protocol hashes,
the verdict and the certificate are public.

## Layout

```
index.json   one entry per record with its files and their SHA-256 (read by `monte-neo registry`)
strategies/  public reference code of a record, when the author publishes it (licence in the file)
specs/    strategy specifications (one JSON file per catalog id, e.g. MN-TSM-FX-001.spec.json)
ledger/   Protocolith ledger (freeze and record entries)
schema/   JSON schema of an evaluation record (draft: strategy-evaluation/1)
docs/     taxonomy, ARL summary, how to submit
```

## Catalog ids

`MN-<signal>-<asset class>-<number>`, for example `MN-TSM-FX-001` (time-series momentum on FX).
Ids are never reused; a changed strategy gets a new version of its record, not a new id.

## How an entry is made

1. Write the specification and the data manifest.
2. Freeze the pre-registration on the ledger before any validation data is read.
3. Run Monte-Neo (`monte-neo verify` or `monte-neo research`) with the full number of trials.
4. Export the evaluation and append it to the ledger.
5. CI checks the ledger chain and rebuilds the catalog pages.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache-2.0 for the repository content. Each record names its own license (default CC BY 4.0).
