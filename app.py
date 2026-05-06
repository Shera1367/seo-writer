import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Professional SEO Content Engine", layout="wide")

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
    extra_instructions = st.text_area("Extra Instructions", placeholder="e.g. Add a FAQ section...")

if st.button("Generate HTML Article"):
    if not article_title:
        st.error("Please enter the Article Title.")
    else:
        try:
            with st.spinner("Gemini is crafting your content..."):
                # Updated model selection to avoid 404
                model = genai.GenerativeModel(model_name='gemini-1.5-flash') 
                
                prompt = f"""
                Write a complete, high-quality SEO article in English.
                - Title: {article_title}
                - Keywords: {keywords}
                - Structure: {headings}
                - Tone: {tone}
                - Length: {word_count} words.
                - Additional Instructions: {extra_instructions}
                
                Format Requirements:
                1. Output MUST be in raw HTML format (using <h2>, <h3>, <p>, <ul>, <li>, <strong>).
                2. DO NOT use markdown code blocks or ```html tags in the output.
                3. Ensure the content is human-like and professional.
                """
                
                response = model.generate_content(prompt)
                
                # Handling potential empty response
                if response.text:
                    article_content = response.text
                    st.success("Generation Complete!")
                    
                    tab1, tab2 = st.tabs(["Preview", "HTML Source"])
                    with tab1:
                        st.markdown(article_content, unsafe_allow_html=True)
                    with tab2:
                        st.code(article_content, language="html")
                else:
                    st.error("Model returned an empty response. Please check your prompt or API limits.")
                    
        except Exception as e:
            # Check if it's a model name issue and provide feedback
            st.error(f"Error: {e}")
            st.write("Tip: If the error persists, check if your API Key is restricted to specific models in Google AI Studio.")
