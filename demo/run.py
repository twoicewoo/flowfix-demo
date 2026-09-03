#!/usr/bin/env python3
"""Deterministic, dependency-free FlowFix synthetic order validation demo."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

FIELDS = ["order_id", "customer", "amount_cny", "paid_at", "status", "invoice_required"]
STATUSES = {"paid", "refunded", "pending"}
BOOLEANS = {"yes", "no"}


def validate(row: dict[str, str], seen: set[str]) -> list[str]:
    errors: list[str] = []
    missing = [field for field in FIELDS if not row.get(field, "").strip()]
    if missing:
        errors.append("missing:" + ",".join(missing))

    order_id = row.get("order_id", "").strip()
    if order_id in seen:
        errors.append("duplicate_order_id")
    elif order_id:
        seen.add(order_id)

    try:
        if Decimal(row.get("amount_cny", "0")) <= 0:
            errors.append("amount_must_be_positive")
    except InvalidOperation:
        errors.append("amount_not_numeric")

    try:
        date.fromisoformat(row.get("paid_at", ""))
    except ValueError:
        errors.append("invalid_date")

    if row.get("status") not in STATUSES:
        errors.append("invalid_status")
    if row.get("invoice_required") not in BOOLEANS:
        errors.append("invalid_invoice_flag")
    return errors


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run(input_path: Path, output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    with input_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise SystemExit(f"expected fields {FIELDS}, got {reader.fieldnames}")
        rows = list(reader)

    valid: list[dict[str, str]] = []
    review: list[dict[str, str]] = []
    seen: set[str] = set()
    for source in rows:
        row = {field: source.get(field, "").strip() for field in FIELDS}
        errors = validate(row, seen)
        if errors:
            review.append({**row, "review_reason": ";".join(errors)})
        else:
            row["amount_cny"] = f"{Decimal(row['amount_cny']):.2f}"
            valid.append(row)

    gross = sum(Decimal(row["amount_cny"]) for row in valid if row["status"] == "paid")
    refunds = sum(Decimal(row["amount_cny"]) for row in valid if row["status"] == "refunded")
    net = gross - refunds
    summary: dict[str, object] = {
        "input_rows": len(rows),
        "valid_rows": len(valid),
        "review_rows": len(review),
        "gross_cny": f"{gross:.2f}",
        "refunds_cny": f"{refunds:.2f}",
        "net_cny": f"{net:.2f}",
        "data_notice": "synthetic_demo_not_business_revenue",
    }

    write_csv(output_dir / "valid_orders.csv", FIELDS, valid)
    write_csv(output_dir / "review_queue.csv", FIELDS + ["review_reason"], review)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "management_report.md").write_text(
        "# 合成订单校验报告\n\n"
        "> 本报告由虚构演示数据生成，不代表真实客户、订单或收入。\n\n"
        f"- 输入行数：{len(rows)}\n"
        f"- 通过校验：{len(valid)}\n"
        f"- 待人工复核：{len(review)}\n"
        f"- 已付款总额：¥{gross:.2f}\n"
        f"- 已退款总额：¥{refunds:.2f}\n"
        f"- 演示净额：¥{net:.2f}\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    summary = run(args.input, args.output)
    print(
        "FLOWFIX_DEMO_OK "
        + " ".join(f"{key}={summary[key]}" for key in (
            "input_rows", "valid_rows", "review_rows", "gross_cny", "refunds_cny", "net_cny"
        ))
    )


if __name__ == "__main__":
    main()

