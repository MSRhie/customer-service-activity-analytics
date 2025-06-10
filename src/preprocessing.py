import pandas as pd
from typing import Dict

CPI_EVENT_MAPPING: Dict[str,str] = {
    "EventAgentReady": "대기",
    "EventHeld": "보류",
    "EventRetrieved": "보류해제",
    "EventRinging": "전화받기",
    "EventDialing": "전화걸기",
    "EventReleased": "전화종료",
    "EventAbandoned": "포기호",
    "EventError": "에러",
    "EventPartyChanged": "콜파티변경",
}

def map_cpi_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    CPI 로그 이벤트 이름을 한글로 매핑합니다.
    .replace(mapping) 을 쓰므로 벡터화되어 빠릅니다.
    """
    df = df.copy()
    df["APPNM"] = df["APPNM"].replace(CPI_EVENT_MAPPING)
    # 관심 이벤트만 필터
    keep = ["대기", "보류", "보류해제"]
    return df[df["APPNM"].isin(keep)]

def drop_telephone_apps(df: pd.DataFrame) -> pd.DataFrame:
    """APPNM 컬럼에 '전화'가 들어간 시스템 로그를 제거합니다."""
    mask = df["APPNM"].str.contains("전화", na=False)
    return df[~mask].reset_index(drop=True)