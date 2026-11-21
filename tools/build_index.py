"""Build index.json: one entry per record, with the files Monte-Neo downloads and their SHA-256.

    python3 tools/build_index.py          # write index.json
    python3 tools/build_index.py --check  # exit 1 when index.json is out of date (CI)

`monte-neo registry list | show | import | try` reads this file. Every file it lists is also checked against the
ledger: the record's SHA-256 must appear in a ledger record, so an imported strategy is the one that was evaluated.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build() -> dict:
    ledger = [json.loads(x) for x in (ROOT / "ledger" / "ledger.jsonl").read_text().splitlines() if x.strip()]
    status = {}
    for e in ledger:
        if e["type"] == "record":
            for s in e["body"]["sources"]:
                status[s["sha256"]] = e["body"]["status"]
    entries = []
    for rp in sorted((ROOT / "records").glob("*.json")):
        rec = json.loads(rp.read_text())
        cid = rec["catalog_id"]
        sp = ROOT / "specs" / f"{cid}.spec.json"
        spec = json.loads(sp.read_text()) if sp.exists() else {}
        code = spec.get("code") or None
        files = {"record": {"path": f"records/{cid}.json", "sha256": sha(rp)}}
        if sp.exists():
            files["spec"] = {"path": f"specs/{cid}.spec.json", "sha256": sha(sp)}
        if code:
            files["code"] = {"path": code["path"], "sha256": sha(ROOT / code["path"])}
        ev = rec["evaluation"]
        entries.append({
            "id": cid, "name": spec.get("name", cid), "asset_class": rec["taxonomy"].get("asset_class"),
            "signal": rec["taxonomy"].get("signal"), "verdict": ev["verdict"], "arl": ev.get("arl_level"),
            "gate_passed": (ev.get("gate") or {}).get("passed"), "ledger_status": status.get(sha(rp)),
            "summary": rec.get("outcome_summary", ""), "files": files,
            "importable": bool(code), "interfaces": (code or {}).get("interfaces", []),
            "data": spec.get("data"), "try": spec.get("try"),
            "deploy": spec.get("deploy") or {"binance_spot_testnet": False, "why": "no public code in this record"},
        })
    return {"schema": "registry-index/1", "repository": "https://github.com/Protocolith/trading-strategy-registry",
            "raw_base": "https://raw.githubusercontent.com/Protocolith/trading-strategy-registry/main/",
            "ledger_head": ledger[-1]["hash"] if ledger else None, "records": entries}


def main() -> int:
    text = json.dumps(build(), indent=1, sort_keys=True) + "\n"
    path = ROOT / "index.json"
    if "--check" in sys.argv:
        ok = path.exists() and path.read_text() == text
        print("index.json is up to date" if ok else "index.json is out of date: run python3 tools/build_index.py")
        return 0 if ok else 1
    path.write_text(text)
    print(f"wrote index.json ({len(json.loads(text)['records'])} records)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
