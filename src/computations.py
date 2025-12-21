"""
Computation functions for MRIO emissions decomposition analysis.
"""
import pandas as pd


def compute_direct_domestic_foreign(
    S: pd.DataFrame,
    L: pd.DataFrame,
    stressor: str,
    region: str,
    sector: str,
    domestic_indirect_definition: str = "minus_direct",
):
    """
    Compute a 3-part decomposition for target j=(region, sector) and chosen stressor.
    """
    col_key = (region, sector)

    if stressor not in S.index:
        raise KeyError(f"Stressor not found: {stressor}")

    if col_key not in L.columns:
        raise KeyError(f"Target sector not found in L.columns: {col_key}")

    # 1) Intensity vector s (index = producers)
    s_row = S.loc[stressor]
    s_aligned = s_row.reindex(L.index)
    if s_aligned.isna().any():
        missing = s_aligned[s_aligned.isna()].index[:10].tolist()
        raise ValueError(f"S -> L alignment produced NaNs. First missing producers: {missing}")

    # 2) Requirement column from Leontief inverse
    L_col = L[col_key]  # indexed by producers

    # 3) Contribution vector r_col = s ⊙ L_col
    r_col = s_aligned * L_col

    # 4) Split
    direct = float(s_aligned.loc[col_key])

    producer_regions = r_col.index.get_level_values("region")
    domestic_mask = (producer_regions == region)

    domestic_total = float(r_col[domestic_mask].sum())
    foreign_total  = float(r_col[~domestic_mask].sum())

    if domestic_indirect_definition == "minus_direct":
        domestic_indirect = domestic_total - direct
    elif domestic_indirect_definition == "exclude_diagonal":
        domestic_indirect = domestic_total - float(r_col.loc[col_key])
    else:
        raise ValueError("domestic_indirect_definition must be 'minus_direct' or 'exclude_diagonal'")

    foreign_indirect = foreign_total
    total = direct + domestic_indirect + foreign_indirect

    return {
        "stressor": stressor,
        "col_key": col_key,
        "direct": direct,
        "domestic_indirect": domestic_indirect,
        "foreign_indirect": foreign_indirect,
        "total": total,
        "r_column": r_col,
        "domestic_indirect_definition": domestic_indirect_definition,
    }

