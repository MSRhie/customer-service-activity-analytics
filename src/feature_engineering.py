import pandas as pd

def add_call_flags(df: pd.DataFrame) -> pd.DataFrame:
    """전화받기/걸기 여부 플래그를 추가합니다."""
    df = df.copy()
    df["전화받기_flag"] = (df["APPNM"] == "전화받기").astype(int)
    df["전화걸기_flag"] = (df["APPNM"] == "전화걸기").astype(int)
    df["전화걸고받기_flag"] = ((df["전화받기_flag"] | df["전화걸기_flag"])).astype(int)
    return df

def generate_case_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    database_id, 날짜, sequence 를 조합해 case_id를 만듭니다.
    shift + cumsum 을 이용해 loop 없이 구현합니다.
    """
    df = df.sort_values(["database_id", "LDATE"])
    df["grp"] = df.groupby("database_id")["전화걸고받기_flag"].cumsum()
    df["case_id"] = (
        df["database_id"]
        + "_"
        + df["LDATE"].dt.date.astype(str)
        + "_"
        + df["grp"].astype(str)
    )
    return df