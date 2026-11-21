# Contributing

Submissions arrive as pull requests; a maintainer appends accepted records to the ledger.

Rules:

- **Pre-register first.** A record whose pre-registration is not older than its validation run is rejected.
- **Count every trial.** `n_trials` is the full number of variants tried, including discarded ones.
- **Failures are welcome.** A rejected strategy is a useful record.
- **No market data in the repository.** Publish a data manifest with a content hash instead.
- **No investment advice.** Do not describe an entry as a recommendation.
- English only.
- **Make it importable (optional):** add `strategies/<id>/strategy.py` (a licence line at the top) with
  `signal(df) -> positions per bar` for `monte-neo verify` and, for spot long-only strategies,
  `target_weights(closes_by_symbol) -> {symbol: share of capital}` for `monte-neo deploy`. Put its SHA-256 in the spec's
  `code` section and the `data`, `try` and `deploy` sections (see `specs/MN-TSM-CRY-002.spec.json`). The maintainer
  records the code's hash on the ledger; `tools/build_index.py` then lists it in `index.json`.

The record schema is a draft (`schema/strategy-evaluation-1.draft.json`); it may change before the first release.
