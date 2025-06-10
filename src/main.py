import logging
from src.config import Config
from src.data_loader import load_consultation_data, load_call_records
from src.preprocessing import map_cpi_events, drop_telephone_apps
from src.feature_engineering import add_call_flags, generate_case_id, drop_consecutive_duplicates

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M",
    )

def main(config_path: str):
    setup_logging()
    cfg = Config(config_path)
    logging.info("데이터 로드 시작")
    con_df = load_consultation_data(cfg.database_ids, cfg.raw_path)
    call_df = load_call_records(cfg.database_ids, cfg.raw_path)

    logging.info("전처리 시작")
    con_df = drop_telephone_apps(con_df)
    cpi_df = map_cpi_events(con_df)

    # 예시: 전화 기록과 합치기 등...

    logging.info("특성 엔지니어링 시작")
    df = add_call_flags(cpi_df)
    df = generate_case_id(df)
    df = drop_consecutive_duplicates(df)

    out_path = cfg.processed_path / "result_final.csv"
    df.to_csv(out_path, index=False)
    logging.info(f"최종 결과를 {out_path}에 저장했습니다.")

if __name__ == "__main__":
    import sys
    config_file = sys.argv[1] if len(sys.argv) > 1 else "configs/config.yaml"
    main(config_file)