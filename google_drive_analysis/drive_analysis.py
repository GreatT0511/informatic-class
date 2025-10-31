"""
Google Drive data analysis workflow for Google Colab.

This script mounts Google Drive, loads a tabular dataset into a pandas DataFrame,
computes descriptive statistics, and visualises the distribution with a histogram
and a box plot.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt


def mount_google_drive(mount_point: str = "/content/drive") -> None:
    """Mount Google Drive when running inside Google Colab."""
    try:
        from google.colab import drive  # type: ignore
    except ImportError:
        print("google.colab is not available; skipping drive.mount().")
        return

    if Path(mount_point).exists():
        print(f"Mounting Google Drive at {mount_point}...")
        drive.mount(mount_point)
    else:
        print(
            f"Mount point {mount_point} does not exist. "
            "Create the directory first or adjust the path."
        )


def load_dataframe(data_path: Path, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a pandas DataFrame.

    Parameters
    ----------
    data_path : Path
        Absolute path to the dataset inside Google Drive.
    sheet_name : Optional[str]
        Sheet name when reading Excel files. Ignored for CSV input.
    """
    if data_path.suffix.lower() in {".xls", ".xlsx"}:
        return pd.read_excel(data_path, sheet_name=sheet_name)
    return pd.read_csv(data_path)


def analyse_dataframe(df: pd.DataFrame, column: str, output_dir: Path) -> None:
    """
    Generate descriptive statistics and distribution plots for a target column.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    column : str
        Column to analyse.
    output_dir : Path
        Directory where plots and summaries will be saved.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = df[column].describe()
    mode = df[column].mode().iloc[0] if not df[column].mode().empty else None

    summary_path = output_dir / "summary_statistics.txt"
    with summary_path.open("w", encoding="utf-8") as fh:
        fh.write("Summary statistics\n")
        fh.write(summary.to_string())
        fh.write("\n\n")
        fh.write(f"Mode: {mode}\n")

    plt.figure(figsize=(8, 5))
    df[column].hist(bins=20, edgecolor="black")
    plt.title(f"Histogram of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_dir / "histogram.png")
    plt.close()

    plt.figure(figsize=(6, 5))
    df.boxplot(column=column)
    plt.title(f"Box plot of {column}")
    plt.ylabel(column)
    plt.tight_layout()
    plt.savefig(output_dir / "boxplot.png")
    plt.close()

    print(f"Summary saved to {summary_path}")
    print(f"Histogram saved to {output_dir / 'histogram.png'}")
    print(f"Box plot saved to {output_dir / 'boxplot.png'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyse a dataset stored on Google Drive."
    )
    parser.add_argument(
        "--data-path",
        required=True,
        help="Absolute path to the dataset (e.g. /content/drive/MyDrive/data.csv)",
    )
    parser.add_argument(
        "--column",
        required=True,
        help="Column name to analyse.",
    )
    parser.add_argument(
        "--sheet",
        help="Sheet name when loading from an Excel file.",
    )
    parser.add_argument(
        "--output-dir",
        default="analysis_results",
        help="Directory to store plots and summary text.",
    )
    parser.add_argument(
        "--skip-mount",
        action="store_true",
        help="Skip drive.mount() call (useful when not running in Colab).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.skip_mount:
        mount_google_drive()

    data_path = Path(args.data_path)
    if not data_path.exists():
        print(
            f"Warning: {data_path} does not exist on this environment. "
            "Confirm the path when running in Google Colab."
        )

    df = load_dataframe(data_path, sheet_name=args.sheet)
    analyse_dataframe(df, args.column, Path(args.output_dir))


if __name__ == "__main__":
    main()
