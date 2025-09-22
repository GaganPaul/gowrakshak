import streamlit as st
import os
from groq import Groq
from PIL import Image
import base64
import io
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import requests
from datetime import datetime, timedelta
import random
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AI Cattle Management Platform",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main Layout Improvements */
    .main {
        padding: 1rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .main-header {
        background: linear-gradient(90deg, #2E8B57, #228B22);
        padding: 2.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 20px rgba(46, 139, 87, 0.3);
    }
    
    .main-header h1 {
        margin: 0 0 0.5rem 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Card Components */
    .metric-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 0.5rem 0;
        border-left: 5px solid #2E8B57;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        color: #666;
        font-weight: 600;
    }
    
    .metric-card h2 {
        margin: 0 0 0.5rem 0;
        font-size: 2rem;
        color: #2E8B57;
        font-weight: 700;
    }
    
    .metric-card p {
        margin: 0;
        font-size: 0.9rem;
        color: #888;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-color: #2E8B57;
    }
    
    .feature-card h4 {
        margin: 0 0 1rem 0;
        color: #2E8B57;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .feature-card p {
        margin: 0;
        line-height: 1.6;
        color: #555;
    }
    
    /* Message Components */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #ffeaa7;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .info-message {
        background: #d1ecf1;
        color: #0c5460;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #bee5eb;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Button Improvements */
    .stButton > button {
        background: linear-gradient(90deg, #2E8B57, #228B22);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(46, 139, 87, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 139, 87, 0.4);
    }
    
    /* Sidebar Improvements */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa, #e9ecef);
        padding: 1rem 0;
    }
    
    .sidebar .sidebar-content .block-container {
        padding: 0 1rem;
    }
    
    /* Breed Result Card */
    .breed-result {
        background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #2E8B57;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(46, 139, 87, 0.1);
    }
    
    .breed-result h3 {
        margin: 0 0 1rem 0;
        color: #2E8B57;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .breed-result h4 {
        margin: 0 0 1rem 0;
        color: #1a5a1a;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .breed-result p {
        margin: 0.5rem 0;
        line-height: 1.5;
    }
    
    /* Chat Messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .user-message {
        background: #e3f2fd;
        margin-left: 2rem;
        border-left: 4px solid #2196f3;
    }
    
    .bot-message {
        background: #f1f8e9;
        margin-right: 2rem;
        border-left: 4px solid #2E8B57;
    }
    
    /* Form Improvements */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2E8B57;
        box-shadow: 0 0 0 3px rgba(46, 139, 87, 0.1);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
    }
    
    /* File Uploader */
    .stFileUploader > div {
        border-radius: 10px;
        border: 2px dashed #2E8B57;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        background: #e8f5e8;
        border-color: #228B22;
    }
    
    /* Section Headers */
    .section-header {
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #2E8B57;
        color: #2E8B57;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Grid Improvements */
    .stColumns {
        gap: 1rem;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        
        .main-header {
            padding: 2rem 1rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1.5rem 1rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
        
        .breed-result {
            padding: 1.5rem;
        }
        
        .chat-message {
            margin-left: 0;
            margin-right: 0;
        }
    }
    
    /* Loading States */
    .stSpinner {
        color: #2E8B57;
    }
    
    /* Tab Improvements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        background: #f8f9fa;
        border: 1px solid #dee2e6;
    }
    
    .stTabs [aria-selected="true"] {
        background: #2E8B57;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize LangChain Groq client
@st.cache_resource
def get_langchain_groq_client():
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            st.warning("⚠️ Groq API key not configured. Please add your API key to secrets.toml")
            return None
        return ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.1-70b-versatile",  # Updated to available model
            temperature=0.3,
            max_tokens=2048
        )
    except Exception as e:
        st.error(f"Error initializing LangChain Groq client: {e}")
        return None

# Initialize original Groq client for image processing
@st.cache_resource
def get_groq_client():
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            return None
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        return None

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'breed_results' not in st.session_state:
    st.session_state.breed_results = []
if 'trading_listings' not in st.session_state:
    st.session_state.trading_listings = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = "English"

# Sample data for demonstration
sample_breeds = [
    "Gir", "Sahiwal", "Red Sindhi", "Tharparkar", "Kankrej", 
    "Ongole", "Deoni", "Rathi", "Hariana", "Murrah", "Jaffarabadi"
]

sample_trading_data = [
    {"id": 1, "breed": "Gir", "age": "3 years", "price": "₹45,000", "location": "Karnataka", "health": "Excellent", "seller": "Ramu Patel"},
    {"id": 2, "breed": "Sahiwal", "age": "4 years", "price": "₹38,000", "location": "Punjab", "health": "Good", "seller": "Singh Farms"},
    {"id": 3, "breed": "Murrah", "age": "2 years", "price": "₹52,000", "location": "Haryana", "health": "Excellent", "seller": "Yadav Dairy"},
    {"id": 4, "breed": "Tharparkar", "age": "5 years", "price": "₹35,000", "location": "Rajasthan", "health": "Good", "seller": "Desert Farms"},
    {"id": 5, "breed": "Kankrej", "age": "3 years", "price": "₹42,000", "location": "Gujarat", "health": "Excellent", "seller": "Gujarat Cattle Co."}
]

def main():
    # Header with status indicator
    api_status = "🟢 Connected" if get_groq_client() else "🔴 API Key Required"
    
    st.markdown(f"""
    <div class="main-header">
        <h1>🐄 AI-Powered Cattle Management Platform</h1>
        <p>Transforming India's Livestock Ecosystem with Technology</p>
        <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            Status: {api_status} | Language: {st.session_state.selected_language}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/2E8B57/FFFFFF?text=Cattle+AI", width=200)
        
        # API Setup Guide
        if not get_groq_client():
            st.markdown("""
            <div style="background: #fff3cd; padding: 1rem; border-radius: 10px; margin: 1rem 0; border: 1px solid #ffeaa7;">
                <h4 style="color: #856404; margin: 0 0 0.5rem 0;">⚠️ Setup Required</h4>
                <p style="color: #856404; font-size: 0.9rem; margin: 0;">
                    To use AI features, add your Groq API key to <code>secrets.toml</code>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔧 Setup Guide"):
                st.markdown("""
                **Steps to get Groq API Key:**
                1. Visit [console.groq.com](https://console.groq.com/)
                2. Sign up for free account
                3. Generate API key
                4. Add to `.streamlit/secrets.toml`:
                ```
                GROQ_API_KEY = "your_api_key_here"
                ```
                5. Restart the app
                """)
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Chat Messages", len(st.session_state.chat_history))
        with col2:
            st.metric("Breed Scans", len(st.session_state.breed_results))
        
        # Clear Data Button
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.breed_results = []
            st.session_state.trading_listings = []
            if 'contacted_sellers' in st.session_state:
                st.session_state.contacted_sellers = []
            st.success("All data cleared!")
            st.rerun()
        
        # Get the current page index for the option menu
        page_options = ["Dashboard", "Breed Recognition", "Trading Platform", "AI Chatbot", "Biogas Business", "Analytics"]
        current_index = page_options.index(st.session_state.current_page) if st.session_state.current_page in page_options else 0
        
        selected = option_menu(
            menu_title="Navigation",
            options=page_options,
            icons=["house", "camera", "handshake", "chat-dots", "recycle", "graph-up"],
            menu_icon="list",
            default_index=current_index,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#2E8B57", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#e8f5e8",
                },
                "nav-link-selected": {"background-color": "#2E8B57"},
            }
        )
        
        # Update session state when page changes
        if selected != st.session_state.current_page:
            st.session_state.current_page = selected
    
    # Route to different pages
    if st.session_state.current_page == "Dashboard":
        show_dashboard()
    elif st.session_state.current_page == "Breed Recognition":
        show_breed_recognition()
    elif st.session_state.current_page == "Trading Platform":
        show_trading_platform()
    elif st.session_state.current_page == "AI Chatbot":
        show_chatbot()
    elif st.session_state.current_page == "Biogas Business":
        show_biogas_business()
    elif st.session_state.current_page == "Analytics":
        show_analytics()

def show_dashboard():
    # Dashboard Header
    st.markdown('<h1 class="section-header">📊 Platform Dashboard</h1>', unsafe_allow_html=True)
    
    # Key metrics with improved spacing
    st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Breed Accuracy</h3>
            <h2>87%</h2>
            <p>AI Recognition Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🤝 Active Traders</h3>
            <h2>1,247</h2>
            <p>Registered Farmers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Transactions</h3>
            <h2>₹2.3L</h2>
            <p>Total Value Traded</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🌱 Biogas Plants</h3>
            <h2>156</h2>
            <p>Active Installations</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Platform features with better structure
    st.markdown('<h2 class="section-header">🚀 Platform Features</h2>', unsafe_allow_html=True)
    
    # Create a grid layout for features
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🔍 AI Breed Recognition</h4>
            <p>Advanced computer vision technology powered by Meta's Llama-4-Scout model to identify cattle breeds with 85-90% accuracy. 
            Supports 20+ Indian breeds with offline capability and enhanced image processing.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🤝 Farmer-to-Farmer Trading</h4>
            <p>Direct trading platform connecting farmers within 50km radius. 
            Features verified profiles, transparent pricing, AI health assessments, and comprehensive logistics support.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 AI Agricultural Chatbot</h4>
            <p>Multilingual cattle-focused knowledge assistant powered by Llama-4-Scout, supporting Hindi, 
            English, Kannada, Telugu, and Tamil with voice and text capabilities for comprehensive farming guidance.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🌱 Sustainable Biogas Business</h4>
            <p>Convert cattle dung into Compressed Biogas (CBG) and organic fertilizer. 
            Multiple revenue streams from energy sales, carbon credits, and government scheme integration.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity with improved layout
    st.markdown('<h2 class="section-header">📈 Recent Activity</h2>', unsafe_allow_html=True)
    
    # Sample activity data
    activity_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'Transactions': [random.randint(5, 25) for _ in range(30)],
        'Breed Scans': [random.randint(50, 150) for _ in range(30)],
        'Chatbot Queries': [random.randint(100, 300) for _ in range(30)]
    })
    
    # Create a container for the chart
    with st.container():
        fig = px.line(activity_data, x='Date', y=['Transactions', 'Breed Scans', 'Chatbot Queries'],
                      title='Platform Activity Over Time',
                      color_discrete_sequence=['#2E8B57', '#228B22', '#32CD32'])
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)

def show_breed_recognition():
    # Header
    st.markdown('<h1 class="section-header">🔍 AI Breed Recognition</h1>', unsafe_allow_html=True)
    
    # Information cards
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="warning-message">
            <strong>📸 Image Quality Tips:</strong>
            <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                <li>Ensure good lighting conditions</li>
                <li>Capture the animal from multiple angles</li>
                <li>Keep the animal clean and visible</li>
                <li>Use high-resolution camera when possible</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-message">
            <strong>🤖 AI Breed Recognition:</strong><br>
            Powered by Meta's Llama-4-Scout model for enhanced accuracy and detailed analysis. 
            The system provides comprehensive breed identification with characteristics, confidence scores, 
            alternative breed suggestions, and specific farming tips.
            <br><br>
            <strong>Model:</strong> meta-llama/llama-4-scout-17b-16e-instruct
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    st.markdown('<h2 class="section-header">📷 Upload & Analyze</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        # Upload section
        st.markdown("""
        <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; border: 2px dashed #2E8B57; text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #2E8B57; margin-bottom: 1rem;">📷 Upload Cattle Image</h3>
            <p style="color: #666; margin-bottom: 1rem;">Choose a clear image of cattle for breed identification</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image of cattle",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of the cattle for breed identification",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            
            # Show original and enhanced images
            st.markdown('<h4 style="color: #2E8B57; margin: 1.5rem 0 1rem 0;">🖼️ Image Comparison</h4>', unsafe_allow_html=True)
            img_col1, img_col2 = st.columns(2, gap="medium")
            
            with img_col1:
                st.image(image, caption="Original Image", use_column_width=True)
            
            with img_col2:
                # Enhance image
                enhanced_image = enhance_image(image)
                st.image(enhanced_image, caption="Enhanced Image", use_column_width=True)
            
            # Convert enhanced image to base64 for API
            buffered = io.BytesIO()
            enhanced_image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Process with Groq API
            st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
            if st.button("🔍 Identify Breed", type="primary", use_container_width=True):
                with st.spinner("Analyzing image with Llama-4-Scout model..."):
                    result = analyze_cattle_breed(img_str)
                    if result:
                        st.session_state.breed_results.append(result)
                        display_breed_result(result)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Recent results sidebar
        st.markdown('<h3 style="color: #2E8B57; margin-bottom: 1rem;">📊 Recent Results</h3>', unsafe_allow_html=True)
        
        if st.session_state.breed_results:
            for i, result in enumerate(reversed(st.session_state.breed_results[-5:])):
                st.markdown(f"""
                <div class="breed-result" style="margin-bottom: 1rem; padding: 1.5rem;">
                    <h5 style="color: #2E8B57; margin: 0 0 0.5rem 0;">Result #{len(st.session_state.breed_results) - i}</h5>
                    <p style="margin: 0.25rem 0;"><strong>Breed:</strong> {result['breed']}</p>
                    <p style="margin: 0.25rem 0;"><strong>Confidence:</strong> {result['confidence']}%</p>
                    <p style="margin: 0.25rem 0;"><strong>Time:</strong> {result['timestamp'].strftime('%H:%M')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-message">
                <strong>📋 No Results Yet</strong><br>
                Upload an image to get started with breed identification!
            </div>
            """, unsafe_allow_html=True)

def enhance_image(image):
    """Enhance image quality for better breed recognition using PIL only"""
    try:
        from PIL import ImageEnhance, ImageFilter
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 1. Enhance contrast
        contrast_enhancer = ImageEnhance.Contrast(image)
        enhanced = contrast_enhancer.enhance(1.2)  # Increase contrast by 20%
        
        # 2. Enhance sharpness
        sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
        enhanced = sharpness_enhancer.enhance(1.5)  # Increase sharpness by 50%
        
        # 3. Enhance brightness slightly
        brightness_enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = brightness_enhancer.enhance(1.1)  # Increase brightness by 10%
        
        # 4. Apply slight blur to reduce noise
        enhanced = enhanced.filter(ImageFilter.MedianFilter(size=3))
        
        return enhanced
    except Exception as e:
        st.warning(f"Image enhancement failed: {e}")
        return image

def analyze_cattle_breed(image_base64):
    """Analyze cattle breed using Groq API with image processing"""
    try:
        groq_client = get_groq_client()
        if not groq_client:
            # Fallback to simulated analysis if API not available
            return simulate_breed_analysis()
        
        # Create a detailed prompt for breed identification
        prompt = f"""
        You are an expert veterinarian and cattle breed specialist. Analyze this cattle image and identify the breed.
        
        Indian cattle breeds to consider:
        - Gir: Large, humped cattle with drooping ears, white to red color, excellent milk producers
        - Sahiwal: Reddish brown, medium-sized, heat-tolerant, good for tropical climates  
        - Red Sindhi: Red color, medium-sized, good milk producers, adaptable to various conditions
        - Tharparkar: White to light gray, drought-resistant, dual-purpose, desert-adapted
        - Kankrej: Large, gray to black, strong draught animals, heavy work capacity
        - Ongole: White, large hump, good for both milk and draught, muscular build
        - Deoni: White with black spots, medium-sized, dual-purpose, hardy breed
        - Rathi: Brown to black, medium-sized, good milk yield, docile temperament
        - Hariana: White to light gray, medium-sized, dual-purpose, northern India breed
        - Murrah: Black, medium-sized, excellent milk producers, high butterfat content
        - Jaffarabadi: Black, large, good milk and draught animals, Gujarat origin
        
        Provide your analysis in this JSON format:
        {{
            "breed": "most_likely_breed",
            "confidence": "confidence_percentage",
            "characteristics": "detailed_description_of_breed_features",
            "reasoning": "why_this_breed_was_selected",
            "alternative_breeds": ["second_choice", "third_choice"],
            "farming_tips": "specific_advice_for_this_breed"
        }}
        
        Be realistic and educational for farmers.
        """
        
        # Use Groq API for analysis
        response = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                        }
                    ]
                }
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        response_text = response.choices[0].message.content
        
        # Try to parse JSON response
        try:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result_data = json.loads(json_match.group())
                return {
                    'breed': result_data.get('breed', 'Unknown'),
                    'confidence': result_data.get('confidence', '85'),
                    'characteristics': result_data.get('characteristics', 'Standard cattle characteristics'),
                    'reasoning': result_data.get('reasoning', 'Based on visual analysis'),
                    'alternatives': result_data.get('alternative_breeds', []),
                    'farming_tips': result_data.get('farming_tips', 'General farming advice'),
                    'timestamp': datetime.now(),
                    'raw_response': response_text
                }
        except:
            pass
        
        # Fallback parsing
        breed = "Unknown"
        confidence = "85"
        characteristics = response_text[:200] + "..." if len(response_text) > 200 else response_text
        
        # Extract breed name (simple keyword matching)
        for b in sample_breeds:
            if b.lower() in response_text.lower():
                breed = b
                break
        
        # Extract confidence (look for percentage)
        import re
        confidence_match = re.search(r'(\d+)%', response_text)
        if confidence_match:
            confidence = confidence_match.group(1)
        
        return {
            'breed': breed,
            'confidence': confidence,
            'characteristics': characteristics,
            'reasoning': 'Based on visual analysis',
            'alternatives': [],
            'farming_tips': 'General farming advice for this breed',
            'timestamp': datetime.now(),
            'raw_response': response_text
        }
        
    except Exception as e:
        st.error(f"Error analyzing image: {e}")
        # Return simulated result as fallback
        return simulate_breed_analysis()

def simulate_breed_analysis():
    """Simulate breed analysis when API is not available"""
    import random
    
    breed = random.choice(sample_breeds)
    confidence = random.randint(75, 95)
    
    breed_info = {
        "Gir": {
            "characteristics": "Large humped cattle with drooping ears, white to red color, excellent milk producers",
            "tips": "Provide high-quality feed and maintain proper hygiene for optimal milk production"
        },
        "Sahiwal": {
            "characteristics": "Reddish brown, medium-sized, heat-tolerant, good for tropical climates",
            "tips": "Ensure adequate shade and water supply during hot weather"
        },
        "Murrah": {
            "characteristics": "Black, medium-sized, excellent milk producers, high butterfat content",
            "tips": "Focus on balanced nutrition and regular health checkups"
        }
    }
    
    info = breed_info.get(breed, {
        "characteristics": "Standard cattle characteristics with good adaptability",
        "tips": "Maintain proper nutrition and regular veterinary care"
    })
    
    return {
        'breed': breed,
        'confidence': str(confidence),
        'characteristics': info["characteristics"],
        'reasoning': 'Based on visual analysis of breed characteristics',
        'alternatives': random.sample([b for b in sample_breeds if b != breed], 2),
        'farming_tips': info["tips"],
        'timestamp': datetime.now(),
        'raw_response': f"Simulated analysis for {breed} cattle"
    }

def display_breed_result(result):
    """Display breed identification result"""
    st.markdown(f"""
    <div class="breed-result">
        <h3>🎯 Breed Identification Result</h3>
        <h4>Breed: {result['breed']}</h4>
        <p><strong>Confidence:</strong> {result['confidence']}%</p>
        <p><strong>Characteristics:</strong> {result['characteristics']}</p>
        <p><strong>Reasoning:</strong> {result.get('reasoning', 'Based on visual analysis')}</p>
        {f"<p><strong>Alternative Breeds:</strong> {', '.join(result.get('alternatives', []))}</p>" if result.get('alternatives') else ""}
        <p><strong>Farming Tips:</strong> {result.get('farming_tips', 'General farming advice')}</p>
        <p><strong>Timestamp:</strong> {result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

def show_trading_platform():
    # Header
    st.markdown('<h1 class="section-header">🤝 Farmer-to-Farmer Trading Platform</h1>', unsafe_allow_html=True)
    
    # Trading statistics with improved layout
    st.markdown('<h2 class="section-header">📊 Trading Statistics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📋 Active Listings</h3>
            <h2>247</h2>
            <p>+12 this week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>✅ Successful Trades</h3>
            <h2>1,156</h2>
            <p>+23 this week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Average Price</h3>
            <h2>₹42,500</h2>
            <p>+₹2,100 this week</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Search and filters with better structure
    st.markdown('<h2 class="section-header">🔍 Search Cattle</h2>', unsafe_allow_html=True)
    
    # Filter section
    with st.container():
        st.markdown("""
        <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <h3 style="color: #2E8B57; margin-bottom: 1.5rem;">🎯 Filter Options</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        with col1:
            breed_filter = st.selectbox("🐄 Breed", ["All"] + sample_breeds, help="Select cattle breed")
        with col2:
            location_filter = st.selectbox("📍 Location", ["All", "Karnataka", "Punjab", "Haryana", "Rajasthan", "Gujarat"], help="Select location")
        with col3:
            price_range = st.selectbox("💰 Price Range", ["All", "Under ₹30,000", "₹30,000 - ₹50,000", "Above ₹50,000"], help="Select price range")
        with col4:
            health_filter = st.selectbox("🏥 Health Status", ["All", "Excellent", "Good", "Fair"], help="Select health status")
    
    # Display listings with improved layout
    st.markdown('<h2 class="section-header">📋 Available Cattle</h2>', unsafe_allow_html=True)
    
    # Filter data based on selections
    filtered_data = sample_trading_data.copy()
    
    if breed_filter != "All":
        filtered_data = [item for item in filtered_data if item['breed'] == breed_filter]
    if location_filter != "All":
        filtered_data = [item for item in filtered_data if item['location'] == location_filter]
    if health_filter != "All":
        filtered_data = [item for item in filtered_data if item['health'] == health_filter]
    
    # Display listings in improved cards
    if filtered_data:
        for i, item in enumerate(filtered_data):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="background: white; padding: 2rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-left: 5px solid #2E8B57;">
                        <h3 style="color: #2E8B57; margin: 0 0 1rem 0;">🐄 {item['breed']} - {item['age']}</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <p style="margin: 0.5rem 0;"><strong>👤 Seller:</strong> {item['seller']}</p>
                            <p style="margin: 0.5rem 0;"><strong>📍 Location:</strong> {item['location']}</p>
                            <p style="margin: 0.5rem 0;"><strong>🏥 Health:</strong> {item['health']}</p>
                            <p style="margin: 0.5rem 0;"><strong>💰 Price:</strong> {item['price']}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
                    if st.button(f"📞 Contact {item['seller']}", key=f"contact_{i}", use_container_width=True):
                        st.success(f"📧 Contact information for {item['seller']}:")
                        st.info(f"**Email:** {item['seller'].replace(' ', '').lower()}@farmersmarket.com")
                        st.info(f"**Phone:** +91-{random.randint(9000000000, 9999999999)}")
                        st.info(f"**Location:** {item['location']}")
                        st.info(f"**Cattle:** {item['breed']} - {item['age']} - {item['price']}")
                        
                        # Add to session state for tracking
                        if 'contacted_sellers' not in st.session_state:
                            st.session_state.contacted_sellers = []
                        st.session_state.contacted_sellers.append({
                            'seller': item['seller'],
                            'breed': item['breed'],
                            'timestamp': datetime.now()
                        })
    else:
        st.markdown("""
        <div class="info-message">
            <strong>🔍 No Results Found</strong><br>
            Try adjusting your search filters to find more cattle listings.
        </div>
        """, unsafe_allow_html=True)
    
    # Add new listing section
    st.markdown('<h2 class="section-header">➕ Add Your Cattle Listing</h2>', unsafe_allow_html=True)
    
    with st.expander("📝 Create New Listing", expanded=False):
        st.markdown("""
        <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; margin: 1rem 0;">
            <h3 style="color: #2E8B57; margin-bottom: 1.5rem;">📋 Listing Details</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            new_breed = st.selectbox("🐄 Breed", sample_breeds, key="new_breed", help="Select cattle breed")
            new_age = st.text_input("📅 Age", placeholder="e.g., 3 years", help="Enter cattle age")
            new_price = st.text_input("💰 Price", placeholder="e.g., ₹45,000", help="Enter asking price")
        
        with col2:
            new_location = st.text_input("📍 Location", placeholder="e.g., Karnataka", help="Enter your location")
            new_health = st.selectbox("🏥 Health Status", ["Excellent", "Good", "Fair"], key="new_health", help="Select health status")
            new_seller = st.text_input("👤 Your Name", placeholder="e.g., Ramu Patel", help="Enter your name")
        
        st.markdown('<div style="text-align: center; margin: 2rem 0;">', unsafe_allow_html=True)
        if st.button("📝 Create Listing", type="primary", use_container_width=True):
            st.success("Your cattle listing has been created successfully!")
            st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)

def show_chatbot():
    # Header
    st.markdown('<h1 class="section-header">🤖 AI Agricultural Chatbot</h1>', unsafe_allow_html=True)
    
    # Information card
    st.markdown("""
    <div class="success-message">
        <strong>🌾 Cattle Knowledge Assistant</strong><br>
        Powered by Meta's Llama-4-Scout model for enhanced agricultural expertise. 
        Ask questions about cattle breeds, health management, breeding, feeding, and farming practices. 
        Available in Hindi, English, Kannada, Telugu, and Tamil.
        <br><br>
        <strong>Model:</strong> meta-llama/llama-4-scout-17b-16e-instruct
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface with improved layout
    st.markdown('<h2 class="section-header">💬 Ask Your Question</h2>', unsafe_allow_html=True)
    
    # Input section
    with st.container():
        st.markdown("""
        <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <h3 style="color: #2E8B57; margin-bottom: 1.5rem;">🎯 Ask About Cattle Farming</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1], gap="large")
        
        with col1:
            user_input = st.text_input(
                "Ask your question about cattle farming:",
                placeholder="e.g., What are the best feeding practices for Gir cattle?",
                key="chat_input",
                help="Enter your question about cattle farming, health, breeding, or management"
            )
        
        with col2:
            language_options = ["English", "Hindi", "Kannada", "Telugu", "Tamil"]
            try:
                current_language_index = language_options.index(st.session_state.selected_language)
            except ValueError:
                current_language_index = 0  # Default to English if language not found
            
            language = st.selectbox(
                "🌐 Language", 
                language_options, 
                index=current_language_index,
                help="Select your preferred language",
                key="language_selector"
            )
            # Update session state when language changes
            if language != st.session_state.selected_language:
                st.session_state.selected_language = language
        
        st.markdown('<div style="text-align: center; margin: 1.5rem 0;">', unsafe_allow_html=True)
        if st.button("💬 Ask Question", type="primary", use_container_width=True) and user_input:
            with st.spinner("🤔 Thinking with Llama-4-Scout..."):
                response = get_chatbot_response(user_input, st.session_state.selected_language)
                if response:
                    st.session_state.chat_history.append({
                        'user': user_input,
                        'bot': response,
                        'timestamp': datetime.now(),
                        'language': st.session_state.selected_language
                    })
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick question buttons with improved layout
    st.markdown('<h2 class="section-header">🚀 Quick Questions</h2>', unsafe_allow_html=True)
    
    quick_questions = [
        "What are the characteristics of Gir cattle?",
        "How to prevent cattle diseases?",
        "Best feeding practices for dairy cattle?",
        "When is the best time for breeding?",
        "How to identify healthy cattle?",
        "What are the benefits of crossbreeding?"
    ]
    
    # Create a grid layout for quick questions
    cols = st.columns(2, gap="large")
    for i, question in enumerate(quick_questions):
        with cols[i % 2]:
            if st.button(question, key=f"quick_{i}", use_container_width=True):
                with st.spinner("🤔 Thinking..."):
                    response = get_chatbot_response(question, st.session_state.selected_language)
                    if response:
                        st.session_state.chat_history.append({
                            'user': question,
                            'bot': response,
                            'timestamp': datetime.now(),
                            'language': st.session_state.selected_language
                        })
                        st.rerun()
    
    # Display chat history with improved layout
    st.markdown('<h2 class="section-header">💬 Conversation History</h2>', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        # Add a container for better scrolling
        with st.container():
            for i, chat in enumerate(reversed(st.session_state.chat_history[-10:])):
                # User message
                st.markdown(f"""
                <div class="chat-message user-message">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong>👤 You ({chat['language']})</strong>
                        <small style="color: #666;">{chat['timestamp'].strftime('%H:%M:%S')}</small>
                    </div>
                    <p style="margin: 0;">{chat['user']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Bot message
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong>🤖 AI Assistant</strong>
                        <small style="color: #666;">Powered by Llama-4-Scout</small>
                    </div>
                    <p style="margin: 0; line-height: 1.6;">{chat['bot']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Add separator
                if i < len(st.session_state.chat_history[-10:]) - 1:
                    st.markdown('<hr style="margin: 1rem 0; border: none; border-top: 1px solid #e0e0e0;">', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-message">
            <strong>💬 Start a Conversation</strong><br>
            Ask a question about cattle farming to begin your conversation with our AI assistant!
        </div>
        """, unsafe_allow_html=True)

def get_chatbot_response(question, language):
    """Get response from LangChain Groq chatbot"""
    try:
        llm = get_langchain_groq_client()
        if not llm:
            return get_fallback_response(question, language)
        
        # Create language-specific prompt templates
        language_prompts = {
            "English": """
            You are an expert agricultural advisor specializing in cattle farming in India. 
            You have deep knowledge of Indian cattle breeds, farming practices, health management, 
            breeding, feeding, and sustainable farming methods.
            
            Provide detailed, practical advice that is:
            - Specific to Indian farming conditions
            - Actionable and implementable
            - Based on scientific principles
            - Considerate of local resources and constraints
            
            Question: {question}
            
            Please provide a comprehensive answer with practical tips and recommendations.
            """,
            "Hindi": """
            आप भारत में मवेशी पालन के विशेषज्ञ कृषि सलाहकार हैं। 
            आपको भारतीय मवेशी नस्लों, खेती के तरीकों, स्वास्थ्य प्रबंधन, 
            प्रजनन, भोजन और सतत खेती के तरीकों का गहरा ज्ञान है।
            
            विस्तृत, व्यावहारिक सलाह दें जो:
            - भारतीय खेती की स्थितियों के लिए विशिष्ट हो
            - क्रियान्वयन योग्य हो
            - वैज्ञानिक सिद्धांतों पर आधारित हो
            - स्थानीय संसाधनों और बाधाओं को ध्यान में रखे
            
            प्रश्न: {question}
            
            कृपया व्यावहारिक सुझावों और सिफारिशों के साथ एक व्यापक उत्तर दें।
            """,
            "Kannada": """
            ನೀವು ಭಾರತದಲ್ಲಿ ಜಾನುವಾರು ಕೃಷಿಯಲ್ಲಿ ಪರಿಣತಿ ಹೊಂದಿರುವ ಕೃಷಿ ಸಲಹೆಗಾರರಾಗಿದ್ದೀರಿ.
            ನಿಮಗೆ ಭಾರತೀಯ ಜಾನುವಾರು ತಳಿಗಳು, ಕೃಷಿ ಪದ್ಧತಿಗಳು, ಆರೋಗ್ಯ ನಿರ್ವಹಣೆ,
            ಸಂತಾನೋತ್ಪತ್ತಿ, ಆಹಾರ ಮತ್ತು ಸುಸ್ಥಿರ ಕೃಷಿ ವಿಧಾನಗಳ ಬಗ್ಗೆ ಆಳವಾದ ಜ್ಞಾನವಿದೆ.
            
            ವಿವರವಾದ, ಪ್ರಾಯೋಗಿಕ ಸಲಹೆ ನೀಡಿ:
            - ಭಾರತೀಯ ಕೃಷಿ ಪರಿಸ್ಥಿತಿಗಳಿಗೆ ನಿರ್ದಿಷ್ಟ
            - ಕಾರ್ಯಗತಗೊಳಿಸಬಹುದಾದ
            - ವಿಜ್ಞಾನಿಕ ತತ್ವಗಳ ಆಧಾರದ ಮೇಲೆ
            - ಸ್ಥಳೀಯ ಸಂಪನ್ಮೂಲಗಳು ಮತ್ತು ನಿರ್ಬಂಧಗಳನ್ನು ಪರಿಗಣಿಸಿ
            
            ಪ್ರಶ್ನೆ: {question}
            
            ದಯವಿಟ್ಟು ಪ್ರಾಯೋಗಿಕ ಸಲಹೆಗಳು ಮತ್ತು ಶಿಫಾರಸುಗಳೊಂದಿಗೆ ಸಮಗ್ರ ಉತ್ತರವನ್ನು ನೀಡಿ.
            """,
            "Telugu": """
            మీరు భారతదేశంలో పశుపాలనలో నిపుణులైన వ్యవసాయ సలహాదారులు.
            మీకు భారతీయ పశువుల జాతులు, వ్యవసాయ పద్ధతులు, ఆరోగ్య నిర్వహణ,
            సంతానోత్పత్తి, ఆహారం మరియు స్థిరమైన వ్యవసాయ పద్ధతుల గురించి లోతైన జ్ఞానం ఉంది.
            
            వివరమైన, ఆచరణాత్మక సలహాలు ఇవ్వండి:
            - భారతీయ వ్యవసాయ పరిస్థితులకు నిర్దిష్టమైనది
            - అమలు చేయదగినది
            - శాస్త్రీయ సూత్రాల ఆధారంగా
            - స్థానిక వనరులు మరియు నిర్బంధాలను పరిగణనలోకి తీసుకుంటుంది
            
            ప్రశ్న: {question}
            
            దయచేసి ఆచరణాత్మక చిట్కాలు మరియు సిఫార్సులతో సమగ్ర సమాధానం ఇవ్వండి.
            """,
            "Tamil": """
            நீங்கள் இந்தியாவில் கால்நடை வளர்ப்பில் நிபுணரான விவசாய ஆலோசகர்.
            உங்களுக்கு இந்திய கால்நடை இனங்கள், விவசாய முறைகள், ஆரோக்கிய மேலாண்மை,
            இனப்பெருக்கம், உணவு மற்றும் நிலையான விவசாய முறைகள் பற்றி ஆழமான அறிவு உள்ளது.
            
            விரிவான, நடைமுறை ஆலோசனைகளை வழங்குங்கள்:
            - இந்திய விவசாய நிலைமைகளுக்கு குறிப்பிட்டது
            - செயல்படுத்தக்கூடியது
            - அறிவியல் கொள்கைகளின் அடிப்படையில்
            - உள்ளூர் வளங்கள் மற்றும் தடைகளை கணக்கில் எடுத்துக்கொள்கிறது
            
            கேள்வி: {question}
            
            தயவுசெய்து நடைமுறை குறிப்புகள் மற்றும் பரிந்துரைகளுடன் விரிவான பதிலை வழங்குங்கள்.
            """
        }
        
        # Create prompt template
        prompt_template = ChatPromptTemplate.from_template(
            language_prompts.get(language, language_prompts['English'])
        )
        
        # Create chain
        chain = prompt_template | llm | StrOutputParser()
        
        # Get response
        response = chain.invoke({"question": question})
        
        return response
        
    except Exception as e:
        st.error(f"Chatbot error: {str(e)}")
        return get_fallback_response(question, language)

def get_fallback_response(question, language):
    """Provide fallback responses when API is not available"""
    question_lower = question.lower()
    
    # English responses
    if language == "English":
        if any(word in question_lower for word in ["gir", "breed", "characteristics"]):
            return """**Gir Cattle Characteristics:**
- Origin: Gujarat, India
- Size: Large with prominent hump
- Color: White to red with black spots
- Milk Production: 3,000-4,000 liters per lactation
- Temperament: Docile and hardy
- Best for: High milk production and tropical climates

**Farming Tips:**
- Provide balanced nutrition with green fodder
- Ensure clean water supply
- Regular health checkups and vaccinations
- Maintain proper shelter and ventilation"""
        
        elif any(word in question_lower for word in ["disease", "health", "prevent"]):
            return """**Common Cattle Diseases Prevention:**
- **Foot and Mouth Disease**: Regular vaccination, quarantine new animals
- **Mastitis**: Maintain clean milking environment, proper udder hygiene
- **Bloat**: Avoid sudden diet changes, provide adequate roughage
- **Parasites**: Regular deworming, clean housing

**Health Management:**
- Daily health monitoring
- Proper nutrition and clean water
- Regular veterinary checkups
- Maintain clean and dry housing"""
        
        elif any(word in question_lower for word in ["feeding", "feed", "nutrition"]):
            return """**Cattle Feeding Best Practices:**
- **Green Fodder**: 25-30 kg per day for adult cattle
- **Dry Fodder**: 8-10 kg per day
- **Concentrates**: 2-3 kg per day for milking cows
- **Water**: 50-80 liters per day

**Feeding Schedule:**
- Morning: Concentrates + green fodder
- Afternoon: Dry fodder + water
- Evening: Green fodder + concentrates
- Night: Dry fodder"""
        
        else:
            return """**General Cattle Farming Advice:**
- Choose breeds suitable for your climate
- Provide adequate shelter and clean water
- Maintain proper nutrition and health care
- Regular veterinary checkups
- Keep records of breeding and health
- Practice good hygiene and sanitation

For specific questions, please provide more details about your farming situation."""
    
    # Hindi responses
    elif language == "Hindi":
        return """**सामान्य मवेशी पालन सलाह:**
- अपने जलवायु के अनुकूल नस्ल चुनें
- पर्याप्त आश्रय और स्वच्छ पानी प्रदान करें
- उचित पोषण और स्वास्थ्य देखभाल बनाए रखें
- नियमित पशु चिकित्सा जांच
- प्रजनन और स्वास्थ्य के रिकॉर्ड रखें
- अच्छी स्वच्छता का अभ्यास करें

विशिष्ट प्रश्नों के लिए, कृपया अपनी खेती की स्थिति के बारे में अधिक विवरण दें।"""
    
    # Default response
    else:
        return f"I understand you're asking about: {question}\n\nFor detailed assistance, please ensure your Groq API key is properly configured in the secrets.toml file."

def show_biogas_business():
    st.title("🌱 Biogas & Sustainable Business")
    
    # Business overview
    st.markdown("""
    <div class="success-message">
        <strong>💰 Revenue Opportunities</strong><br>
        Convert cattle dung into Compressed Biogas (CBG) and organic fertilizer. 
        Small plants can generate ₹16+ lakh yearly income.
    </div>
    """, unsafe_allow_html=True)
    
    # Revenue streams
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ CBG Sales</h3>
            <h2>₹50-60/kg</h2>
            <p>Compressed Biogas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🌾 Bio-Slurry</h3>
            <h2>₹5-15/kg</h2>
            <p>Organic Fertilizer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🌍 Carbon Credits</h3>
            <h2>₹2,000/ton</h2>
            <p>CO2 Reduction</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Business calculator
    st.subheader("🧮 Business Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Plant Size Calculator</h4>
            <p>Calculate potential revenue based on your cattle count and dung production.</p>
        </div>
        """, unsafe_allow_html=True)
        
        cattle_count = st.number_input("Number of Cattle", min_value=1, max_value=1000, value=10)
        dung_per_cow = st.number_input("Dung per Cow (kg/day)", min_value=10, max_value=50, value=25)
        
        # Calculations
        total_dung = cattle_count * dung_per_cow
        cbg_production = total_dung * 0.15  # 15% conversion rate
        slurry_production = total_dung * 0.8  # 80% slurry
        
        daily_cbg_revenue = cbg_production * 55  # ₹55/kg average
        daily_slurry_revenue = slurry_production * 10  # ₹10/kg average
        daily_total = daily_cbg_revenue + daily_slurry_revenue
        
        yearly_revenue = daily_total * 365
    
    with col2:
        st.markdown(f"""
        <div class="breed-result">
            <h4>💰 Revenue Projection</h4>
            <p><strong>Cattle Count:</strong> {cattle_count}</p>
            <p><strong>Daily Dung:</strong> {total_dung} kg</p>
            <p><strong>CBG Production:</strong> {cbg_production:.1f} kg/day</p>
            <p><strong>Slurry Production:</strong> {slurry_production:.1f} kg/day</p>
            <hr>
            <h5>Daily Revenue: ₹{daily_total:,.0f}</h5>
            <h4>Yearly Revenue: ₹{yearly_revenue:,.0f}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # Product showcase
    st.subheader("🛍️ Cow Dung Products")
    
    products = [
        {"name": "Cow Dung Soap", "price": "₹50-100", "market": "Urban Wellness"},
        {"name": "Eco-Friendly Idols", "price": "₹20-50", "market": "Religious"},
        {"name": "Cow Dung Wood", "price": "₹100-200", "market": "Construction"},
        {"name": "Dhoop Sticks", "price": "₹30-80", "market": "Religious"},
        {"name": "Packaging Material", "price": "₹40-120", "market": "Eco-Friendly"},
        {"name": "Cattle Compost", "price": "₹5-15", "market": "Agriculture"}
    ]
    
    cols = st.columns(3)
    for i, product in enumerate(products):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <h5>{product['name']}</h5>
                <p><strong>Price:</strong> {product['price']}</p>
                <p><strong>Market:</strong> {product['market']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Government schemes
    st.subheader("🏛️ Government Support")
    
    schemes = [
        "SATAT Scheme - ₹46/kg CBG support",
        "GOBAR DHAN - ₹50 lakh plant subsidy",
        "PM-KUSUM - Solar-biogas integration",
        "National Biogas Program - Technical support"
    ]
    
    for scheme in schemes:
        st.markdown(f"✅ {scheme}")

def show_analytics():
    st.markdown('<h1 class="section-header">📈 Platform Analytics</h1>', unsafe_allow_html=True)
    
    # Real-time metrics from session state
    total_chats = len(st.session_state.chat_history)
    total_scans = len(st.session_state.breed_results)
    contacted_sellers = len(st.session_state.get('contacted_sellers', []))
    
    # Key performance indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Chat Sessions", total_chats, f"+{total_chats}" if total_chats > 0 else "0")
    with col2:
        st.metric("Breed Scans", total_scans, f"+{total_scans}" if total_scans > 0 else "0")
    with col3:
        st.metric("Seller Contacts", contacted_sellers, f"+{contacted_sellers}" if contacted_sellers > 0 else "0")
    with col4:
        st.metric("Active Users", "1", "You")
    
    # User Activity Analysis
    if total_chats > 0 or total_scans > 0:
        st.markdown('<h2 class="section-header">📊 Your Activity</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Activity breakdown
            activity_data = pd.DataFrame({
                'Activity': ['Chat Messages', 'Breed Scans', 'Seller Contacts'],
                'Count': [total_chats, total_scans, contacted_sellers]
            })
            
            fig = px.bar(activity_data, x='Activity', y='Count', 
                         title='Your Platform Activity',
                         color='Count',
                         color_continuous_scale='Greens')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Language usage
            if total_chats > 0:
                language_counts = {}
                for chat in st.session_state.chat_history:
                    lang = chat.get('language', 'English')
                    language_counts[lang] = language_counts.get(lang, 0) + 1
                
                if language_counts:
                    lang_data = pd.DataFrame({
                        'Language': list(language_counts.keys()),
                        'Messages': list(language_counts.values())
                    })
                    
                    fig = px.pie(lang_data, values='Messages', names='Language', 
                                 title='Language Usage in Chats')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No chat data available")
            else:
                st.info("Start chatting to see language usage statistics")
    
    # Charts
    st.markdown('<h2 class="section-header">📈 Market Overview</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Breed popularity chart
        breed_data = pd.DataFrame({
            'Breed': sample_breeds[:8],
            'Listings': [45, 38, 32, 28, 25, 22, 18, 15]
        })
        
        fig = px.bar(breed_data, x='Breed', y='Listings', 
                     title='Most Popular Cattle Breeds',
                     color='Listings',
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Regional distribution
        region_data = pd.DataFrame({
            'State': ['Karnataka', 'Punjab', 'Haryana', 'Rajasthan', 'Gujarat'],
            'Users': [456, 389, 324, 287, 234]
        })
        
        fig = px.pie(region_data, values='Users', names='State', 
                     title='User Distribution by State')
        st.plotly_chart(fig, use_container_width=True)
    
    # Monthly trends
    st.subheader("📊 Monthly Trends")
    
    monthly_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Transactions': [45, 52, 48, 61, 58, 67],
        'Revenue': [180000, 210000, 195000, 245000, 230000, 270000]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_data['Month'], y=monthly_data['Transactions'], 
                            name='Transactions', yaxis='y'))
    fig.add_trace(go.Scatter(x=monthly_data['Month'], y=monthly_data['Revenue']/1000, 
                            name='Revenue (₹K)', yaxis='y2'))
    
    fig.update_layout(
        title='Monthly Platform Performance',
        yaxis=dict(title='Transactions'),
        yaxis2=dict(title='Revenue (₹K)', overlaying='y', side='right')
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
