import streamlit as st
import requests
import json

# Page Config
st.set_page_config(page_title="Professional SEO Content Engine", layout="wide")

# Fixed API Key
API_KEY = "AIzaSyA-qdNkgPPL31NkuOeHDyF5ducJRuD-0LU"

st.title("🚀 Professional SEO Content Engine")
st.info("Generating SEO-optimized articles using direct Google API connection.")

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
            with st.spinner("Connecting to Google AI..."):
                # We try v1beta which is currently the most compatible for 1.5-flash
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Write a professional SEO article in English.\nTitle: {article_title}\nKeywords: {keywords}\nStructure: {headings}\nTone: {tone}\nTarget Length: {word_count} words.\nInstructions: {extra_instructions}\n\nFormat: Return ONLY the content wrapped in HTML tags (h2, h3, p, ul, li, strong). No markdown blocks."
                        }]
                    }]
                }
                
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                result = response.json()

                if response.status_code == 200:
                    article_text = result['candidates'][0]['content']['parts'][0]['text']
                    st.success("Generation Complete!")
                    
                    tab1, tab2 = st.tabs(["Preview", "HTML Source"])
                    with tab1:
                        st.markdown(article_text, unsafe_allow_html=True)
                    with tab2:
                        st.code(article_text, language="html")
                else:
                    error_msg = result.get('error', {}).get('message', 'Unknown Error')
                    st.error(f"API Error: {error_msg}")
                    st.write("Tip: If you see 'not found', Google might have changed the endpoint. I will help you fix it.")
                
        except Exception as e:
            st.error(f"System Error: {str(e)}")
