"""
UI components for the Streamlit app.
"""
import streamlit as st


def show_welcome_message(catalog: dict):
    """
    Display the welcome message and instructions when no chart is generated.
    
    Args:
        catalog: Dictionary containing regions, sectors, and stressors lists
    """
    # Main welcome text
    st.markdown("""
    ## Welcome! 👋
    
    This tool helps you analyze **emissions decomposition** using Multi-Regional Input-Output (MRIO) data.
    
    ### How to use:
    1. **Select parameters** from the sidebar on the left:
       - Choose a **region** (e.g., US, CN, EU)
       - Select a **sector** (e.g., Construction, Manufacturing)
       - Pick a **stressor** (e.g., CO2 emissions, Water use)
    
    2. **Click "Generate Pie Chart"** to visualize the decomposition
    
    3. **Interpret the results**:
       - **Direct**: On-site emissions intensity of the selected sector
       - **Domestic Indirect**: Emissions from domestic supply chain
       - **Foreign Indirect**: Emissions from international supply chain
    
    ### Data Coverage:
    - 📊 **{regions}** regions
    - 🏭 **{sectors}** sectors  
    - 💨 **{stressors}** stressors
    
    ---
    
    """.format(
        regions=len(catalog["regions"]),
        sectors=len(catalog["sectors"]),
        stressors=len(catalog["stressors"])
    ))
    
    # Quick stats section
    st.markdown("### 💡 Quick Stats")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Available Regions", len(catalog["regions"]))
    with col2:
        st.metric("Available Sectors", len(catalog["sectors"]))
    with col3:
        st.metric("Available Stressors", len(catalog["stressors"]))
    
    st.markdown("---")
    
    # Example selections
    st.markdown("### 📌 Example Selections")
    st.markdown("""
    Try these interesting combinations:
    - **US Construction + CO2**: See carbon footprint of US construction sector
    - **CN Manufacturing + Water**: Analyze water use in Chinese manufacturing
    - **EU Agriculture + Methane**: Explore methane emissions from EU agriculture
    """)


def show_footer():
    """Display the application footer."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #7F8C8D;'>
            <small>MRIO Emissions Decomposition Analysis Tool | December 2025</small>
        </div>
        """,
        unsafe_allow_html=True
    )

