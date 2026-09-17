"""
Data loading and preprocessing utilities for World Happiness Report (2015 - 2019).
"""

from pathlib import Path
from typing import Dict, Optional, Union
import pandas as pd

# Đường dẫn mặc định tương đối chuẩn
DEFAULT_RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

# Bảng quy đổi tên cột qua các năm về định dạng chuẩn thống nhất
COLUMN_MAPPING = {
    # 2015 & 2016
    "Country": "country",
    "Region": "region",
    "Happiness Rank": "happiness_rank",
    "Happiness Score": "happiness_score",
    "Economy (GDP per Capita)": "gdp_per_capita",
    "Family": "social_support",
    "Health (Life Expectancy)": "healthy_life_expectancy",
    "Freedom": "freedom",
    "Trust (Government Corruption)": "corruption_perception",
    "Generosity": "generosity",
    "Dystopia Residual": "dystopia_residual",

    # 2017
    "Happiness.Rank": "happiness_rank",
    "Happiness.Score": "happiness_score",
    "Economy..GDP.per.Capita.": "gdp_per_capita",
    "Health..Life.Expectancy.": "healthy_life_expectancy",
    "Trust..Government.Corruption.": "corruption_perception",
    "Dystopia.Residual": "dystopia_residual",

    # 2018 & 2019
    "Overall rank": "happiness_rank",
    "Country or region": "country",
    "Score": "happiness_score",
    "GDP per capita": "gdp_per_capita",
    "Social support": "social_support",
    "Healthy life expectancy": "healthy_life_expectancy",
    "Freedom to make life choices": "freedom",
    "Perceptions of corruption": "corruption_perception",
}


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Đổi tên các cột của DataFrame về chuẩn snake_case thống nhất.
    """
    rename_dict = {col: COLUMN_MAPPING[col] for col in df.columns if col in COLUMN_MAPPING}
    return df.rename(columns=rename_dict)


def load_year_data(year: int, raw_dir: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Tải dữ liệu của một năm cụ thể và gắn thêm cột 'year'.
    """
    raw_path = Path(raw_dir) if raw_dir else DEFAULT_RAW_DIR
    file_path = raw_path / f"{year}.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {file_path}")

    df = pd.read_csv(file_path)
    df = standardize_columns(df)
    df["year"] = year
    return df


def load_raw_data(
    years: list = [2015, 2016, 2017, 2018, 2019],
    raw_dir: Optional[Union[str, Path]] = None
) -> Dict[int, pd.DataFrame]:
    """
    Tải toàn bộ dữ liệu thô các năm và trả về dictionary {year: df}.
    """
    data_dict = {}
    for y in years:
        data_dict[y] = load_year_data(y, raw_dir=raw_dir)
    return data_dict
