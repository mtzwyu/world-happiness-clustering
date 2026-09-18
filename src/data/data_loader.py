"""
Nạp và tiền xử lý dữ liệu World Happiness Report (2015 - 2019).

Phạm vi trách nhiệm: đọc dữ liệu gốc, chuẩn hóa tên cột và tên quốc gia, dựng bảng
trung gian dùng chung cho cả 5 năm, và cung cấp hàm đọc lại các tệp đã sinh ra.

Quy ước:
- Tên hàm/biến bằng tiếng Anh, chú thích bằng tiếng Việt.
- Bảng trung gian chỉ giữ bộ cột trong INTERIM_COLUMNS (xem lý do ở DROPPED_COLUMNS_NOTE).
- Đường dẫn luôn tính từ gốc repo, không phụ thuộc máy cá nhân.
"""

from pathlib import Path
from typing import Dict, Iterable, Optional, Union
import pandas as pd

# --------------------------------------------------------------------------------------
# ĐƯỜNG DẪN CHUẨN (tính từ gốc repo)
# --------------------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_DIR = REPO_ROOT / "data" / "raw"
DEFAULT_INTERIM_DIR = REPO_ROOT / "data" / "interim"
DEFAULT_PROCESSED_DIR = REPO_ROOT / "data" / "processed"

DEFAULT_YEARS = (2015, 2016, 2017, 2018, 2019)
INTERIM_FILENAME = "happiness_merged.csv"

# --------------------------------------------------------------------------------------
# ÁNH XẠ TÊN CỘT QUA CÁC NĂM (mỗi năm một cách đặt tên khác nhau)
# --------------------------------------------------------------------------------------
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

# Bộ cột cố định của bảng trung gian; cột nào không có ở một năm sẽ được thêm giá trị thiếu.
INTERIM_COLUMNS = [
    "year",
    "country",
    "region",
    "happiness_rank",
    "happiness_score",
    "gdp_per_capita",
    "social_support",
    "healthy_life_expectancy",
    "freedom",
    "generosity",
    "corruption_perception",
    "dystopia_residual",
]

# Các cột bị loại bỏ khỏi bảng trung gian và lý do (dùng để giải thích trong notebook 01 và báo cáo).
DROPPED_COLUMNS_NOTE = {
    "Standard Error": "sai số chuẩn của điểm hạnh phúc, không phải yếu tố cơ sở",
    "Lower Confidence Interval": "khoảng tin cậy của điểm hạnh phúc, không phải yếu tố cơ sở",
    "Upper Confidence Interval": "khoảng tin cậy của điểm hạnh phúc, không phải yếu tố cơ sở",
    "Whisker.high": "biên trên khoảng bất định của điểm hạnh phúc ở bản 2017",
    "Whisker.low": "biên dưới khoảng bất định của điểm hạnh phúc ở bản 2017",
}

# --------------------------------------------------------------------------------------
# CHUẨN HÓA TÊN QUỐC GIA (phục vụ phân tích 5 năm và ánh xạ bản đồ)
# --------------------------------------------------------------------------------------
# Một số quốc gia đổi tên giữa các năm; nếu không chuẩn hóa thì bảng dịch chuyển cụm
# sẽ tách một quốc gia thành hai dòng. Dùng tên chuẩn hiện hành.
COUNTRY_NAME_FIXES = {
    "Macedonia": "North Macedonia",
    "Swaziland": "Eswatini",
    "Trinidad & Tobago": "Trinidad and Tobago",
}

# Ánh xạ tên quốc gia sang mã ISO-3 cho bản đồ thế giới. Chỉ liệt kê các tên mà cách
# nhận diện theo tên của thư viện vẽ bản đồ thường không khớp; các tên còn lại để
# thư viện tự nhận diện theo tên.
COUNTRY_ISO3_OVERRIDES = {
    "Bolivia": "BOL",
    "Comoros": "COM",
    "Congo (Brazzaville)": "COG",
    "Congo (Kinshasa)": "COD",
    "Czech Republic": "CZE",
    "Egypt": "EGY",
    "Eswatini": "SWZ",
    "Gambia": "GMB",
    "Hong Kong": "HKG",
    "Iran": "IRN",
    "Ivory Coast": "CIV",
    "Kosovo": "XKX",
    "Laos": "LAO",
    "Moldova": "MDA",
    "North Macedonia": "MKD",
    "Palestinian Territories": "PSE",
    "Russia": "RUS",
    "South Korea": "KOR",
    "Syria": "SYR",
    "Taiwan": "TWN",
    "Trinidad and Tobago": "TTO",
    "Turkey": "TUR",
    "Venezuela": "VEN",
    "Vietnam": "VNM",
    "Yemen": "YEM",
}


# --------------------------------------------------------------------------------------
# 1. ĐỌC DỮ LIỆU GỐC
# --------------------------------------------------------------------------------------
def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Đổi tên các cột của DataFrame về chuẩn snake_case thống nhất."""
    rename_dict = {col: COLUMN_MAPPING[col] for col in df.columns if col in COLUMN_MAPPING}
    return df.rename(columns=rename_dict)


def harmonize_country_names(df: pd.DataFrame, column: str = "country") -> pd.DataFrame:
    """Chuẩn hóa tên quốc gia giữa các năm (bỏ khoảng trắng thừa và đổi tên cũ)."""
    df = df.copy()
    df[column] = df[column].astype(str).str.strip()
    df[column] = df[column].replace(COUNTRY_NAME_FIXES)
    return df


def load_year_data(year: int, raw_dir: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Tải dữ liệu của một năm cụ thể, chuẩn hóa tên cột và gắn thêm cột 'year'."""
    raw_path = Path(raw_dir) if raw_dir else DEFAULT_RAW_DIR
    file_path = raw_path / f"{year}.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {file_path}")

    df = pd.read_csv(file_path)
    df = standardize_columns(df)
    df["year"] = year
    return df


def load_raw_data(
    years: Optional[Iterable[int]] = None,
    raw_dir: Optional[Union[str, Path]] = None,
) -> Dict[int, pd.DataFrame]:
    """Tải dữ liệu thô các năm và trả về dictionary {year: df}."""
    year_list = list(years) if years is not None else list(DEFAULT_YEARS)
    return {year: load_year_data(year, raw_dir=raw_dir) for year in year_list}


# --------------------------------------------------------------------------------------
# 2. DỰNG BẢNG TRUNG GIAN 5 NĂM
# --------------------------------------------------------------------------------------
def build_interim_dataset(
    years: Optional[Iterable[int]] = None,
    raw_dir: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """
    Ghép dữ liệu các năm thành một bảng trung gian có bộ cột cố định.

    - Chuẩn hóa tên cột và tên quốc gia trước khi ghép.
    - Cột nào không tồn tại ở một năm (ví dụ 'region' chỉ có 2015-2016) sẽ nhận giá trị thiếu,
      giữ nguyên vị trí cột để mọi năm dùng chung một schema.
    - Nếu truyền output_path thì ghi CSV (mặc định dùng ở notebook 01).
    """
    raw_data = load_raw_data(years=years, raw_dir=raw_dir)

    frames = []
    for year, df in raw_data.items():
        df = harmonize_country_names(df)
        for column in INTERIM_COLUMNS:
            if column not in df.columns:
                df[column] = pd.NA
        frames.append(df[INTERIM_COLUMNS])

    merged = pd.concat(frames, ignore_index=True)
    merged = merged.sort_values(["year", "country"], ignore_index=True)

    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        merged.to_csv(path, index=False)

    return merged


# --------------------------------------------------------------------------------------
# 3. ĐỌC LẠI DỮ LIỆU ĐÃ SINH RA
# --------------------------------------------------------------------------------------
def load_interim(
    interim_dir: Optional[Union[str, Path]] = None,
    filename: str = INTERIM_FILENAME,
) -> pd.DataFrame:
    """
    Đọc bảng trung gian đã sinh bởi notebook 01.

    Nếu chưa có tệp, báo lỗi kèm hướng dẫn để người chạy biết phải chạy notebook nào trước.
    """
    base_dir = Path(interim_dir) if interim_dir else DEFAULT_INTERIM_DIR
    path = base_dir / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Chưa có bảng trung gian: {path}\n"
            "Hãy chạy notebooks/01_data_understanding_and_cleaning.ipynb trước."
        )
    return pd.read_csv(path)


def load_processed(
    filename: str,
    processed_dir: Optional[Union[str, Path]] = None,
) -> pd.DataFrame:
    """Đọc một tệp kết quả trong data/processed (ví dụ 'final_clustered_2019.csv')."""
    base_dir = Path(processed_dir) if processed_dir else DEFAULT_PROCESSED_DIR
    path = base_dir / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Chưa có tệp kết quả: {path}\n"
            "Hãy chạy notebooks/04_cluster_profiling_and_evaluation.ipynb trước."
        )
    return pd.read_csv(path)


# --------------------------------------------------------------------------------------
# 4. ÁNH XẠ MÃ QUỐC GIA CHO BẢN ĐỒ
# --------------------------------------------------------------------------------------
def country_to_iso3(country_name: str) -> Optional[str]:
    """
    Trả về mã ISO-3 cho tên quốc gia nếu có trong bảng override, ngược lại trả None.

    Quy ước: None nghĩa là "để thư viện vẽ bản đồ tự nhận diện theo tên"; nếu vẫn không
    khớp thì ứng dụng demo phải đếm và hiển thị số quốc gia chưa ánh xạ được.
    """
    if country_name is None:
        return None
    return COUNTRY_ISO3_OVERRIDES.get(str(country_name).strip())
