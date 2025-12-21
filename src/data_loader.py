"""
Data loading and catalog building functions for MRIO analysis.
"""
import pandas as pd


def load_S_L(path_S: str, path_L: str) -> tuple:
    """
    Load:
      S: rows = stressors, columns = MultiIndex(region, sector)
      L: rows/cols = MultiIndex(region, sector)

    Returns (S, L) with named MultiIndex levels.
    """
    S = pd.read_csv(path_S, header=[0, 1], index_col=0)
    L = pd.read_csv(path_L, header=[0, 1], index_col=[0, 1])

    # Force consistent MultiIndex naming
    S.columns = pd.MultiIndex.from_tuples(S.columns, names=["region", "sector"])
    L.index   = pd.MultiIndex.from_tuples(L.index,   names=["region", "sector"])
    L.columns = pd.MultiIndex.from_tuples(L.columns, names=["region", "sector"])

    # Sanity checks
    if not L.index.equals(L.columns):
        raise ValueError("L must be square with identical row/column MultiIndex ordering.")
    if not S.columns.equals(L.columns):
        # We need S columns aligned to L columns for correct multiplication
        S = S.reindex(columns=L.columns)
        if S.isna().any().any():
            raise ValueError("After aligning S to L.columns, NaNs appeared. Check your CSV exports.")

    return S, L


def build_catalog(S: pd.DataFrame) -> dict:
    """
    Extract unique stressors, regions, sectors from S without touching numeric values meaningfully.
    """
    stressors = S.index.astype(str).unique().tolist()
    regions   = S.columns.get_level_values("region").astype(str).unique().tolist()
    sectors   = S.columns.get_level_values("sector").astype(str).unique().tolist()

    stressors.sort()
    regions.sort()
    sectors.sort()

    return {"stressors": stressors, "regions": regions, "sectors": sectors}

