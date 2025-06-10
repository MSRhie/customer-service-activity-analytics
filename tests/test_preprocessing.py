import pandas as pd
import pytest

from src.preprocessing import map_cpi_events, drop_telephone_apps

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "APPNM": [
            "EventAgentReady",  # 대기
            "EventHeld",        # 보류
            "EventRetrieved",   # 보류해제
            "EventDialing",     # 전화걸기 → 필터링 후 drop
            "OtherApp"          # 불필요 앱
        ]
    })

def test_map_cpi_events_maps_and_filters_correctly(sample_df):
    df = sample_df.copy()
    mapped = map_cpi_events(df)

    # 매핑된 컬럼 값 확인
    assert set(mapped["APPNM"]) == {"대기", "보류", "보류해제"}

    # 원본에 없던 값이 생기면 안 되고, EventDialing 은 필터링 돼야 함
    assert "전화걸기" not in mapped["APPNM"].values
    assert "OtherApp" not in mapped["APPNM"].values

def test_drop_telephone_apps_removes_전화_entries():
    df = pd.DataFrame({
        "APPNM": ["전화받기", "전화걸기", "포기호", "대기", None]
    })
    cleaned = drop_telephone_apps(df)

    # "전화" 단어가 들어간 모든 행이 제거돼야 함
    assert all(~cleaned["APPNM"].str.contains("전화", na=False))
    # "대기" 행은 남아 있어야 함
    assert "대기" in cleaned["APPNM"].values