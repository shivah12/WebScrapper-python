import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scraper import extract_data
from utils import download_csv, download_chart_as_image

# Page configuration
st.set_page_config(
    page_title="Data Scraper",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, minimal CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2rem;
        font-weight: 600;
        color: #1e293b;
        text-align: center;
        margin: 1rem 0 2rem 0;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    .section-title {
        font-size: 1.25rem;
        font-weight: 500;
        color: #334155;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .metric-box {
        background: #ffffff;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        margin-top: 0.25rem;
    }
    .stButton > button {
        width: 100%;
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background: #2563eb;
    }
    .info-box {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    
    /* Position alerts in bottom right corner */
    .stAlert {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        top: auto !important;
        left: auto !important;
        width: 350px !important;
        z-index: 1000 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* Success alert styling */
    .stAlert[data-baseweb="notification"] {
        background: #ecfdf5 !important;
        border: 1px solid #10b981 !important;
        color: #065f46 !important;
    }
    
    /* Error alert styling */
    .stAlert[data-baseweb="notification"][data-testid="stAlert"] {
        background: #fef2f2 !important;
        border: 1px solid #ef4444 !important;
        color: #991b1b !important;
    }
    
    /* Warning alert styling */
    .stAlert[data-baseweb="notification"] {
        background: #fffbeb !important;
        border: 1px solid #f59e0b !important;
        color: #92400e !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
# st.markdown('<h1 class="main-title">Data Scraper</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Input Parameters")
    st.markdown("---")
    
    url = st.text_input(
        "Website URL",
        placeholder="https://example.com",
        help="Enter the URL to scrape"
    )
    
    option = st.selectbox(
        "Extraction Method",
        ["All Tables", "Headings", "Specific Row/Column"],
        help="Select data extraction method"
    )
    
    st.markdown("---")
    
    if st.button("Extract Data", type="primary"):
        st.session_state['extract_clicked'] = True

# Main content
if 'extract_clicked' in st.session_state and st.session_state['extract_clicked']:
    if not url:
        st.error("Please enter a URL")
    else:
        with st.spinner("Extracting data..."):
            try:
                df = extract_data(url, option)
                st.session_state['scraped_df'] = df
                st.session_state['extract_clicked'] = False
                st.success("Data extracted successfully")
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state['extract_clicked'] = False

# Display results
if 'scraped_df' in st.session_state:
    df = st.session_state['scraped_df']
    
    if isinstance(df, pd.DataFrame) and not df.empty:
        # Statistics overview
        st.markdown('<h2 class="section-title">Data Overview</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{len(df)}</div>
                <div class="metric-label">Total Rows</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{len(df.columns)}</div>
                <div class="metric-label">Total Columns</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            numeric_cols = df.select_dtypes(include=["float64", "int64", "int32"]).columns.tolist()
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{len(numeric_cols)}</div>
                <div class="metric-label">Numeric Columns</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            missing_total = df.isnull().sum().sum()
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{missing_total}</div>
                <div class="metric-label">Missing Values</div>
            </div>
            """, unsafe_allow_html=True)

        # Data display
        st.markdown('<h2 class="section-title">Extracted Data</h2>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Data Table", "Data Summary"])
        
        with tab1:
            st.dataframe(df, use_container_width=True, height=400)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Column Information**")
                st.dataframe(df.info(), use_container_width=True)
            with col2:
                st.write("**Missing Values**")
                missing_df = pd.DataFrame({
                    'Column': df.columns,
                    'Missing Count': df.isnull().sum(),
                    'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
                })
                st.dataframe(missing_df, use_container_width=True)

        # Download section
        st.markdown('<h2 class="section-title">Export Data</h2>', unsafe_allow_html=True)
        download_csv(df)

        # Visualization
        if len(numeric_cols) >= 1:
            st.markdown('<h2 class="section-title">Data Visualization</h2>', unsafe_allow_html=True)
            
            # Chart configuration section
            st.markdown("""
            <div class="info-box">
                <strong>Chart Configuration</strong> - Select chart type and axes to visualize your data
            </div>
            """, unsafe_allow_html=True)
            
            # Chart controls in a clean layout
            chart_col1, chart_col2, chart_col3, chart_col4 = st.columns(4)
            
            with chart_col1:
                chart_type = st.selectbox(
                    "Chart Type",
                    ["Bar Chart", "Line Chart", "Scatter Plot"],
                    help="Choose the type of chart to display"
                )
            
            with chart_col2:
                x_axis = st.selectbox(
                    "X-Axis",
                    df.columns,
                    help="Select the column for X-axis"
                )
            
            with chart_col3:
                y_axis = st.selectbox(
                    "Y-Axis",
                    numeric_cols,
                    help="Select the numeric column for Y-axis"
                )
            
            with chart_col4:
                # Chart size selector
                chart_size = st.selectbox(
                    "Chart Size",
                    ["Medium", "Large", "Extra Large"],
                    help="Select chart display size"
                )

            # Create chart with improved spacing
            if x_axis and y_axis:
                try:
                    # Determine figure size based on selection
                    size_map = {
                        "Medium": (10, 6),
                        "Large": (12, 8),
                        "Extra Large": (14, 10)
                    }
                    fig_width, fig_height = size_map[chart_size]
                    
                    # Create figure with better styling
                    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                    
                    # Data preparation
                    x_data = df[x_axis].astype(str) if df[x_axis].dtype == 'object' else df[x_axis]
                    y_data = pd.to_numeric(df[y_axis], errors='coerce')
                    
                    # Remove NaN values
                    valid_indices = ~y_data.isna()
                    x_data = x_data[valid_indices]
                    y_data = y_data[valid_indices]
                    
                    if len(x_data) > 0:
                        # Color schemes for different chart types
                        colors = {
                            "Bar Chart": "#3b82f6",
                            "Line Chart": "#ef4444", 
                            "Scatter Plot": "#10b981"
                        }
                        
                        if chart_type == "Bar Chart":
                            bars = ax.bar(range(len(x_data)), y_data, 
                                        color=colors[chart_type], alpha=0.8, 
                                        edgecolor='#1e40af', linewidth=0.5)
                            
                            # Add value labels on bars if not too many
                            if len(x_data) <= 20:
                                for i, bar in enumerate(bars):
                                    height = bar.get_height()
                                    ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                                           f'{height:,.0f}', ha='center', va='bottom', fontsize=8)
                            
                            ax.set_xticks(range(len(x_data)))
                            ax.set_xticklabels(x_data, rotation=45, ha='right', fontsize=10)
                            
                        elif chart_type == "Line Chart":
                            line = ax.plot(range(len(x_data)), y_data, 
                                         marker='o', linestyle='-', 
                                         color=colors[chart_type], linewidth=3, 
                                         markersize=6, markerfacecolor='white',
                                         markeredgecolor=colors[chart_type], markeredgewidth=2)
                            
                            ax.set_xticks(range(len(x_data)))
                            ax.set_xticklabels(x_data, rotation=45, ha='right', fontsize=10)
                            
                        elif chart_type == "Scatter Plot":
                            scatter = ax.scatter(range(len(x_data)), y_data, 
                                               color=colors[chart_type], s=80, alpha=0.7,
                                               edgecolors='white', linewidth=1)
                            
                            ax.set_xticks(range(len(x_data)))
                            ax.set_xticklabels(x_data, rotation=45, ha='right', fontsize=10)

                        # Enhanced chart styling
                        ax.set_title(f"{chart_type}: {y_axis} vs {x_axis}", 
                                   fontsize=16, fontweight=600, pad=20, color='#1e293b')
                        ax.set_xlabel(x_axis, fontsize=12, fontweight=500, color='#374151', labelpad=10)
                        ax.set_ylabel(y_axis, fontsize=12, fontweight=500, color='#374151', labelpad=10)
                        
                        # Improved grid
                        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
                        ax.set_axisbelow(True)  # Put grid behind data
                        
                        # Style the spines
                        for spine in ax.spines.values():
                            spine.set_color('#d1d5db')
                            spine.set_linewidth(0.5)
                        
                        # Set background color
                        ax.set_facecolor('#f9fafb')
                        fig.patch.set_facecolor('white')
                        
                        # Adjust layout with more padding
                        plt.tight_layout(pad=2.0)
                        
                        # Display chart with spacing
                        st.markdown("### Chart Display")
                        st.pyplot(fig, use_container_width=True)
                        
                        # Chart information
                        st.markdown(f"""
                        <div class="info-box">
                            <strong>Chart Information:</strong> Displaying {len(x_data)} data points from {x_axis} vs {y_axis}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Chart download section
                        st.markdown("### Export Chart")
                        download_chart_as_image(fig)
                        
                    else:
                        st.warning("No valid numeric data found for visualization")
                        
                except Exception as e:
                    st.error(f"Chart creation error: {e}")
        else:
            st.markdown("""
            <div class="info-box">
                <strong>No numeric columns found.</strong> Visualization requires numeric data.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No data extracted")
