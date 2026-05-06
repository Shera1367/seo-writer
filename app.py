import streamlit as st
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

# Page Config
st.set_page_config(page_title="Professional SEO Content Engine", layout="wide")

# Fixed API Key
API_KEY = "AIzaSyA-qdNkgPPL31NkuOeHDyF5ducJRuD-0LU"

# FORCE STABLE VERSION
os_environ = {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}
genai.configure(api_key=API_KEY, transport='rest')

st.title("🚀 Professional SEO Content Engine")
st.info("This tool generates full English articles in ready-to-use HTML format.")

# Sidebar
with st.sidebar:
    st.header("Global Settings")
    tone = st.selectbox("Tone of Voice", ["Professional", "Informative", "Casual", "Technical", "Authoritative"])
    word_count = st.number_input("Target Word Count", min_value=300, max_value=5000, value=1000)

# Main Input Fields
col1, col2 = st.columns(2)
with col1:
    article_title = st.text_input("Article Title")
    keywords = st.text_area("Keywords")
with col2:
    headings = st.text_area("Suggested Headings")
    extra_instructions = st.text_area("Extra Instructions")

if st.button("Generate HTML Article"):
    if not article_title:
        st.error("Please enter the Article Title.")
    else:
        try:
            with st.spinner("Crafting content..."):
                # Using gemini-1.5-flash as the most reliable high-speed model
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""Write a professional SEO article in English.
                Title: {article_title}
                Keywords: {keywords}
                Structure: {headings}
                Tone: {tone}
                Target Length: {word_count} words.
                Additional Notes: {extra_instructions}
                
                IMPORTANT: Return ONLY the content wrapped in HTML tags (h2, h3, p, ul, li, strong). 
                Do not use markdown code blocks (```html)."""
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("Generation Complete!")
                    tab1, tab2 = st.tabs(["Preview", "HTML Source"])
                    with tab1:
                        st.markdown(response.text, unsafe_allow_html=True)
                    with tab2:
                        st.code(response.text, language="html")
                
        except Exception as e:
            st.error(f"Technical Error: {e}")
            st.info("Check if your API key from Google AI Studio is active and has 'Gemini API' enabled.")
