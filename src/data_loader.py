from pathlib import Path
import pandas as pd


def load_csv(path: Path, parse_dates=None) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=parse_dates)


def load_all(data_dir: Path):
    txns = load_csv(data_dir / "transactions.csv", parse_dates=["txn_ts"])
    approvals = load_csv(data_dir / "approvals.csv", parse_dates=["approval_ts"])
    users = load_csv(data_dir / "users.csv")
    return txns, approvals, users