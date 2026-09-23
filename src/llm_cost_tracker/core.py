from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Iterable

MICRO = Decimal("0.000001")

@dataclass(frozen=True)
class Price:
    input_per_million: Decimal
    output_per_million: Decimal

@dataclass(frozen=True)
class Usage:
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: Decimal
    timestamp: str
    label: str = ""

DEFAULT_PRICES: dict[str, Price] = {
    # Illustrative defaults only; provider pricing changes. Override for billing decisions.
    "example-small": Price(Decimal("0.25"), Decimal("1.00")),
    "example-medium": Price(Decimal("2.00"), Decimal("8.00")),
    "example-large": Price(Decimal("10.00"), Decimal("30.00")),
}

def parse_money(value: str | int | float | Decimal) -> Decimal:
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("invalid decimal value") from exc
    if not result.is_finite() or result < 0:
        raise ValueError("value must be a finite non-negative number")
    return result

def validate_tokens(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("token counts must be non-negative integers")
    return value

def estimate_cost(input_tokens: int, output_tokens: int, price: Price) -> Decimal:
    validate_tokens(input_tokens); validate_tokens(output_tokens)
    if price.input_per_million < 0 or price.output_per_million < 0:
        raise ValueError("prices must be non-negative")
    total = (Decimal(input_tokens) * price.input_per_million + Decimal(output_tokens) * price.output_per_million) / Decimal(1_000_000)
    return total.quantize(MICRO, rounding=ROUND_HALF_UP)

def make_usage(model: str, input_tokens: int, output_tokens: int, price: Price, label: str = "", timestamp: str | None = None) -> Usage:
    model = model.strip()
    if not model:
        raise ValueError("model is required")
    ts = timestamp or datetime.now(timezone.utc).isoformat()
    try:
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("timestamp must be ISO-8601") from exc
    return Usage(model, validate_tokens(input_tokens), validate_tokens(output_tokens), estimate_cost(input_tokens, output_tokens, price), ts, label.strip())

def append_usage(path: str | Path, usage: Usage) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    row = asdict(usage); row["cost_usd"] = str(usage.cost_usd)
    with target.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

def load_usage(path: str | Path) -> list[Usage]:
    target = Path(path)
    if not target.exists():
        return []
    rows: list[Usage] = []
    with target.open(encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            if not line.strip(): continue
            try:
                row = json.loads(line)
                rows.append(Usage(str(row["model"]), int(row["input_tokens"]), int(row["output_tokens"]), parse_money(row["cost_usd"]), str(row["timestamp"]), str(row.get("label", ""))))
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                raise ValueError(f"invalid ledger row {line_no}: {exc}") from exc
    return rows

def summarize(rows: Iterable[Usage]) -> dict[str, object]:
    items = list(rows)
    by_model: dict[str, dict[str, object]] = {}
    for row in items:
        bucket = by_model.setdefault(row.model, {"requests": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": Decimal("0")})
        bucket["requests"] += 1; bucket["input_tokens"] += row.input_tokens; bucket["output_tokens"] += row.output_tokens; bucket["cost_usd"] += row.cost_usd
    total = sum((r.cost_usd for r in items), Decimal("0"))
    return {"requests": len(items), "input_tokens": sum(r.input_tokens for r in items), "output_tokens": sum(r.output_tokens for r in items), "cost_usd": total.quantize(MICRO), "by_model": by_model}

def budget_status(spend: Decimal, budget: Decimal) -> dict[str, object]:
    spend, budget = parse_money(spend), parse_money(budget)
    remaining = max(Decimal("0"), budget - spend)
    percent = Decimal("0") if budget == 0 and spend == 0 else (Decimal("100") if budget == 0 else spend / budget * 100)
    return {"spend": spend, "budget": budget, "remaining": remaining, "percent": percent.quantize(Decimal("0.01")), "exceeded": spend > budget}
