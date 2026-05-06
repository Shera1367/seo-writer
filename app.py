import streamlit as st
import google.generativeai as genai
import os

# Page Config
st.set_page_config(page_title="Professional SEO Content Engine", layout="wide")

# Fixed API Key
API_KEY = "AIzaSyA-qdNkgPPL31NkuOeHDyF5ducJRuD-0LU"

# Configure SDK to use stable version
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Configuration Error: {e}")

st.title("🚀 Professional SEO Content Engine")
st.info("This tool generates full English articles in ready-to-use HTML format.")

# Sidebar for metadata
with st.sidebar:
    st.header("Global Settings")
    tone = st.selectbox("Tone of Voice", ["Professional", "Informative", "Casual", "Technical", "Authoritative"])
    word_count = st.number_input("Target Word Count", min_value=300, max_value=5000, value=1000)

# Main Input Fields
col1, col2 = st.columns(2)

with col1:
    article_title = st.text_input("Article Title", placeholder="Enter your main H1 title")
    keywords = st.text_area("Keywords", placeholder="Enter primary and LSI keywords...")

with col2:
    headings = st.text_area("Suggested Headings", placeholder="H2, H3 structures...")
    extra_instructions = st.text_area("Extra Instructions", placeholder="e.g. Add a FAQ section...")

if st.button("Generate HTML Article"):
    if not article_title:
        st.error("Please enter the Article Title.")
    else:
        try:
            with st.spinner("Gemini is crafting your content..."):
                # Using the most stable model name string
                model = genai.GenerativeModel('gemini-1.5-flash') 
                
                prompt = f"""
                Write a complete, high-quality SEO article in English.
                Title: {article_title}
                Keywords: {keywords}
                Structure: {headings}
                Tone: {tone}
                Length: {word_count} words.
                Instructions: {extra_instructions}
                
                Format: Output ONLY raw HTML (h2, h3, p, ul, li). No markdown blocks.
                """
                
                # Use a more direct generation call
                response = model.generate_content(prompt)
                
                if response:
                    st.success("Generation Complete!")
                    tab1, tab2 = st.tabs(["Preview", "HTML Source"])
                    with tab1:
                        st.markdown(response.text, unsafe_allow_html=True)
                    with tab2:
                        st.code(response.text, language="html")
                
        except Exception as e:
            # If 1.5-flash fails, try the older stable pro as fallback
            try:
                model_fallback = genai.GenerativeModel('gemini-pro')
                response = model_fallback.generate_content(prompt)
                st.markdown(response.text, unsafe_allow_html=True)
            except:
                st.error(f"Critical Error: {e}")
                st.write("Please ensure your API Key has access to Gemini models in Google AI Studio.")
