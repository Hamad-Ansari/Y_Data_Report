import streamlit as st
import pandas as pd
import requests
import time
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Data Profiler Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for green theme and animations
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        background: linear-gradient(90deg, #2E8B57, #3CB371);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 2s ease-in;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #228B22;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #2E8B57, #32CD32);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(46, 139, 87, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(46, 139, 87, 0.5);
        background: linear-gradient(135deg, #228B22, #2E8B57);
    }
    
    .dataset-card {
        background: linear-gradient(135deg, #F8FFF8, #E8F5E8);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #2E8B57;
        box-shadow: 0 4px 15px 0 rgba(46, 139, 87, 0.1);
        transition: all 0.3s ease;
    }
    
    .dataset-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px 0 rgba(46, 139, 87, 0.2);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .success-message {
        background: linear-gradient(135deg, #90EE90, #98FB98);
        color: #006400;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #32CD32;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #FFB6C1, #FF69B4);
        color: #8B0000;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #DC143C;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def load_titanic_data():
    """Load Titanic dataset"""
    try:
        # Using direct URL to avoid dependencies
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading Titanic data: {str(e)}")
        # Create sample data as fallback
        return pd.DataFrame({
            'Survived': [0, 1, 1, 1, 0],
            'Pclass': [3, 1, 3, 1, 3],
            'Sex': ['male', 'female', 'female', 'female', 'male'],
            'Age': [22.0, 38.0, 26.0, 35.0, 35.0],
            'Fare': [7.2500, 71.2833, 7.9250, 53.1000, 8.0500]
        })

def load_iris_data():
    """Load Iris dataset"""
    try:
        url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading Iris data: {str(e)}")
        # Create sample data as fallback
        return pd.DataFrame({
            'sepal_length': [5.1, 4.9, 4.7, 4.6, 5.0],
            'sepal_width': [3.5, 3.0, 3.2, 3.1, 3.6],
            'petal_length': [1.4, 1.4, 1.3, 1.5, 1.4],
            'petal_width': [0.2, 0.2, 0.2, 0.2, 0.2],
            'species': ['setosa', 'setosa', 'setosa', 'setosa', 'setosa']
        })

def create_profiling_report(df, title):
    """Create yData profiling report with updated parameters"""
    try:
        from ydata_profiling import ProfileReport
        
        # Updated parameters for newer version of ydata-profiling
        profile = ProfileReport(
            df,
            title=title,
            explorative=True,
            minimal=False,  # Use comprehensive report
            progress_bar=False  # Disable progress bar in report generation
        )
        return profile
    except ImportError:
        st.error("ydata-profiling not installed. Run: pip install ydata-profiling")
        return None
    except Exception as e:
        st.error(f"Error creating profile report: {str(e)}")
        return None

def st_profile_report(profile):
    """Display profile report in Streamlit"""
    try:
        profile_html = profile.to_html()
        components.html(profile_html, height=800, scrolling=True)
    except Exception as e:
        st.error(f"Error displaying profile report: {str(e)}")
        st.warning("Please download the full report using the download button below.")

def display_basic_analysis(df, title):
    """Display basic data analysis when full profiling fails"""
    st.markdown(f"## 📊 Basic Analysis: {title}")
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rows", df.shape[0])
    with col2:
        st.metric("Total Columns", df.shape[1])
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())
    with col4:
        st.metric("Duplicate Rows", df.duplicated().sum())
    
    # Data preview
    st.subheader("Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Data types
    st.subheader("Data Types")
    st.write(df.dtypes)
    
    # Basic statistics
    st.subheader("Basic Statistics")
    st.write(df.describe())
    
    # Missing values
    st.subheader("Missing Values")
    missing_data = df.isnull().sum()
    if missing_data.sum() > 0:
        st.write(missing_data[missing_data > 0])
    else:
        st.write("No missing values found!")

def main():
    # Header section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-header">📊 Data Profiler Pro</h1>', unsafe_allow_html=True)
        st.markdown("### *Advanced Data Analysis with yData Profiling*")
    
    # Try to load animation
    try:
        calibration_animation = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_Stt1R6.json")
        if calibration_animation:
            from streamlit_lottie import st_lottie
            st_lottie(calibration_animation, height=150, key="calibration")
    except:
        pass
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        st.markdown("---")
        
        dataset_choice = st.radio(
            "Select Dataset:",
            ["Titanic", "Iris", "Upload Your Own"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Report Settings")
        
        report_mode = st.radio(
            "Report Mode:",
            ["Complete", "Minimal"],
            help="Complete: Full detailed report. Minimal: Faster basic report."
        )
        
        st.markdown("---")
        st.markdown("### 📈 About")
        st.markdown("""
        This app provides comprehensive data profiling using yData Profiling library.
        
        **Features:**
        - Automated data quality assessment
        - Interactive visualizations
        - Statistical summaries
        - Correlation analysis
        - Missing values analysis
        """)
    
    # Main content area
    if dataset_choice == "Upload Your Own":
        st.markdown('<div class="sub-header">📤 Upload Your Dataset</div>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload your dataset in CSV format"
        )
        
        if uploaded_file is not None:
            try:
                with st.spinner('📥 Loading your data...'):
                    df = pd.read_csv(uploaded_file)
                
                st.markdown(f'<div class="success-message">✅ Successfully loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns</div>', unsafe_allow_html=True)
                
                # Data preview
                with st.expander("🔍 Data Preview", expanded=True):
                    st.dataframe(df.head(), use_container_width=True)
                
                # Generate report
                if st.button("🚀 Generate Profiling Report", key="generate_custom"):
                    with st.spinner('🔬 Creating comprehensive profile report...'):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        profile = create_profiling_report(df, "Custom Dataset Profiling Report")
                        if profile:
                            st.markdown('<div class="success-message">📊 Profile Report Generated Successfully!</div>', unsafe_allow_html=True)
                            st_profile_report(profile)
                            
                            # Download option
                            st.markdown("---")
                            st.markdown("### 💾 Download Report")
                            profile_html = profile.to_html()
                            
                            st.download_button(
                                label="📥 Download HTML Report",
                                data=profile_html,
                                file_name="custom_dataset_profile_report.html",
                                mime="text/html"
                            )
                        else:
                            st.markdown('<div class="error-message">⚠️ Falling back to Basic Analysis</div>', unsafe_allow_html=True)
                            display_basic_analysis(df, "Custom Dataset")
            
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
    
    else:
        # Dataset selection and description
        if dataset_choice == "Titanic":
            st.markdown('<div class="sub-header">🚢 Titanic Dataset Analysis</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                <div class="dataset-card">
                <h3>About the Titanic Dataset</h3>
                <p>The Titanic dataset contains information about passengers aboard the RMS Titanic, 
                including survival status, passenger class, age, gender, and more. This dataset is 
                commonly used for predictive modeling and data analysis exercises.</p>
                <p><strong>Key Features:</strong> Survival, Pclass, Sex, Age, Fare, Embarked</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Titanic animation
                titanic_animation = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_kUZwfP.json")
                if titanic_animation:
                    try:
                        from streamlit_lottie import st_lottie
                        st_lottie(titanic_animation, height=150, key="titanic")
                    except:
                        pass
            
            # Load data with loading animation
            with st.spinner('🛳️ Loading Titanic dataset...'):
                df = load_titanic_data()
            
        else:  # Iris dataset
            st.markdown('<div class="sub-header">🌺 Iris Dataset Analysis</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                <div class="dataset-card">
                <h3>About the Iris Dataset</h3>
                <p>The Iris flower dataset is a multivariate dataset introduced by Ronald Fisher. 
                It contains measurements of iris flowers from three different species, making it 
                perfect for classification and clustering analysis.</p>
                <p><strong>Key Features:</strong> Sepal length, Sepal width, Petal length, Petal width, Species</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Flower animation
                flower_animation = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_sk5h1kfn.json")
                if flower_animation:
                    try:
                        from streamlit_lottie import st_lottie
                        st_lottie(flower_animation, height=150, key="flower")
                    except:
                        pass
            
            # Load data with loading animation
            with st.spinner('🌸 Loading Iris dataset...'):
                df = load_iris_data()
        
        # Show dataset info
        st.markdown(f'<div class="success-message">✅ Successfully loaded {dataset_choice} dataset with {df.shape[0]} rows and {df.shape[1]} columns</div>', unsafe_allow_html=True)
        
        # Data preview section
        with st.expander("🔍 Quick Data Preview", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Rows", df.shape[0])
            with col2:
                st.metric("Total Columns", df.shape[1])
            with col3:
                st.metric("Missing Values", df.isnull().sum().sum())
            
            st.dataframe(df.head(10), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Data Types:**")
                st.write(df.dtypes)
            with col2:
                st.write("**Basic Statistics:**")
                st.write(df.describe())
        
        # Generate profiling report
        st.markdown("---")
        st.markdown('<div class="sub-header">📈 Generate Comprehensive Profile Report</div>', unsafe_allow_html=True)
        
        if st.button(f"🚀 Generate {dataset_choice} Profiling Report", key=f"generate_{dataset_choice}"):
            with st.spinner('🔬 Creating comprehensive profile report...'):
                # Progress animation
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    status_text.text(f"Processing... {i+1}%")
                    time.sleep(0.01)
                
                status_text.text("Finalizing report...")
                
                # Create profile report
                profile = create_profiling_report(df, f"{dataset_choice} Dataset Profiling Report")
                
                if profile:
                    st.markdown('<div class="success-message">🎉 Profile Report Generated Successfully!</div>', unsafe_allow_html=True)
                    st.balloons()
                    
                    # Display the report
                    st_profile_report(profile)
                    
                    # Download option
                    st.markdown("---")
                    st.markdown("### 💾 Download Report")
                    
                    # Convert to HTML for download
                    profile_html = profile.to_html()
                    
                    st.download_button(
                        label="📥 Download HTML Report",
                        data=profile_html,
                        file_name=f"{dataset_choice.lower()}_profile_report.html",
                        mime="text/html"
                    )
                else:
                    st.markdown('<div class="error-message">⚠️ Advanced profiling failed. Showing Basic Analysis instead.</div>', unsafe_allow_html=True)
                    display_basic_analysis(df, dataset_choice)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #2E8B57;'>
            <p>Made with ❤️(Hammad_Zahid) using Streamlit & yData Profiling</p>
            <p>Professional Data Analysis Tool</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()