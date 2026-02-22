import pandas as pd


def test_high_value_two_approvals(txns: pd.DataFrame, approvals: pd.DataFrame, threshold: float) -> pd.DataFrame:
    appr_count = approvals.groupby("txn_id")["approval_id"].nunique().reset_index(name="approval_count")
    merged = txns.merge(appr_count, on="txn_id", how="left").fillna({"approval_count": 0})

    high_value = merged[merged["amount"] >= threshold].copy()
    exceptions = high_value[high_value["approval_count"] < 2].copy()
    exceptions["exception_reason"] = "High value txn has < 2 approvals"
    return exceptions


def test_segregation_of_duties(txns: pd.DataFrame, approvals: pd.DataFrame) -> pd.DataFrame:
    merged = approvals.merge(txns[["txn_id", "created_by"]], on="txn_id", how="left")
    exceptions = merged[merged["approved_by"] == merged["created_by"]].copy()
    exceptions["exception_reason"] = "Maker approved own transaction"

    # Join back to txn context for reporting
    exceptions = exceptions.merge(txns, on="txn_id", how="left")
    return exceptions

def test_approval_timeliness(txns: pd.DataFrame, approvals: pd.DataFrame, sla_hours: int) -> pd.DataFrame:
    # earliest approval timestamp per txn as proxy for "time to first approval"
    first_appr = approvals.groupby("txn_id")["approval_ts"].min().reset_index(name="first_approval_ts")
    merged = txns.merge(first_appr, on="txn_id", how="left")

    merged["hours_to_first_approval"] = (merged["first_approval_ts"] - merged["txn_ts"]).dt.total_seconds() / 3600.0

    exceptions = merged[
        merged["first_approval_ts"].notna() & (merged["hours_to_first_approval"] > sla_hours)
    ].copy()
    exceptions["exception_reason"] = f"First approval exceeded SLA ({sla_hours}h)"
    return exceptions


def test_duplicate_payments(txns: pd.DataFrame, window_minutes: int) -> pd.DataFrame:
    # heuristic: same account_id + counterparty + amount within N minutes
    df = txns.sort_values("txn_ts").copy()
    df["dup_key"] = (
        df["account_id"].astype(str) + "|" + df["counterparty"].astype(str) + "|" + df["amount"].astype(str)
    )

    df["prev_txn_ts"] = df.groupby("dup_key")["txn_ts"].shift(1)
    df["mins_since_prev"] = (df["txn_ts"] - df["prev_txn_ts"]).dt.total_seconds() / 60.0

    exceptions = df[df["mins_since_prev"].notna() & (df["mins_since_prev"] <= window_minutes)].copy()
    exceptions["exception_reason"] = f"Potential duplicate within {window_minutes} minutes"
    return exceptions