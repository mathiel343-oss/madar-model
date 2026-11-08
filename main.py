
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

app = FastAPI(
    title="MADAR V2 API",
    description="Predictive Waste Management - Mina Prototype",
    version="2.0.0"
)

# السماح لواجهة الموقع بالتواصل مع API أثناء التطوير.
# قبل النشر الفعلي يجب تحديد نطاق الموقع المسموح.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"]
)

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "MADAR_V2_Project" / "predictions.csv"


def load_bins():
    """قراءة نتائج الحاويات المحفوظة."""

    if not DATA_FILE.exists():
        raise HTTPException(
            status_code=503,
            detail="Predictions data is unavailable"
        )

    df = pd.read_csv(DATA_FILE)

    # تحويل القيم غير الرقمية مثل NaN إلى null
    # لتكون صالحة للإرسال بصيغة JSON.

    df = df.astype(object).where(
        pd.notnull(df), None
    )

    return df


@app.get("/")
def home():
    """الواجهة الرئيسية للتأكد من تشغيل النظام."""

    return {
        "project": "MADAR V2",
        "status": "running",
        "message": "MADAR API is ready",
        "data_type": "synthetic"
    }


@app.get("/api/health")
def health():
    """فحص جاهزية API وملف البيانات."""

    return {
        "status": "ok" if DATA_FILE.exists() else "missing_data",
        "predictions_file_exists": DATA_FILE.exists()
    }


@app.get("/api/bins")
def get_bins():
    """إرجاع جميع الحاويات مع نتائج التنبؤ والأولويات."""

    df = load_bins()

    return {
        "total_bins": len(df),
        "data_type": "synthetic_simulation",
        "bins": df.to_dict(orient="records")
    }


@app.get("/api/bins/{bin_id}")
def get_bin(bin_id: str):
    """إرجاع تفاصيل حاوية واحدة باستخدام رقمها."""

    df = load_bins()

    result = df[
        df["bin_id"].astype(str) == bin_id
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Bin not found"
        )

    return result.iloc[0].to_dict()


# ============================================================
# MADAR V2 - Operational API Endpoints
# ============================================================

def load_csv(filename):
    """قراءة ملف CSV وتحويل القيم المفقودة إلى null."""

    file_path = BASE_DIR / "MADAR_V2_Project" / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=503,
            detail=f"Data file unavailable: {filename}"
        )

    df = pd.read_csv(file_path)

    # إزالة القيم غير الصالحة لـ JSON
    df = df.astype(object).where(
        pd.notnull(df), None
    )

    return df


@app.get("/api/map")
def get_map_data():
    """إرجاع مواقع الحاويات ونتائج التنبؤ."""

    df = load_csv("map_data.csv")

    return {
        "total_bins": len(df),
        "data_type": "synthetic_simulation",
        "bins": df.to_dict(orient="records")
    }


@app.get("/api/priorities")
def get_priorities():
    """إرجاع الحاويات مرتبة حسب الأولوية."""

    df = load_csv("predictions.csv")

    df = df.sort_values(
        by="priority_score",
        ascending=False
    )

    return {
        "total_bins": len(df),
        "bins": df.to_dict(orient="records")
    }


@app.get("/api/simulation")
def get_simulation():
    """إرجاع نتائج محاكاة أعداد فرق النظافة."""

    df = load_csv("simulation.csv")

    return {
        "total_scenarios": len(df),
        "scenarios": df.to_dict(orient="records")
    }


@app.get("/api/routes")
def get_routes():
    """إرجاع نتائج توزيع الحاويات على الفرق."""

    df = load_csv("routes.csv")

    return {
        "total_teams": len(df),
        "routes": df.to_dict(orient="records"),
        "distance_type": "straight_line_km"
    }
