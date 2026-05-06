import streamlit as st
from openai import OpenAI

# Page Config
st.set_page_config(page_title="Professional SEO Content Engine", layout="wide")

# دریافت کلید امنیتی از بخش Secrets استریم‌لیت (برای جلوگیری از لو رفتن در گیت‌هاب)
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("Please add your OPENAI_API_KEY to Streamlit Secrets.")
    st.stop()

st.title("🚀 Professional SEO Content Engine")
st.info("System Status: Online | Powered by OpenAI GPT-4o")

# Sidebar for Settings
with st.sidebar:
    st.header("Global Settings")
    tone = st.selectbox("Tone of Voice", ["Professional", "Informative", "Casual", "Technical", "Authoritative"])
    word_count = st.number_input("Target Word Count", min_value=300, max_value=5000, value=1000, step=100)

# Main Input Fields
col1, col2 = st.columns(2)
with col1:
    article_title = st.text_input("Article Title", placeholder="e.g. Best Dental Implants in Los Angeles")
    keywords = st.text_area("Keywords", placeholder="Enter keywords separated by commas...")
with col2:
    headings = st.text_area("Suggested Headings", placeholder="H2, H3 structures...")
    extra_instructions = st.text_area("Extra Instructions", placeholder="e.g. Include a local call-to-action...")

if st.button("Generate HTML Article"):
    if not article_title:
        st.error("Please enter the Article Title.")
    else:
        try:
            with st.spinner("OpenAI is writing your professional article..."):
                client = OpenAI(api_key=API_KEY)
                
                prompt = f"""
                Write a comprehensive, SEO-optimized English article.
                - Title: {article_title}
                - Keywords: {keywords}
                - Structure: {headings}
                - Tone: {tone}
                - Target Length: {word_count} words.
                - Special Instructions: {extra_instructions}
                
                Technical Requirements:
                1. Output ONLY valid HTML tags (<h2>, <h3>, <p>, <ul>, <li>, <strong>).
                2. Do not include <html>, <head>, or <body> tags.
                3. Do not use markdown code blocks (no ```html).
                4. Ensure high readability and professional SEO structure.
                """

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert SEO content writer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                article_html = response.choices[0].message.content
                
                st.success("Generation Complete!")
                
                tab1, tab2 = st.tabs(["👁️ Preview Content", "💻 HTML Source Code"])
                with tab1:
                    st.markdown(article_html, unsafe_allow_html=True)
                with tab2:
                    st.code(article_html, language="html")
                    
        except Exception as e:
            st.error(f"Error: {e}")
