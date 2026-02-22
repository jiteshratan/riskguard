import pandas as pd


def add_risk_score(exceptions: pd.DataFrame, control_weights: dict) -> pd.DataFrame:
    df = exceptions.copy()
    weight_map = {
        "C01": control_weights.get("high_value_weight", 3),
        "C02": control_weights.get("sod_weight", 5),
    }
    df["risk_score"] = df["control_id"].map(weight_map).fillna(1).astype(int)

    def label(score: int) -> str:
        if score >= 5:
            return "High"
        if score >= 3:
            return "Medium"
        return "Low"

    df["risk_rating"] = df["risk_score"].apply(label)
    return df