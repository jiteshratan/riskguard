from pathlib import Path
import json
import pandas as pd


def write_outputs(output_dir: Path, exceptions: pd.DataFrame):
    output_dir.mkdir(parents=True, exist_ok=True)

    exceptions_path = output_dir / "exceptions.csv"
    summary_path = output_dir / "summary.json"

    exceptions.to_csv(exceptions_path, index=False)

    summary = {
        "total_exceptions": int(len(exceptions)),
        "by_control": exceptions["control_id"].value_counts().to_dict() if len(exceptions) else {},
        "by_risk_rating": exceptions["risk_rating"].value_counts().to_dict() if len(exceptions) else {},
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")