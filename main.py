from pathlib import Path
import pandas as pd

from src.config import load_config
from src.data_loader import load_all
from src.control_tests import (
    test_high_value_two_approvals,
    test_segregation_of_duties,
    test_approval_timeliness,
    test_duplicate_payments,
)
from src.scoring import add_risk_score
from src.reporting import write_outputs


def run():
    project_root = Path(__file__).resolve().parent
    cfg = load_config(project_root)
    txns, approvals, users = load_all(cfg.data_dir)

    enabled = {c["id"]: c for c in cfg.controls if c.get("enabled", True)}
    exceptions_all = []

    if "C01" in enabled:
        e = test_high_value_two_approvals(txns, approvals, float(cfg.thresholds["high_value_amount"]))
        e["control_id"] = "C01"
        e["control_name"] = enabled["C01"]["name"]
        exceptions_all.append(e)

    if "C02" in enabled:
        e = test_segregation_of_duties(txns, approvals)
        e["control_id"] = "C02"
        e["control_name"] = enabled["C02"]["name"]
        exceptions_all.append(e)

    if "C03" in enabled:
        e = test_approval_timeliness(txns, approvals, int(cfg.thresholds["approval_sla_hours"]))
        e["control_id"] = "C03"
        e["control_name"] = enabled["C03"]["name"]
        exceptions_all.append(e)

    if "C04" in enabled:
        e = test_duplicate_payments(txns, int(cfg.thresholds["duplicate_window_minutes"]))
        e["control_id"] = "C04"
        e["control_name"] = enabled["C04"]["name"]
        exceptions_all.append(e)

    exceptions = pd.concat(exceptions_all, ignore_index=True, sort=False) if exceptions_all else pd.DataFrame()

    if len(exceptions):
        exceptions = add_risk_score(exceptions, cfg.risk_scoring)

    write_outputs(cfg.output_dir, exceptions)
    print("Done. Outputs written to ./output")


if __name__ == "__main__":
    run()