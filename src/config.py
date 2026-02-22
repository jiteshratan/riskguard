from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass(frozen=True)
class AppConfig:
    data_dir: Path
    output_dir: Path
    thresholds: dict
    risk_scoring: dict
    controls: list


def load_config(project_root: Path) -> AppConfig:
    controls_path = project_root / "control_rules" / "controls.yaml"
    with open(controls_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    return AppConfig(
        data_dir=project_root / "data" / "raw",
        output_dir=project_root / "output",
        thresholds=cfg.get("thresholds", {}),
        risk_scoring=cfg.get("risk_scoring", {}),
        controls=cfg.get("controls", []),
    )