# Trading Strategy Registry

Reproducible, pre-registered evaluations of trading strategies, recorded on a tamper-evident
[Protocolith](https://github.com/Protocolith/protocolith) ledger. Every entry holds a verdict and an
**ARL (Alpha Readiness Level)** from the open-source verifier
[Monte-Neo](https://github.com/NeoZorK/Monte-Neo). Failed strategies are recorded too.

> **Not investment advice. No trading signals.** An entry says how much evidence a backtest
> carries under a stated protocol, not that a strategy will make money.

**Status:** under construction. The record schema is a draft; the first records follow the
Monte-Neo v0.55 release.

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
