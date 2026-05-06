import streamlit as st
import requests
import json

# Page Config
st.set_page_config(page_title="Professional SEO Content Engine", layout="wide")

# --- PLACE YOUR NEW API KEY HERE ---
API_KEY = "کلید_جدید_را_اینجا_بگذارید"

st.title("🚀 Professional SEO Content Engine")
st.info("Using Gemini 1.5 Flash - Optimized for Free Tier Users")

# Sidebar
with st.sidebar:
    st.header("Global Settings")
    tone = st.selectbox("Tone of Voice", ["Professional", "Informative", "Casual", "Technical", "Authoritative"])
    word_count = st.number_input("Target Word Count", min_value=300, max_value=5000, value=1000)

# Main Input Fields
col1, col2 = st.columns(2)
with col1:
    article_title = st.text_input("Article Title", placeholder="e.g. Benefits of Dental Implants")
    keywords = st.text_area("Keywords", placeholder="SEO, Dental, Health...")
with col2:
    headings = st.text_area("Suggested Headings", placeholder="Introduction, Procedures, Cost...")
    extra_instructions = st.text_area("Extra Instructions", placeholder="Add 3 FAQ questions at the end.")

if st.button("Generate HTML Article"):
    if not article_title:
        st.error("Please enter the Article Title.")
    elif "AIza" not in API_KEY:
        st.error("Please update the API KEY in the code.")
    else:
        try:
            with st.spinner("Writing..."):
                # این آدرس دقیقاً برای مدل‌های رایگان بهینه شده است
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
                    st.success("Success!")
                    
                    tab1, tab2 = st.tabs(["Preview", "HTML Source"])
                    with tab1:
                        st.markdown(article_text, unsafe_allow_html=True)
                    with tab2:
                        st.code(article_text, language="html")
                else:
                    st.error(f"Error: {result.get('error', {}).get('message', 'Check API Status')}")
                
        except Exception as e:
            st.error(f"System Error: {str(e)}")
