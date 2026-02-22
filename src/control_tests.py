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