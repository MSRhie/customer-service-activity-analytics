import pandas as pd
import pytest

from src.feature_engineering import (
    add_call_flags,
    generate_case_id,
    drop_consecutive_duplicates
)

@pytest.fixture
def call_df():
    # database A 에는 2개의 세션, B 에는 1개의 세션
    data = {
        "database_id": ["A","A","A","B","B"],
        "LDATE": pd.to_datetime([
            "2022-01-01 10:00",  # A 의 첫 통화 시작
            "2022-01-01 10:05",  # A 의 첫 통화 종료
            "2022-01-01 11:00",  # A 의 두 번째 통화 시작
            "2022-02-02 09:00",  # B 의 통화 시작
            "2022-02-02 09:10",  # B 의 통화 종료
        ]),
        "APPNM": [
            "전화걸기", "전화종료",
            "전화받기",    # A 의 두 번째 세션은 전화받기만
            "전화걸기", "전화종료"
        ]
    }
    return pd.DataFrame(data)

def test_add_call_flags_creates_flags(call_df):
    df = add_call_flags(call_df)
    # 컬럼 존재 확인
    assert {"전화걸기_flag","전화받기_flag","전화걸고받기_flag"}.issubset(df.columns)

    # 개별 플래그 동작 확인
    assert df.loc[df["APPNM"]=="전화걸기","전화걸기_flag"].eq(1).all()
    assert df.loc[df["APPNM"]=="전화종료","전화걸기_flag"].eq(0).all()

def test_generate_case_id_prefix_and_uniqueness(call_df):
    flagged = add_call_flags(call_df)
    with_case = generate_case_id(flagged)

    # case_id 컬럼 존재
    assert "case_id" in with_case.columns

    # 각 행의 case_id 가 "database_id_YYYY-MM-DD" 로 시작하는지
    for _, row in with_case.iterrows():
        prefix = f"{row['database_id']}_{row['LDATE'].date()}"
        assert row["case_id"].startswith(prefix)

    # A 데이터는 서로 다른 세션이 2개여서 고유 case_id 2개
    a_ids = with_case.query("database_id=='A'")["case_id"].unique()
    assert len(a_ids) == 2

    # B 데이터는 하나의 세션이므로 case_id 1개
    b_ids = with_case.query("database_id=='B'")["case_id"].unique()
    assert len(b_ids) == 1

def test_drop_consecutive_duplicates_collapses_runs():
    df = pd.DataFrame({
        "case_id": ["C1","C1","C1","C2","C2"],
        "APPNM":    ["A","A","B","X","X"]
    })
    deduped = drop_consecutive_duplicates(df)

    # 연속 중복 제거 후 A→B, X만 남아야 함
    assert list(deduped["APPNM"]) == ["A","B","X"]
    # 케이스별로 첫 등장만 남아야 함
    assert not any(deduped.duplicated(["case_id","APPNM"]))