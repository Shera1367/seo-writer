import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Professional SEO Content Writer", layout="wide")

# Fixed API Key
API_KEY = "AIzaSyA-qdNkgPPL31NkuOeHDyF5ducJRuD-0LU"
genai.configure(api_key=API_KEY)

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
    extra_instructions = st.text_area("Extra Instructions", placeholder="e.g. Add a FAQ section or use specific local SEO terms...")

if st.button("Generate HTML Article"):
    if not article_title:
        st.error("Please enter the Article Title.")
    else:
        try:
            with st.spinner("Gemini is crafting your content..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"""
                Write a comprehensive, SEO-optimized English article.
                - Title: {article_title}
                - Keywords: {keywords}
                - Structure: {headings}
                - Tone: {tone}
                - Length: {word_count} words.
                - Additional Instructions: {extra_instructions}
                
                Format Requirements:
                1. Output MUST be in raw HTML format (using <h2>, <h3>, <p>, <ul>, <li>, <strong>).
                2. DO NOT use markdown code blocks (no ```html).
                3. Ensure the content is human-like and passes basic SEO checks.
                """
                
                response = model.generate_content(prompt)
                article_content = response.text
                
                st.success("Generation Complete!")
                
                # Display Result
                tab1, tab2 = st.tabs(["Preview", "HTML Source"])
                
                with tab1:
                    st.markdown(article_content, unsafe_allow_html=True)
                
                with tab2:
                    st.code(article_content, language="html")
                    st.button("Copy to Clipboard", on_click=lambda: st.write("Code copied! (Manual copy required in some browsers)"))
                    
        except Exception as e:
            st.error(f"An error occurred: {e}")