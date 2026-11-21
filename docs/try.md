# Try a registry strategy yourself

This page takes you from nothing to a running demo forward record of a public strategy. Every command is copy-paste.
**Not investment advice:** the records are research examples, many of them failed on purpose of being honest.

## 1. Install Monte-Neo

```bash
pip install monte-neo            # or: pipx install monte-neo   (Python 3.11 or newer)
monte-neo --version
```

## 2. Find a strategy

```bash
monte-neo registry list                 # all records
monte-neo registry list --deployable    # only those that can run on the Binance spot demo testnet
monte-neo registry show MN-TSM-CRY-002  # rules, verdict, ARL, the gate and why it passed or failed
```

A record is **importable** when its author published code in `strategies/<id>/strategy.py`; records without code show
their rules and evaluation only (some strategies are proprietary: only their protocol hashes and results are public).

## 3. Import it, with proof that it is the evaluated code

```bash
monte-neo registry import MN-TSM-CRY-002     # writes ./strategies/MN-TSM-CRY-002/
```

Monte-Neo downloads the record, the specification and the code, and refuses the import if any file's SHA-256 differs
from `index.json`, or if the record and the code are not referenced by a record entry of the Protocolith ledger
(`ledger/ledger.jsonl`). `provenance.json` in the folder lists what was checked.

## 4. Re-run the verification on public data

```bash
monte-neo registry try MN-TSM-CRY-002
```

This downloads the public daily bars (Binance spot), runs `monte-neo verify` with the record's number of trials and
cost model, writes `certificate.json`, and prints the registry's numbers next to yours. Small differences can come from
a newer Monte-Neo version or revised exchange data; the verdict should agree.

## 5. Run it as a demo forward record

```bash
monte-neo deploy init --strategy strategies/MN-TSM-CRY-002/strategy.py \
  --certificate strategies/MN-TSM-CRY-002/certificate.json --symbols BTCUSDT --rebalance daily --mode dry
monte-neo deploy run          # records every day up to today; run it daily (or use scripts/deploy_loop.sh)
monte-neo deploy serve        # dashboard on http://127.0.0.1:8787/
```

`--mode dry` simulates orders. For the Binance spot demo testnet, create keys at https://testnet.binance.vision,
store them with `monte-neo deploy keys`, and use `--mode testnet`. Real money is not supported.

## 6. What the numbers mean

- **Verdict** and **ARL** come from Monte-Neo: how much evidence the backtest carries, not how much it will earn.
- **Gate**: the criterion written before the decisive test (a sealed holdout or a forward period). A failed gate is
  published like a passed one.
- **Ledger status**: `PASSED_UNDER_PROTOCOL` or `NEGATIVE_RESULT_UNDER_PROTOCOL`, fixed on a hash-chained ledger.

## 7. Add your own strategy

Open a pull request with `specs/<id>.spec.json`, `records/<id>.json` and, to make it importable,
`strategies/<id>/strategy.py` with `signal(df)` and, for deployment, `target_weights(closes_by_symbol)`. See
[CONTRIBUTING.md](../CONTRIBUTING.md).

If this helped you, please star [Monte-Neo](https://github.com/NeoZorK/Monte-Neo) on GitHub.
