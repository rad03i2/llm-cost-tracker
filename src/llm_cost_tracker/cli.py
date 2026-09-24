from __future__ import annotations
import argparse, json, sys
from decimal import Decimal
from pathlib import Path
from .core import DEFAULT_PRICES, Price, append_usage, budget_status, export_csv, filter_usage, load_usage, make_usage, parse_money, summarize

VERSION = "1.1.0"

def price_from_args(args) -> Price:
    if args.input_price is not None or args.output_price is not None:
        if args.input_price is None or args.output_price is None:
            raise ValueError("--input-price and --output-price must be supplied together")
        return Price(parse_money(args.input_price), parse_money(args.output_price))
    try: return DEFAULT_PRICES[args.model]
    except KeyError as exc: raise ValueError("unknown model; supply both --input-price and --output-price") from exc

def serial(value):
    if isinstance(value, Decimal): return str(value)
    if isinstance(value, dict): return {k: serial(v) for k, v in value.items()}
    return value

def add_filters(q):
    q.add_argument("--model"); q.add_argument("--label"); q.add_argument("--since", help="ISO-8601 inclusive lower bound"); q.add_argument("--until", help="ISO-8601 inclusive upper bound")

def parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(prog="llm-cost", description="Estimate and track LLM token costs locally.")
    p.add_argument("--version", action="version", version=f"llm-cost-tracker {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    sub=p.add_subparsers(dest="command", required=True)
    for name in ("estimate","record"):
        q=sub.add_parser(name); q.add_argument("--model", required=True); q.add_argument("--input-tokens", type=int, required=True); q.add_argument("--output-tokens", type=int, required=True); q.add_argument("--input-price"); q.add_argument("--output-price"); q.add_argument("--json", action="store_true")
        if name=="record": q.add_argument("--ledger", default="llm-usage.jsonl"); q.add_argument("--label", default="")
    q=sub.add_parser("summary"); q.add_argument("--ledger", default="llm-usage.jsonl"); q.add_argument("--budget"); q.add_argument("--json", action="store_true"); add_filters(q)
    q=sub.add_parser("export"); q.add_argument("--ledger", default="llm-usage.jsonl"); q.add_argument("--output", required=True); q.add_argument("--json", action="store_true"); add_filters(q)
    q=sub.add_parser("models"); q.add_argument("--json", action="store_true")
    return p

def selected_rows(args):
    return filter_usage(load_usage(args.ledger), model=args.model, label=args.label, since=args.since, until=args.until)

def main(argv=None) -> int:
    args=parser().parse_args(argv)
    try:
        if args.command in {"estimate","record"}:
            usage=make_usage(args.model,args.input_tokens,args.output_tokens,price_from_args(args),getattr(args,"label",""))
            if args.command=="record": append_usage(args.ledger,usage)
            out={"model":usage.model,"input_tokens":usage.input_tokens,"output_tokens":usage.output_tokens,"cost_usd":usage.cost_usd}
            if args.command=="record": out["ledger"]=str(Path(args.ledger))
        elif args.command=="summary":
            out=summarize(selected_rows(args))
            if args.budget is not None: out["budget"]=budget_status(out["cost_usd"],parse_money(args.budget))
        elif args.command=="export":
            count=export_csv(args.output, selected_rows(args)); out={"rows":count,"output":str(Path(args.output))}
        else:
            out={k:{"input_per_million":v.input_per_million,"output_per_million":v.output_per_million} for k,v in DEFAULT_PRICES.items()}
        if getattr(args,"json",False): print(json.dumps(serial(out),ensure_ascii=False,indent=2))
        else:
            if args.command=="models":
                for k,v in out.items(): print(f"{k}: input ${v['input_per_million']}/1M, output ${v['output_per_million']}/1M")
            elif args.command=="summary": print(f"requests={out['requests']} input={out['input_tokens']} output={out['output_tokens']} cost=${out['cost_usd']}")
            elif args.command=="export": print(f"exported {out['rows']} rows to {out['output']}")
            else: print(f"{out['model']}: {out['input_tokens']} input + {out['output_tokens']} output = ${out['cost_usd']}")
        return 0
    except (ValueError,OSError) as exc:
        print(f"error: {exc}",file=sys.stderr); return 2

if __name__ == "__main__": raise SystemExit(main())
