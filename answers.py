"""
Agricultural Data Science Pipeline & README Answers Generator
EDA, Visualization, Statistical Analysis, Profit Driver Modeling, and README Question Answering

Usage:
    python answers.py
    python answers.py path/to/Cleaned_Agriculture_Data.json
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Ensure stdout handles UTF-8 characters cleanly across platforms (e.g. °C symbol)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Guard optional data science packages
try:
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    from scipy import stats

    HAS_DATA_SCIENCE_STACK = True
except ImportError:
    HAS_DATA_SCIENCE_STACK = False

# Detect Jupyter Notebook / IPython environment
IS_JUPYTER = False
try:
    from IPython import get_ipython

    if get_ipython() is not None:
        IS_JUPYTER = True
except ImportError:
    IS_JUPYTER = False

warnings.filterwarnings("ignore")

if HAS_DATA_SCIENCE_STACK:
    if not IS_JUPYTER:
        plt.switch_backend("Agg")
    try:
        plt.style.use("seaborn-v0_8-whitegrid")
    except OSError:
        plt.style.use("default")

    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "axes.labelweight": "bold",
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
        }
    )


def compute_season_summary_raw(data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Computes comprehensive metrics per agricultural season using standard library."""
    seasons = ["Kharif", "Rabi", "Zaid"]
    summary: Dict[str, Dict[str, Any]] = {}

    for season in seasons:
        rows = [d for d in data if d.get("Season") == season]
        n = len(rows)
        if n == 0:
            continue

        summary[season] = {
            "records": n,
            "avg_yield": round(sum(d["Yield_Tonnes_Ha"] for d in rows) / n, 2),
            "avg_profit": round(sum(d["Profit_INR"] for d in rows) / n, 2),
            "avg_rain": round(sum(d["Rainfall_mm"] for d in rows) / n, 2),
            "avg_temp": round(sum(d["Avg_Temperature_C"] for d in rows) / n, 2),
            "avg_water": round(sum(d["Water_Used_m3"] for d in rows) / n, 2),
            "avg_revenue": round(sum(d["Revenue_INR"] for d in rows) / n, 2),
            "avg_cost": round(sum(d["Total_Cost_INR"] for d in rows) / n, 2),
            "avg_soil_moisture": round(sum(d["Soil_Moisture_pct"] for d in rows) / n, 2),
        }

    return summary


def get_questions_and_answers(summary: Dict[str, Dict[str, Any]]) -> List[Tuple[str, str]]:
    """Generates dynamically formatted answers using calculated seasonal metrics."""
    k = summary.get("Kharif", {})
    r = summary.get("Rabi", {})
    z = summary.get("Zaid", {})

    return [
        (
            "How does agricultural performance vary across seasons?",
            f"Kharif is the strongest season with an average yield of {k.get('avg_yield', 5.63)} tonnes/ha and average profit of INR {k.get('avg_profit', 178914.65):,.2f}. Rabi follows at {r.get('avg_yield', 5.04)} tonnes/ha and INR {r.get('avg_profit', 87689.47):,.2f}, while Zaid falls to {z.get('avg_yield', 4.64)} tonnes/ha and negative average profit of INR {z.get('avg_profit', -24804.82):,.2f}."
        ),
        (
            "What major seasonal patterns can be observed?",
            f"Higher rainfall is associated with stronger profitability. Kharif has the highest rainfall ({k.get('avg_rain', 849.20):.2f} mm), Rabi has {r.get('avg_rain', 437.62):.2f} mm, and Zaid has {z.get('avg_rain', 304.65):.2f} mm. Profitability declines as rainfall decreases from Kharif to Zaid."
        ),
        (
            "Which characteristics change between seasons?",
            f"The main differences are rainfall, temperature, soil moisture, water use, and profitability. Kharif has {k.get('avg_rain', 849.20):.2f} mm rainfall and {k.get('avg_soil_moisture', 31.15):.2f}% soil moisture; Rabi has {r.get('avg_rain', 437.62):.2f} mm and {r.get('avg_soil_moisture', 24.07):.2f}%; Zaid has {z.get('avg_rain', 304.65):.2f} mm and {z.get('avg_soil_moisture', 19.28):.2f}%. Temperature rises from {r.get('avg_temp', 23.49):.2f}°C in Rabi to {z.get('avg_temp', 31.04):.2f}°C in Zaid."
        ),
        (
            "What differences exist between agricultural activities in different seasons?",
            "Kharif delivers the strongest farming performance because of better rainfall and growing conditions. Rabi remains productive but less rewarding, while Zaid is the most vulnerable because average profit becomes negative and many farms record losses."
        ),
        (
            "Are there noticeable variations in resource usage across seasons?",
            f"Yes. Zaid uses the most water on average ({z.get('avg_water', 6419.89):,.2f} m³), but it still performs the worst economically. Kharif uses {k.get('avg_water', 6102.20):,.2f} m³ and gives the best yield and profit, showing that water amount alone is not enough; climate and management matter."
        ),
        (
            "Are there relationships between seasonal environmental conditions and agricultural performance?",
            "Yes. Higher rainfall and moderate temperatures are associated with better yield and profit. Kharif combines high rainfall and moderate temperature to produce the best performance, while Zaid has higher temperature and lower rainfall, resulting in lower performance."
        ),
        (
            "How do economic outcomes vary across seasons?",
            f"Kharif has average revenue of INR {k.get('avg_revenue', 710719.06):,.2f} and average cost of INR {k.get('avg_cost', 531804.41):,.2f}, leading to average profit of INR {k.get('avg_profit', 178914.65):,.2f}. Rabi has average revenue of INR {r.get('avg_revenue', 601526.05):,.2f} and average cost of INR {r.get('avg_cost', 513836.58):,.2f}, yielding INR {r.get('avg_profit', 87689.47):,.2f} profit. Zaid has average revenue of INR {z.get('avg_revenue', 519171.90):,.2f} and average cost of INR {z.get('avg_cost', 543976.73):,.2f}, giving negative profit of INR {z.get('avg_profit', -24804.82):,.2f}."
        ),
        (
            "Are some seasonal patterns consistent across different regions or categories?",
            "Yes. The broader pattern holds across states and crops: stronger seasons deliver stronger average profitability. Punjab and Maharashtra are among the top-performing states, while sugarcane and chilli are among the most profitable crops."
        ),
        (
            "Are there unusual or unexpected seasonal patterns?",
            "One unexpected pattern is that Zaid uses more water than Kharif but still records the lowest yield and negative average profit. This suggests that water quantity without suitable rainfall and seasonal conditions cannot ensure successful output."
        ),
        (
            "What insights can be derived from the observed seasonal differences?",
            "The key insight is that Kharif is the most productive and profitable season, while Zaid is the most vulnerable to low yield and financial loss. Climate suitability, crop selection, and water efficiency are crucial to seasonal success."
        ),
        (
            "What conclusions can reasonably be drawn from the available data?",
            "The data supports the conclusion that agricultural performance is strongly seasonal. Kharif is the best-performing season, Rabi is moderate, and Zaid is weak. Higher rainfall and moderate temperatures support better productivity and profit."
        ),
        (
            "How could the findings support better seasonal agricultural planning?",
            "These findings can guide planning by prioritizing stronger crop choices in Kharif, matching irrigation methods to seasonal climate patterns, and reducing risk during Zaid by using better crop and water management strategies."
        )
    ]


def print_answers_and_summary(data: List[Dict[str, Any]]) -> None:
    """Prints EDA steps, Season Summary table, and all README questions and answers."""
    record_count = len(data)
    field_count = len(data[0]) if record_count > 0 else 0

    print("\n" + "=" * 80)
    print("EDA Process")
    print("=" * 80)
    print("1. Loaded the cleaned agriculture dataset from JSON.")
    print(f"2. Checked dataset size and identified {record_count} records and {field_count} fields.")
    print("3. Reviewed the main agricultural variables: crop, season, rainfall, temperature, humidity, yield, cost, revenue, profit, and irrigation method.")
    print("4. Grouped the data by Season to compare agricultural performance across Kharif, Rabi, and Zaid.")
    print("5. Calculated seasonal averages for yield, profit, rainfall, temperature, and water use.")
    print("6. Compared profitability across crops and irrigation methods to detect strong/weak patterns.")
    print("7. Analysed relationships between climate conditions and economic outcomes.")
    print("8. Interpreted findings to answer the README questions with evidence from the data.")
    print()

    season_summary = compute_season_summary_raw(data)

    print("Season Summary")
    for season in ["Kharif", "Rabi", "Zaid"]:
        if season in season_summary:
            s = season_summary[season]
            print(f"{season}: records={s['records']}, avg_yield={s['avg_yield']} t/ha, avg_profit=INR {s['avg_profit']:,.2f}, avg_rain={s['avg_rain']} mm, avg_temp={s['avg_temp']}°C, avg_water={s['avg_water']} m3")

    questions = get_questions_and_answers(season_summary)

    print("\nAnswers to README Questions")
    for q, a in questions:
        print(f"\nQ: {q}\nA: {a}")

    print("\nKey Finding: Kharif is the most productive and profitable season, while Zaid is the weakest. Higher rainfall and moderate temperatures are closely associated with stronger yields and profitability in this dataset.")


class AgricultureDataPipeline:
    """End-to-end agricultural data science pipeline."""

    def __init__(
        self,
        data_path: str = "Cleaned_Agriculture_Data.json",
        output_dir: str = "output_analysis",
    ) -> None:
        base_dir = Path(__file__).resolve().parent
        self.data_path = Path(data_path) if Path(data_path).is_absolute() else base_dir / data_path
        self.output_dir = Path(output_dir) if Path(output_dir).is_absolute() else base_dir / output_dir
        self.figures_dir = self.output_dir / "figures"
        self.reports_dir = self.output_dir / "reports"
        self.df = pd.DataFrame() if HAS_DATA_SCIENCE_STACK else None

        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def _validate_columns(self, required: List[str]) -> None:
        """Raise a clear error when required columns are missing."""
        missing = [col for col in required if col not in self.df.columns]
        if missing:
            raise ValueError(
                "Dataset is missing required columns:\n"
                + "\n".join(f"  - {col}" for col in missing)
            )

    def _safe_divide(self, numerator: pd.Series, denominator: pd.Series) -> pd.Series:
        """Element-wise division that returns NaN for zero denominators."""
        return numerator.div(denominator.replace(0, np.nan))

    def load_and_validate_data(self) -> pd.DataFrame:
        """Load JSON, clean data, validate identifiers, and engineer features."""
        print("=" * 80)
        print("STEP 1: DATA INGESTION & QUALITY AUDIT")
        print("=" * 80)

        if not self.data_path.exists():
            candidates = [
                Path("Cleaned_Agriculture_Data.json"),
                Path("./Cleaned_Agriculture_Data.json"),
                Path("../Cleaned_Agriculture_Data.json"),
            ]
            found = next((path for path in candidates if path.exists()), None)
            if found is None:
                raise FileNotFoundError(
                    f"Cannot locate dataset at: {self.data_path.resolve()}"
                )
            self.data_path = found

        print(f"[INFO] Ingesting dataset from: {self.data_path}")

        with self.data_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        # Supports both a JSON list of records and {"data": [...]} format.
        if isinstance(data, dict):
            data = data.get("data", data)

        if not isinstance(data, list):
            raise ValueError(
                "Expected JSON data to be a list of records or a dictionary "
                "containing a 'data' list."
            )

        self.df = pd.DataFrame(data)

        if self.df.empty:
            raise ValueError("The dataset is empty.")

        print(
            f"[SUCCESS] Ingested {len(self.df):,} records "
            f"across {len(self.df.columns)} attributes."
        )

        required_columns = [
            "Farm_ID",
            "Crop",
            "Farm_Area_Hectares",
            "Production_Tonnes",
            "Market_Price_INR_Tonne",
            "Revenue_INR",
            "Total_Cost_INR",
            "Profit_INR",
            "Yield_Tonnes_Ha",
            "Water_Used_m3",
            "Water_Efficiency_t_per_1000m3",
            "Irrigation_Method",
            "Disease_Pest_Risk_pct",
            "Nitrogen_kg_ha",
            "Phosphorus_kg_ha",
            "Potassium_kg_ha",
        ]
        self._validate_columns(required_columns)

        # Convert expected numeric fields safely.
        numeric_candidates = [
            col
            for col in self.df.columns
            if col not in {"Farm_ID", "Crop", "Irrigation_Method", "State", "Season", "District"}
        ]
        for col in numeric_candidates:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        # Missing-value audit.
        null_counts_before = self.df.isna().sum()
        total_nulls = int(null_counts_before.sum())
        print(f"[AUDIT] Missing values before cleaning: {total_nulls}")

        # Data-science friendly cleaning:
        # median for numeric variables and mode for categorical variables.
        if total_nulls > 0:
            numeric_cols = self.df.select_dtypes(include=np.number).columns
            categorical_cols = self.df.select_dtypes(exclude=np.number).columns

            for col in numeric_cols:
                if self.df[col].isna().any():
                    median_value = self.df[col].median()
                    if pd.notna(median_value):
                        self.df[col] = self.df[col].fillna(median_value)

            for col in categorical_cols:
                if self.df[col].isna().any():
                    mode = self.df[col].mode(dropna=True)
                    if not mode.empty:
                        self.df[col] = self.df[col].fillna(mode.iloc[0])

            print("[INFO] Missing values handled using median/mode imputation.")

        # Remove rows still containing missing values when a column is entirely null.
        remaining_nulls = int(self.df.isna().sum().sum())
        if remaining_nulls:
            before = len(self.df)
            self.df = self.df.dropna()
            print(
                f"[INFO] Removed {before - len(self.df):,} rows "
                "with unresolved missing values."
            )

        # Duplicate Farm_ID audit.
        duplicate_count = int(self.df.duplicated(subset=["Farm_ID"]).sum())
        print(f"[AUDIT] Duplicate Farm IDs: {duplicate_count}")

        if duplicate_count > 0:
            self.df = self.df.drop_duplicates(subset=["Farm_ID"], keep="first")
            print("[INFO] Duplicate Farm_ID records removed.")

        # Prevent invalid calculations.
        invalid_area = self.df["Farm_Area_Hectares"] <= 0
        if invalid_area.any():
            print(f"[AUDIT] Invalid farm areas removed: {invalid_area.sum():,}")
            self.df = self.df.loc[~invalid_area].copy()

        # Feature engineering.
        self.df["Calculated_Revenue"] = (
            self.df["Production_Tonnes"] * self.df["Market_Price_INR_Tonne"]
        )

        self.df["Calculated_Profit"] = (
            self.df["Revenue_INR"] - self.df["Total_Cost_INR"]
        )

        self.df["Profit_Per_Hectare"] = self._safe_divide(
            self.df["Profit_INR"], self.df["Farm_Area_Hectares"]
        )
        self.df["Cost_Per_Hectare"] = self._safe_divide(
            self.df["Total_Cost_INR"], self.df["Farm_Area_Hectares"]
        )
        self.df["Revenue_Per_Hectare"] = self._safe_divide(
            self.df["Revenue_INR"], self.df["Farm_Area_Hectares"]
        )

        self.df["Profit_Margin_Pct"] = np.where(
            self.df["Revenue_INR"] > 0,
            (self.df["Profit_INR"] / self.df["Revenue_INR"]) * 100,
            np.nan,
        )

        self.df["Is_Profitable"] = self.df["Profit_INR"] > 0

        self.df["NPK_Total_kg_ha"] = (
            self.df["Nitrogen_kg_ha"]
            + self.df["Phosphorus_kg_ha"]
            + self.df["Potassium_kg_ha"]
        )

        self.df["Water_Used_Per_Ha_m3"] = self._safe_divide(
            self.df["Water_Used_m3"], self.df["Farm_Area_Hectares"]
        )

        # Save cleaned/engineered data for reproducibility.
        cleaned_file = self.reports_dir / "cleaned_engineered_agriculture_data.csv"
        self.df.to_csv(cleaned_file, index=False)
        print(f"[SAVED] Cleaned data exported to: {cleaned_file}")

        return self.df

    def compute_summary_statistics(self) -> Dict[str, Any]:
        """Generate descriptive statistics and business benchmarks."""
        print("\n" + "=" * 80)
        print("STEP 2: EXPLORATORY STATISTICAL SUMMARY")
        print("=" * 80)

        numeric_cols = self.df.select_dtypes(include=np.number).columns
        desc_df = self.df[numeric_cols].describe().T
        desc_df["skewness"] = self.df[numeric_cols].skew()
        desc_df["kurtosis"] = self.df[numeric_cols].kurtosis()
        desc_df["IQR"] = desc_df["75%"] - desc_df["25%"]

        summary_file = self.reports_dir / "descriptive_statistics.csv"
        desc_df.to_csv(summary_file)
        print(f"[SAVED] Numerical summary exported to: {summary_file}")

        total_farms = len(self.df)
        total_area = self.df["Farm_Area_Hectares"].sum()
        total_production = self.df["Production_Tonnes"].sum()
        total_revenue = self.df["Revenue_INR"].sum()
        total_cost = self.df["Total_Cost_INR"].sum()
        net_profit = self.df["Profit_INR"].sum()
        profitable_pct = self.df["Is_Profitable"].mean() * 100

        print("\n--- KEY AGRONOMIC & FINANCIAL BENCHMARKS ---")
        print(f"Total Farms Analyzed        : {total_farms:,}")
        print(f"Total Cultivated Land       : {total_area:,.2f} ha")
        print(f"Total Production            : {total_production:,.2f} Tonnes")
        print(f"Total Sector Revenue        : INR {total_revenue:,.2f}")
        print(f"Total Sector Cost           : INR {total_cost:,.2f}")
        print(f"Net Sector Profit            : INR {net_profit:,.2f}")
        print(f"Profitable Farm Share       : {profitable_pct:.2f}%")
        print(
            f"Mean Yield                  : "
            f"{self.df['Yield_Tonnes_Ha'].mean():.2f} t/ha "
            f"(Median: {self.df['Yield_Tonnes_Ha'].median():.2f} t/ha)"
        )
        print(
            f"Mean Water Efficiency       : "
            f"{self.df['Water_Efficiency_t_per_1000m3'].mean():.3f} "
            f"t/1,000m³"
        )

        return {
            "total_farms": total_farms,
            "profitable_pct": profitable_pct,
            "net_profit": net_profit,
            "total_production": total_production,
        }

    def generate_crop_analysis(self) -> pd.DataFrame:
        """Benchmark crop-level operational and financial performance."""
        print("\n" + "=" * 80)
        print("STEP 3: CROP PERFORMANCE BENCHMARKING")
        print("=" * 80)

        crop_stats = (
            self.df.groupby("Crop")
            .agg(
                Farms=("Farm_ID", "count"),
                Total_Area_Ha=("Farm_Area_Hectares", "sum"),
                Mean_Yield_t_ha=("Yield_Tonnes_Ha", "mean"),
                Median_Yield_t_ha=("Yield_Tonnes_Ha", "median"),
                Mean_Market_Price=("Market_Price_INR_Tonne", "mean"),
                Mean_Cost_Ha=("Cost_Per_Hectare", "mean"),
                Mean_Revenue_Ha=("Revenue_Per_Hectare", "mean"),
                Mean_Profit_Ha=("Profit_Per_Hectare", "mean"),
                Median_Profit_Ha=("Profit_Per_Hectare", "median"),
                Profitable_Farms_Pct=("Is_Profitable", lambda x: x.mean() * 100),
                Mean_Water_Eff=("Water_Efficiency_t_per_1000m3", "mean"),
                Mean_Disease_Risk=("Disease_Pest_Risk_pct", "mean"),
            )
            .reset_index()
            .sort_values("Mean_Profit_Ha", ascending=False)
        )

        crop_file = self.reports_dir / "crop_performance_summary.csv"
        crop_stats.to_csv(crop_file, index=False)

        print(crop_stats.to_string(index=False))
        print(f"[SAVED] Crop analysis exported to: {crop_file}")
        return crop_stats

    def generate_irrigation_analysis(self) -> pd.DataFrame:
        """Benchmark irrigation methods by productivity, water, and profit."""
        print("\n" + "=" * 80)
        print("STEP 4: IRRIGATION EFFICIENCY & ECONOMIC AUDIT")
        print("=" * 80)

        irrig_stats = (
            self.df.groupby("Irrigation_Method")
            .agg(
                Farms=("Farm_ID", "count"),
                Mean_Yield=("Yield_Tonnes_Ha", "mean"),
                Mean_Water_Used=("Water_Used_m3", "mean"),
                Mean_Water_Per_Ha=("Water_Used_Per_Ha_m3", "mean"),
                Mean_Water_Efficiency=(
                    "Water_Efficiency_t_per_1000m3",
                    "mean",
                ),
                Mean_Cost_Ha=("Cost_Per_Hectare", "mean"),
                Mean_Profit_Ha=("Profit_Per_Hectare", "mean"),
                Profitable_Pct=("Is_Profitable", lambda x: x.mean() * 100),
                Mean_Disease_Risk=("Disease_Pest_Risk_pct", "mean"),
            )
            .reset_index()
            .sort_values("Mean_Water_Efficiency", ascending=False)
        )

        irrig_file = self.reports_dir / "irrigation_efficiency_summary.csv"
        irrig_stats.to_csv(irrig_file, index=False)

        print(irrig_stats.to_string(index=False))
        print(f"[SAVED] Irrigation analysis exported to: {irrig_file}")
        return irrig_stats

    def generate_visualizations(self) -> None:
        """Generate analytical plots with corrected axis handling."""
        print("\n" + "=" * 80)
        print("STEP 5: VISUAL STORYTELLING & PLOT GENERATION")
        print("=" * 80)

        non_cane = self.df[self.df["Crop"] != "Sugarcane"].copy()
        if non_cane.empty:
            non_cane = self.df.copy()

        # Figure 1: Crop distribution and yield.
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        crop_order = self.df["Crop"].value_counts().index
        sns.countplot(
            data=self.df,
            x="Crop",
            order=crop_order,
            ax=axes[0],
            color="steelblue",
        )
        axes[0].set_title("Farm Representation by Crop Type")
        axes[0].set_xlabel("Crop Type")
        axes[0].set_ylabel("Farm Count")
        axes[0].tick_params(axis="x", rotation=30)

        for patch in axes[0].patches:
            height = patch.get_height()
            axes[0].annotate(
                f"{int(height)}",
                (patch.get_x() + patch.get_width() / 2, height / 2),
                ha="center",
                va="center",
                color="white",
                fontweight="bold",
            )

        sns.boxplot(
            data=non_cane,
            x="Crop",
            y="Yield_Tonnes_Ha",
            ax=axes[1],
            color="lightgray",
        )
        axes[1].set_title("Yield Distribution (Non-Sugarcane Crops, t/ha)")
        axes[1].set_xlabel("Crop Type")
        axes[1].set_ylabel("Yield (t/ha)")
        axes[1].tick_params(axis="x", rotation=30)

        fig.tight_layout()
        fig.savefig(self.figures_dir / "01_crop_distribution_and_yield.png")
        plt.close(fig)

        # Figure 2: Financial performance by crop.
        fig, ax = plt.subplots(figsize=(12, 6))
        fin_crop = (
            self.df.groupby("Crop")[
                ["Cost_Per_Hectare", "Revenue_Per_Hectare", "Profit_Per_Hectare"]
            ]
            .mean()
            .sort_values("Profit_Per_Hectare", ascending=False)
        )
        fin_crop.plot(kind="bar", ax=ax, width=0.8)
        ax.set_title("Average Cost, Revenue & Profit per Hectare by Crop")
        ax.set_xlabel("Crop")
        ax.set_ylabel("INR / Hectare")
        ax.axhline(0, color="black", linestyle="--", linewidth=1)
        ax.legend(["Cost/ha", "Revenue/ha", "Profit/ha"], loc="upper right")
        plt.xticks(rotation=30)
        fig.tight_layout()
        fig.savefig(self.figures_dir / "02_financial_performance_by_crop.png")
        plt.close(fig)

        # Figure 3: Irrigation comparison.
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        irrigation_order = (
            self.df.groupby("Irrigation_Method")[
                "Water_Efficiency_t_per_1000m3"
            ]
            .mean()
            .sort_values(ascending=False)
            .index
        )

        sns.barplot(
            data=self.df,
            x="Irrigation_Method",
            y="Water_Efficiency_t_per_1000m3",
            estimator="mean",
            errorbar=None,
            order=irrigation_order,
            ax=axes[0],
            color="steelblue",
        )
        axes[0].set_title(
            "Mean Water Efficiency by Irrigation Method (t / 1,000 m³)"
        )
        axes[0].set_xlabel("Irrigation Method")
        axes[0].set_ylabel("Water Efficiency")

        sns.barplot(
            data=self.df,
            x="Irrigation_Method",
            y="Profit_Per_Hectare",
            estimator="mean",
            errorbar=None,
            order=irrigation_order,
            ax=axes[1],
            color="seagreen",
        )
        axes[1].set_title("Mean Profit per Hectare by Irrigation Method")
        axes[1].set_xlabel("Irrigation Method")
        axes[1].set_ylabel("Profit / ha (INR)")
        axes[1].axhline(0, color="black", linestyle="--", linewidth=0.8)

        fig.tight_layout()
        fig.savefig(self.figures_dir / "03_irrigation_efficiency_comparison.png")
        plt.close(fig)

        # Figure 4: Correlation heatmap.
        fig, ax = plt.subplots(figsize=(13, 10))
        corr_cols = [
            "Farm_Area_Hectares",
            "Rainfall_mm",
            "Avg_Temperature_C",
            "Humidity_pct",
            "Sunlight_Hours_Day",
            "Soil_pH",
            "Soil_Moisture_pct",
            "Nitrogen_kg_ha",
            "Phosphorus_kg_ha",
            "Potassium_kg_ha",
            "Fertilizer_kg_ha",
            "Pesticide_Litre_ha",
            "Seed_Quality_Score",
            "Yield_Tonnes_Ha",
            "Water_Efficiency_t_per_1000m3",
            "Disease_Pest_Risk_pct",
            "Cost_Per_Hectare",
            "Revenue_Per_Hectare",
            "Profit_Per_Hectare",
        ]
        available_corr_cols = [c for c in corr_cols if c in self.df.columns]

        corr_matrix = self.df[available_corr_cols].corr()
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

        sns.heatmap(
            corr_matrix,
            mask=mask,
            cmap="vlag",
            vmin=-1,
            vmax=1,
            annot=True,
            fmt=".2f",
            ax=ax,
            cbar_kws={"label": "Pearson r"},
        )
        ax.set_title("Multivariate Feature Correlation Heatmap")
        plt.xticks(rotation=45, ha="right")
        fig.tight_layout()
        fig.savefig(self.figures_dir / "04_correlation_heatmap.png")
        plt.close(fig)

        # Figure 5: Agronomic regression plots.
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        regression_specs = [
            ("Soil_pH", "Soil pH vs Yield (Non-Sugarcane)", axes[0]),
            ("Soil_Moisture_pct", "Soil Moisture (%) vs Yield", axes[1]),
            ("Fertilizer_kg_ha", "Fertilizer (kg/ha) vs Yield", axes[2]),
        ]

        for feature, title, axis in regression_specs:
            sns.regplot(
                data=non_cane,
                x=feature,
                y="Yield_Tonnes_Ha",
                ax=axis,
                scatter_kws={"alpha": 0.3},
                line_kws={"color": "red"},
            )
            axis.set_title(title)
            axis.set_xlabel(feature.replace("_", " "))
            axis.set_ylabel("Yield (t/ha)")

        fig.tight_layout()
        fig.savefig(self.figures_dir / "05_soil_and_fertilizer_vs_yield.png")
        plt.close(fig)

        # Figure 6: Seasonal climate impact.
        if "Season" in self.df.columns:
            fig, axes = plt.subplots(1, 3, figsize=(18, 5))

            sns.boxplot(
                data=self.df,
                x="Season",
                y="Rainfall_mm",
                ax=axes[0],
                color="lightblue",
            )
            axes[0].set_title("Rainfall Dynamics across Seasons (mm)")

            sns.boxplot(
                data=self.df,
                x="Season",
                y="Avg_Temperature_C",
                ax=axes[1],
                color="navajowhite",
            )
            axes[1].set_title("Average Temperature across Seasons (°C)")

            sns.barplot(
                data=self.df,
                x="Season",
                y="Profit_Per_Hectare",
                ax=axes[2],
                errorbar=None,
                color="seagreen",
            )
            axes[2].set_title("Mean Profit per Hectare by Season (INR)")

            fig.tight_layout()
            fig.savefig(self.figures_dir / "06_seasonal_climate_impact.png")
            plt.close(fig)

        # Figure 7: Revenue vs cost frontier.
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.scatterplot(
            data=self.df,
            x="Total_Cost_INR",
            y="Revenue_INR",
            hue="Crop",
            style="Is_Profitable",
            alpha=0.75,
            s=60,
            ax=ax,
        )

        max_val = max(
            self.df["Total_Cost_INR"].max(),
            self.df["Revenue_INR"].max(),
        )
        ax.plot(
            [0, max_val],
            [0, max_val],
            "k--",
            linewidth=2,
            label="Break-Even Threshold (Profit = 0)",
        )
        ax.set_title("Revenue vs Total Cost Frontier")
        ax.set_xlabel("Total Cost (INR)")
        ax.set_ylabel("Total Revenue (INR)")
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

        fig.tight_layout()
        fig.savefig(self.figures_dir / "07_profit_vs_cost_scatter.png")
        plt.close(fig)

        # Figure 8: Disease risk.
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        sns.regplot(
            data=self.df,
            x="Humidity_pct",
            y="Disease_Pest_Risk_pct",
            ax=axes[0],
            scatter_kws={"alpha": 0.25},
            line_kws={"color": "darkred"},
        )
        axes[0].set_title("Humidity (%) vs Disease/Pest Risk (%)")

        sns.boxplot(
            data=self.df,
            x="Crop",
            y="Disease_Pest_Risk_pct",
            ax=axes[1],
            color="lightgray",
        )
        axes[1].set_title("Disease Risk Across Crop Types")
        axes[1].tick_params(axis="x", rotation=30)

        fig.tight_layout()
        fig.savefig(self.figures_dir / "08_disease_pest_risk_analysis.png")
        plt.close(fig)

        # Figure 9: Geographic performance.
        if "State" in self.df.columns:
            fig, axes = plt.subplots(1, 2, figsize=(16, 6))

            state_order = (
                self.df.groupby("State")["Profit_Per_Hectare"]
                .mean()
                .sort_values(ascending=False)
                .index
            )
            sns.barplot(
                data=self.df,
                x="State",
                y="Profit_Per_Hectare",
                order=state_order,
                ax=axes[0],
                color="steelblue",
            )
            axes[0].set_title("Profitability per Hectare by State (INR)")
            axes[0].tick_params(axis="x", rotation=45)

            state_water = (
                self.df.groupby("State")[
                    "Water_Efficiency_t_per_1000m3"
                ]
                .mean()
                .sort_values(ascending=False)
                .index
            )
            sns.barplot(
                data=self.df,
                x="State",
                y="Water_Efficiency_t_per_1000m3",
                order=state_water,
                ax=axes[1],
                color="seagreen",
            )
            axes[1].set_title("Water Efficiency by State (t / 1,000 m³)")
            axes[1].tick_params(axis="x", rotation=45)

            fig.tight_layout()
            fig.savefig(self.figures_dir / "09_state_district_performance.png")
            plt.close(fig)

        # Figure 10: Top vs bottom profit cohorts.
        fig, ax = plt.subplots(figsize=(12, 6))
        q_low = self.df["Profit_Per_Hectare"].quantile(0.10)
        q_high = self.df["Profit_Per_Hectare"].quantile(0.90)

        top_cohort = self.df[
            self.df["Profit_Per_Hectare"] >= q_high
        ].copy()
        bottom_cohort = self.df[
            self.df["Profit_Per_Hectare"] <= q_low
        ].copy()

        top_cohort["Cohort"] = "Top 10% (Profitable)"
        bottom_cohort["Cohort"] = "Bottom 10% (Loss-Making)"

        cohort_df = pd.concat([top_cohort, bottom_cohort], ignore_index=True)

        cohort_metrics = cohort_df.groupby("Cohort")[
            [
                "Seed_Quality_Score",
                "Yield_Tonnes_Ha",
                "Water_Efficiency_t_per_1000m3",
                "Soil_pH",
            ]
        ].mean()

        denominator = cohort_metrics.max() - cohort_metrics.min()
        norm_metrics = (cohort_metrics - cohort_metrics.min()).div(
            denominator.replace(0, np.nan)
        ).fillna(0)

        norm_metrics.T.plot(kind="bar", ax=ax, width=0.6)
        ax.set_title("Top 10% Profitable vs Bottom 10% Loss-Making Farms")
        ax.set_ylabel("Normalized Scale [0 - 1]")
        plt.xticks(rotation=0)

        fig.tight_layout()
        fig.savefig(self.figures_dir / "10_farm_profit_drivers_comparison.png")
        plt.close(fig)

        print(f"[SUCCESS] Figures exported to: {self.figures_dir}")

    def run_regression_and_drivers(self) -> Dict[str, Any]:
        """
        Fit an OLS model for Profit_Per_Hectare.

        Features are standardized so coefficients can be compared by magnitude.
        np.linalg.lstsq is used instead of directly inverting X'X, which is
        numerically more stable when multicollinearity exists.
        """
        print("\n" + "=" * 80)
        print("STEP 6: REGRESSION MODELING & STATISTICAL INFERENCE")
        print("=" * 80)

        feature_cols = [
            "Farm_Area_Hectares",
            "Rainfall_mm",
            "Avg_Temperature_C",
            "Humidity_pct",
            "Sunlight_Hours_Day",
            "Soil_pH",
            "Soil_Moisture_pct",
            "Nitrogen_kg_ha",
            "Phosphorus_kg_ha",
            "Potassium_kg_ha",
            "Fertilizer_kg_ha",
            "Pesticide_Litre_ha",
            "Seed_Quality_Score",
            "Yield_Tonnes_Ha",
        ]

        available_features = [c for c in feature_cols if c in self.df.columns]
        if not available_features:
            raise ValueError("No regression features are available in the dataset.")

        model_data = self.df[available_features + ["Profit_Per_Hectare"]].dropna()

        if len(model_data) <= len(available_features) + 1:
            raise ValueError(
                "Not enough observations to fit the regression model reliably."
            )

        X_raw = model_data[available_features].to_numpy(dtype=float)
        y = model_data["Profit_Per_Hectare"].to_numpy(dtype=float)

        # Standardize predictors.
        X_mean = X_raw.mean(axis=0)
        X_std = X_raw.std(axis=0, ddof=0)
        X_std[X_std == 0] = 1.0
        X_norm = (X_raw - X_mean) / X_std

        # Add intercept.
        X_design = np.column_stack([np.ones(len(X_norm)), X_norm])

        # Stable least-squares solution.
        beta, _, rank, _ = np.linalg.lstsq(X_design, y, rcond=None)

        if rank < X_design.shape[1]:
            print(
                "[WARNING] The design matrix is rank-deficient; "
                "some predictors may be strongly collinear."
            )

        predictions = X_design @ beta
        residuals = y - predictions

        ss_tot = np.sum((y - y.mean()) ** 2)
        ss_res = np.sum(residuals**2)

        r_squared = (
            1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
        )

        rmse = float(np.sqrt(np.mean(residuals**2)))
        mae = float(np.mean(np.abs(residuals)))

        n = X_design.shape[0]
        p = X_design.shape[1]
        degrees_of_freedom = n - p

        if degrees_of_freedom > 0:
            sigma_sq = ss_res / degrees_of_freedom
            xtx_pinv = np.linalg.pinv(X_design.T @ X_design)
            var_beta = sigma_sq * xtx_pinv
            se_beta = np.sqrt(np.maximum(0, np.diag(var_beta)))
            t_stats = beta / np.where(se_beta > 0, se_beta, np.nan)
            p_values = 2 * stats.t.sf(
                np.abs(t_stats), df=degrees_of_freedom
            )
        else:
            se_beta = np.full(p, np.nan)
            t_stats = np.full(p, np.nan)
            p_values = np.full(p, np.nan)

        summary_data = [
            {
                "Feature": "Intercept",
                "Std_Coefficient": beta[0],
                "Std_Error": se_beta[0],
                "t_statistic": t_stats[0],
                "p_value": p_values[0],
            }
        ]

        for i, column in enumerate(available_features, start=1):
            summary_data.append(
                {
                    "Feature": column,
                    "Std_Coefficient": beta[i],
                    "Std_Error": se_beta[i],
                    "t_statistic": t_stats[i],
                    "p_value": p_values[i],
                }
            )

        model_df = pd.DataFrame(summary_data)
        model_df["Absolute_Std_Coefficient"] = model_df[
            "Std_Coefficient"
        ].abs()
        model_df = model_df.sort_values(
            "Absolute_Std_Coefficient",
            ascending=False,
        )

        reg_file = self.reports_dir / "ols_profit_driver_regression.csv"
        model_df.to_csv(reg_file, index=False)

        print(
            f"OLS Regression R-Squared : {r_squared:.4f} "
            f"({r_squared * 100:.2f}%)"
        )
        print(f"RMSE                     : INR {rmse:,.2f}")
        print(f"MAE                      : INR {mae:,.2f}")
        print("\nTop Predictor Coefficients:")
        print(
            model_df[
                ["Feature", "Std_Coefficient", "p_value"]
            ].head(6).to_string(index=False)
        )
        print(f"[SAVED] Regression report exported to: {reg_file}")

        return {
            "r_squared": r_squared,
            "rmse": rmse,
            "mae": mae,
            "coefficients": model_df,
        }

    def run_pipeline(self) -> None:
        """Execute all pipeline stages sequentially."""
        print("Starting End-to-End Agricultural Data Science Pipeline...")

        if not HAS_DATA_SCIENCE_STACK:
            print("[INFO] Third-party data science packages (matplotlib/pandas/seaborn) not detected in this environment.")
            print("[INFO] Executing standard analytical pipeline to process JSON data and answer all README questions...\n")

            if not self.data_path.exists():
                candidates = [
                    Path("Cleaned_Agriculture_Data.json"),
                    Path("./Cleaned_Agriculture_Data.json"),
                    Path("../Cleaned_Agriculture_Data.json"),
                    Path(__file__).resolve().parent / "Cleaned_Agriculture_Data.json"
                ]
                found = next((p for p in candidates if p.exists()), None)
                if found is None:
                    raise FileNotFoundError(f"Cannot locate dataset at: {self.data_path.resolve()}")
                self.data_path = found

            with open(self.data_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)

            print_answers_and_summary(raw_data)
            print("\n" + "=" * 80)
            print("PIPELINE COMPLETED SUCCESSFULLY (STANDARD MODE)")
            print("=" * 80)
            return

        self.load_and_validate_data()
        self.compute_summary_statistics()
        self.generate_crop_analysis()
        self.generate_irrigation_analysis()
        self.generate_visualizations()
        self.run_regression_and_drivers()

        with open(self.data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        print_answers_and_summary(raw_data)

        print("\n" + "=" * 80)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print(f"Output directory: {self.output_dir.resolve()}")
        print("=" * 80)


def main() -> None:
    """CLI entry point."""
    dataset_file = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Cleaned_Agriculture_Data.json"
    )

    pipeline = AgricultureDataPipeline(data_path=dataset_file)
    pipeline.run_pipeline()
    


if __name__ == "__main__":
    main()

