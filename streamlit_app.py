import streamlit as st
import matplotlib.pyplot as plt
import os

# Import custom modules
from src.data_loader import load_S_L, build_catalog
from src.computations import compute_direct_domestic_foreign
from src.visualization import create_enhanced_donut, fmt_kg, percent
from src.ui_components import show_welcome_message, show_footer

# Data paths
base_data_path = "./data/2022"
path_S = f"{base_data_path}/S_2022_all_.csv"
path_L = f"{base_data_path}/L_2022.csv"

# Page configuration
st.set_page_config(
    page_title="MRIO Emissions Decomposition",
    page_icon="🌍",
    layout="wide"
)

# Title
st.title("🌍 MRIO Emissions Decomposition Analysis")
st.markdown("### Visualize direct and indirect emissions by region, sector, and stressor")

# -----------------------------
# Cached Data Loading Functions
# -----------------------------
@st.cache_data
def load_data_cached(path_S: str, path_L: str):
    """Cached wrapper for data loading."""
    return load_S_L(path_S, path_L)


@st.cache_data
def build_catalog_cached(S):
    """Cached wrapper for catalog building."""
    return build_catalog(S)


# Check if data files exist
if not os.path.exists(path_S) or not os.path.exists(path_L):
    st.error(f"⚠️ Data files not found! Please ensure the following files exist:\n- {path_S}\n- {path_L}")
    st.stop()

# Load data
with st.spinner("Loading data..."):
    try:
        S, L = load_data_cached(path_S, path_L)
        catalog = build_catalog_cached(S)
        st.success(f"✅ Data loaded successfully! ({len(catalog['regions'])} regions, {len(catalog['sectors'])} sectors, {len(catalog['stressors'])} stressors)")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Sidebar for parameters
with st.sidebar:
    st.header("📋 Parameters")
    st.markdown("Select the region, sector, and stressor to analyze emissions decomposition.")
    st.markdown("---")
    
    selected_region = st.selectbox(
        "🌍 Region",
        options=catalog["regions"],
        index=catalog["regions"].index("US") if "US" in catalog["regions"] else 0
    )
    
    selected_sector = st.selectbox(
        "🏭 Sector",
        options=catalog["sectors"],
        index=catalog["sectors"].index("Construction (45)") if "Construction (45)" in catalog["sectors"] else 0
    )
    
    selected_stressor = st.selectbox(
        "💨 Stressor",
        options=catalog["stressors"],
        index=catalog["stressors"].index("CO2 - combustion - air") if "CO2 - combustion - air" in catalog["stressors"] else 0
    )
    
    st.markdown("---")
    st.subheader("⚙️ Advanced Options")
    indirect_definition = st.radio(
        "Domestic Indirect Definition",
        options=["minus_direct", "exclude_diagonal"],
        index=0,
        help="""
        - **minus_direct**: Domestic indirect = domestic total - direct (includes self-indirect)
        - **exclude_diagonal**: Excludes entire diagonal contribution from domestic indirect
        """
    )
    
    st.markdown("---")
    generate_button = st.button("📊 Generate Pie Chart", type="primary", use_container_width=True)

# Main section for results
if generate_button:
    with st.spinner("Computing emissions decomposition..."):
        try:
            # Compute decomposition
            result = compute_direct_domestic_foreign(
                S=S,
                L=L,
                stressor=selected_stressor,
                region=selected_region,
                sector=selected_sector,
                domestic_indirect_definition=indirect_definition
            )
            
            # Display results
            st.subheader("📈 Emissions Decomposition Results")
            
            # Show current selection
            st.info(f"**Region:** {selected_region} | **Sector:** {selected_sector} | **Stressor:** {selected_stressor}")
            
            # Create and display the chart
            fig = create_enhanced_donut(
                direct=result["direct"],
                domestic_indirect=result["domestic_indirect"],
                foreign_indirect=result["foreign_indirect"],
                country=selected_region,
                sector_name=selected_sector,
                stressor=selected_stressor,
                unit_label="per 1 M€ final demand"
            )
            
            st.pyplot(fig)
            plt.close(fig)
            
        except Exception as e:
            st.error(f"❌ Error computing emissions: {str(e)}")
else:
    # Show welcome message and instructions
    show_welcome_message(catalog)

# Footer
show_footer()

