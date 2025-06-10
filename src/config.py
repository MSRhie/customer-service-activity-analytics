import yaml
from pathlib import Path
from typing import List

class Config:
    def __init__(self, path: str):
        cfg = yaml.safe_load(Path(path).read_text())
        self.raw_path: Path = Path(cfg["data_path"]["raw"])
        self.processed_path: Path = Path(cfg["data_path"]["processed"])
        self.database_ids: List[str] = cfg["database_ids"]

# 사용 예
# cfg = Config("configs/config.yaml")