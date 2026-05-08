import streamlit as st
from openai import OpenAI
import time
import json
import streamlit.components.v1 as components

# Advanced Page Configuration
st.set_page_config(
    page_title="Elite AI SEO & GEO Writer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# JavaScript for Copy to Clipboard Functionality
def copy_to_clipboard(text, button_label="Copy"):
    # Using document.execCommand('copy') as per instructions for iframe compatibility
    html_code = f"""
    <button id="copyBtn" style="
        background-color: #007bff; 
        color: white; 
        border: none; 
        padding: 5px 10px; 
        border-radius: 5px; 
        cursor: pointer;
        font-size: 12px;
        margin-bottom: 5px;
        ">
        {button_label}
    </button>
    <textarea id="copyText" style="display:none;">{text}</textarea>
    <script>
    document.getElementById("copyBtn").onclick = function() {{
        var copyText = document.getElementById("copyText");
        copyText.style.display = "block";
        copyText.select();
        document.execCommand("copy");
        copyText.style.display = "none";
        this.innerHTML = "Copied!";
        setTimeout(() => {{ this.innerHTML = "{button_label}"; }}, 2000);
    }}
    </script>
    """
    components.html(html_code, height=45)

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #218838; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Persistence
if "generated_data" not in st.session_state:
    st.session_state.generated_data = None

# Check for API Key
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("Error: OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

st.title("🚀 SEO & GEO Content Engine")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Content Strategy")
    language = st.selectbox("Language", ["English", "Persian", "Spanish", "French", "German"])
    industry = st.selectbox("Industry", ["Legal", "Medical", "Travel", "Real Estate", "Technology", "Finance"])
    search_intent = st.selectbox("Search Intent", ["Informational", "Transactional", "Navigational", "Commercial"])
    tone = st.selectbox("Tone", ["Professional", "Informative", "Casual", "Technical", "Authoritative"])
    word_count = st.select_slider("Target Words", options=[300, 500, 800, 1000, 1500, 2000, 2500], value=1000)
    
    if st.button("🗑️ Clear Results", type="secondary"):
        st.session_state.generated_data = None
        st.rerun()

# Input Section
col1, col2 = st.columns([1, 1])
with col1:
    article_title = st.text_input("Article Title", placeholder="Main Headline (H1)")
    target_audience = st.text_input("Target Audience", placeholder="Who are we writing for?")
    primary_keyword = st.text_input("Primary Keyword")
    secondary_keywords = st.text_area("Secondary Keywords", placeholder="Comma separated...")
with col2:
    lsi_keywords = st.text_area("LSI Keywords", placeholder="Comma separated...")
    suggested_headings = st.text_area("Suggested Headings")
    extra_instructions = st.text_area("Extra Instructions & GEO Data")

# Generation Logic
if st.button("✨ GENERATE ELITE CONTENT"):
    if not article_title or not primary_keyword:
        st.warning("Please fill required fields.")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            system_prompt = f"Elite SEO/GEO strategist and conversion writer. Industry: {industry}. Language: {language}."
            user_prompt = f"""
            Write a 100% unique, authoritative, E-E-A-T article for {industry}.
            H1: {article_title}. Audience: {target_audience}. 
            Intent: {search_intent}. Tone: {tone}. Length: {word_count}.
            Include 3 FAQs, GEO Optimization (citations/stats), no em-dashes, short paragraphs.
            Humanize content perfectly.
            
            Return JSON: 
            {{"meta_title": "...", "meta_description": "...", "article_html": "..."}}
            
            Keywords: {primary_keyword}, {secondary_keywords}, {lsi_keywords}.
            Extra: {extra_instructions}
            """
            
            with st.spinner("⏳ Strategizing and Writing..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.7
                )
                st.session_state.generated_data = json.loads(response.choices[0].message.content)
                st.success("Content Strategy Applied Successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Results Display (Persistent via Session State)
if st.session_state.generated_data:
    data = st.session_state.generated_data
    st.markdown("---")
    st.header("📋 Generated Strategy & Content")
    
    # Meta Info Row
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.write("**Meta Title**")
        copy_to_clipboard(data.get("meta_title", ""))
        st.text_input("Edit Title", value=data.get("meta_title", ""), key="mt_edit", label_visibility="collapsed")
    with m_col2:
        st.write("**Meta Description**")
        copy_to_clipboard(data.get("meta_description", ""))
        st.text_area("Edit Description", value=data.get("meta_description", ""), height=68, key="md_edit", label_visibility="collapsed")

    # Article Content Section
    st.write("**Article Body**")
    copy_to_clipboard(data.get("article_html", ""), "Copy Full HTML")
    
    tab_preview, tab_html = st.tabs(["👁️ Preview Content", "💻 HTML Code Source"])
    
    with tab_preview:
        st.markdown(data.get("article_html", ""), unsafe_allow_html=True)
    
    with tab_html:
        st.text_area("HTML Source (Editable)", value=data.get("article_html", ""), height=500, key="body_edit")
        st.download_button(
            label="📥 Download HTML File",
            data=data.get("article_html", ""),
            file_name=f"{article_title.lower().replace(' ', '_')}.html",
            mime="text/html"
        )
