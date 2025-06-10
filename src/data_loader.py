from pathlib import Path
import pandas as pd
from typing import List

def load_consultation_data(ids: List[str], raw_dir: Path) -> pd.DataFrame:
    """여러 CSV 파일을 읽어와 하나의 DataFrame으로 합칩니다."""
    dfs = []
    for db_id in ids:
        path = raw_dir / f"{db_id}.csv"
        df = pd.read_csv(path, encoding="utf-8")
        df["database_id"] = db_id
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def load_call_records(ids: List[str], raw_dir: Path) -> pd.DataFrame:
    """XLS 파일을 읽어와 '음성녹음시작시간' 등을 전처리합니다."""
    dfs = []
    for db_id in ids:
        path = raw_dir / f"{db_id}.xls"
        df = pd.read_excel(path, skiprows=2)
        df.columns = df.iloc[0]
        df = df.iloc[1:].reset_index(drop=True)
        df["database_id"] = db_id
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)