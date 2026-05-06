import streamlit as st
from openai import OpenAI

# Page Config
st.set_page_config(page_title="Professional SEO Writer", layout="wide")

# Your Paid OpenAI API Key
API_KEY = "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"
st.title("🚀 Professional SEO Content Engine")
st.info("System Status: Online | Powered by OpenAI GPT-4o")

# Sidebar
with st.sidebar:
    st.header("Settings")
    tone = st.selectbox("Tone", ["Professional", "Informative", "Casual", "Technical"])
    word_count = st.number_input("Words", min_value=300, max_value=5000, value=1000)

# Main UI
col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Article Title")
    keywords = st.text_area("Keywords")
with col2:
    headings = st.text_area("Suggested Headings")
    extra = st.text_area("Instructions")

if st.button("Generate HTML Article"):
    if not title:
        st.error("Please enter a title.")
    else:
        try:
            with st.spinner("Writing..."):
                client = OpenAI(api_key=API_KEY)
                prompt = f"Write an SEO article. Title: {title}. Keywords: {keywords}. Headings: {headings}. Tone: {tone}. Length: {word_count} words. Extra: {extra}. Format: Raw HTML (h2, h3, p, ul, li)."
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                content = response.choices[0].message.content
                st.success("Done!")
                tab1, tab2 = st.tabs(["Preview", "HTML Code"])
                with tab1:
                    st.markdown(content, unsafe_allow_html=True)
                with tab2:
                    st.code(content, language="html")
        except Exception as e:
            st.error(f"Error: {e}")
