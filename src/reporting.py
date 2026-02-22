from pathlib import Path
import json
import pandas as pd


def write_outputs(output_dir: Path, exceptions: pd.DataFrame):
    output_dir.mkdir(parents=True, exist_ok=True)

    exceptions_path = output_dir / "exceptions.csv"
    summary_path = output_dir / "summary.json"
    report_path = output_dir / "assurance_report.md"

    # Always write locally (even if ignored by git)
    exceptions.to_csv(exceptions_path, index=False)

    summary = {
        "total_exceptions": int(len(exceptions)),
        "by_control": exceptions["control_id"].value_counts().to_dict() if len(exceptions) else {},
        "by_risk_rating": exceptions["risk_rating"].value_counts().to_dict() if len(exceptions) else {},
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    report_md = build_markdown_report(exceptions, summary)
    report_path.write_text(report_md, encoding="utf-8")


def build_markdown_report(exceptions: pd.DataFrame, summary: dict) -> str:
    lines = []
    lines.append("# RiskGuard – Assurance Analytics Report\n")
    lines.append("## Objective\n")
    lines.append(
        "Perform repeatable, data-driven control testing to support 2LOD assurance reviews by identifying exceptions, "
        "summarising results, and generating evidence-based recommendations.\n"
    )

    lines.append("## Summary\n")
    lines.append(f"- Total exceptions identified: **{summary['total_exceptions']}**")
    lines.append(f"- Exceptions by control: `{summary.get('by_control', {})}`")
    lines.append(f"- Exceptions by risk rating: `{summary.get('by_risk_rating', {})}`\n")

    lines.append("## Controls Tested\n")
    lines.append("- **C01:** High value transactions require at least 2 approvals")
    lines.append("- **C02:** Segregation of duties (maker cannot approve own transaction)\n")

    lines.append("## Exceptions Register (Top 20)\n")
    if len(exceptions) == 0:
        lines.append("_No exceptions detected._\n")
    else:
        cols = [c for c in ["control_id", "risk_rating", "txn_id", "txn_ts", "account_id", "counterparty", "amount", "exception_reason"] if c in exceptions.columns]
        top = exceptions[cols].head(20).copy()
        lines.append(top.to_markdown(index=False))
        lines.append("")

    lines.append("## Recommendations (Actionable)\n")
    lines.append("1. Confirm **control design**: validate high-value approval thresholds and required approval levels.")
    lines.append("2. Improve **operating effectiveness**: implement preventive checks to block maker self-approval.")
    lines.append("3. Enhance **monitoring**: create periodic exception dashboards and trend exception rates by business unit.")
    lines.append("4. Strengthen **traceability**: ensure approvals retain full audit trail metadata (who/when/level/decision).\n")

    lines.append("## Notes\n")
    lines.append("- This prototype uses **synthetic data** to demonstrate assurance-style analytics and reporting.\n")

    return "\n".join(lines)