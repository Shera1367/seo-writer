import streamlit as st
from openai import OpenAI
import time
import json
import streamlit.components.v1 as components
import re

# Advanced Page Configuration
st.set_page_config(
    page_title="Elite AI SEO & GEO Writer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper to strip HTML tags for plain text word counting
def strip_html(html_string):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_string)

def copy_to_clipboard(content, button_label="Copy", key_suffix="", is_html=False):
    safe_content = content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$').replace('"', '\\"')
    
    if is_html:
        js_code = f"""
        var textArea = document.createElement("textarea");
        textArea.value = `{safe_content}`;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("copy");
        document.body.removeChild(textArea);
        """
    else:
        js_code = f"""
        var container = document.createElement("div");
        container.innerHTML = `{safe_content}`;
        container.style.position = "fixed";
        container.style.pointerEvents = "none";
        container.style.opacity = 0;
        document.body.appendChild(container);
        window.getSelection().removeAllRanges();
        var range = document.createRange();
        range.selectNode(container);
        window.getSelection().addRange(range);
        document.execCommand("copy");
        window.getSelection().removeAllRanges();
        document.body.removeChild(container);
        """

    html_button = f"""
    <button id="copyBtn{key_suffix}" style="
        background-color: #007bff; color: white; border: none; padding: 5px 12px; 
        border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500;
        margin-bottom: 8px; transition: background 0.2s;
        ">
        {button_label}
    </button>
    <script>
    document.getElementById("copyBtn{key_suffix}").onclick = function() {{
        {js_code}
        this.innerHTML = "Copied!";
        this.style.backgroundColor = "#28a745";
        setTimeout(() => {{ 
            this.innerHTML = "{button_label}"; 
            this.style.backgroundColor = "#007bff";
        }}, 2000);
    }}
    </script>
    """
    components.html(html_button, height=45)

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.2em;
        background-color: #28a745; color: white; font-weight: bold;
        border: none; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { background-color: #218838; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "generated_data" not in st.session_state:
    st.session_state.generated_data = None

# API Key check
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("Error: OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

st.title("🚀 SEO & GEO Content Engine")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Strategy")
    language = st.selectbox("Language", ["English", "Persian", "Spanish", "French", "German"])
    industry = st.selectbox("Industry", ["Legal", "Medical", "Travel", "Real Estate", "Technology", "Finance", "E-commerce"])
    search_intent = st.selectbox("Search Intent", ["Informational", "Transactional", "Navigational", "Commercial"])
    tone = st.selectbox("Tone", ["Professional", "Informative", "Casual", "Technical", "Authoritative", "Conversational"])
    word_count = st.select_slider("Target Words", options=[300, 500, 800, 1000, 1500, 2000, 2500], value=1000)
    
    if st.button("🗑️ Clear Results", type="secondary"):
        st.session_state.generated_data = None
        st.rerun()

col1, col2 = st.columns([1, 1])
with col1:
    article_title = st.text_input("Article Title", placeholder="Main Headline (H1)")
    business_name = st.text_input("Business/Brand Name", placeholder="e.g. Golden State Dental")
    target_audience = st.text_input("Target Audience", placeholder="e.g. Patients in Sacramento")
    primary_keyword = st.text_input("Primary Keyword")
    secondary_keywords = st.text_area("Secondary Keywords", placeholder="Comma or Enter separated...")
with col2:
    lsi_keywords = st.text_area("LSI Keywords", placeholder="Contextual synonyms...")
    suggested_headings = st.text_area("Suggested Headings", placeholder="Intro\nServices\nWhy Us\nConclusion")
    extra_instructions = st.text_area("Extra Instructions & GEO Data", placeholder="Include neighborhoods, highways, or specific local laws...")

if st.button("✨ GENERATE ELITE HUMANIZED CONTENT"):
    if not article_title or not primary_keyword or not business_name:
        st.warning("Please fill required fields (Title, Brand, and Primary Keyword).")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            
            system_prompt = f"""
            You are an elite investigative journalist and a high-ticket practitioner in the {industry} field for {business_name}.
            You write with the weight of 20 years of real-world experience. You despise robotic, generic AI writing.
            Language: {language}.
            """
            
            user_prompt = f"""
            Write an ULTIMATE, human-grade deep-dive SEO article for {business_name}.
            
            STRICT HUMANIZATION & ANTI-AI PROTOCOL:
            1. NO CLICHÉS: Never start with "Imagine this". Do not use phrases like "In the ever-evolving world", "Unleash", "Delve", "The result?", "Moreover", or "Furthermore".
            2. PERPLEXITY & BURSTINESS: Vary sentence length significantly. Follow a long, complex sentence with a very short, punchy one.
            3. HYPER-LOCAL GEO: Refer to specific neighborhoods, nearby highways, or local landmarks if provided.
            4. FIRST-PERSON EXPERTISE: Use 'I' or 'We'. Speak like a practitioner, not an observer.
            5. FORMATTING EXCELLENCE: Use <strong> for critical terms and <u> for specific emphasis where needed.
            6. AUTHORITATIVE QUOTE: Include exactly one relevant, inspiring quote from a famous world figure (philosopher, scientist, or industry pioneer) related to {industry}, wrapped in <blockquote> tags.
            7. HONEST FAQ: Write 3 FAQs that sound like a real conversation. If it's about cost, be direct and honest.
            8. NO EM-DASHES: Do not use (—) anywhere. Use short paragraphs.
            
            CORE DATA:
            - Title: {article_title} (Transform into a magnetic, high-CTR headline).
            - Brand: {business_name}.
            - Primary Keyword: {primary_keyword}.
            - Word Count: {word_count} words.
            - Authority: Include 2 external outbound links to .gov or .edu sources.
            
            OUTPUT:
            Return ONLY a JSON object: 
            {{"meta_title": "...", "meta_description": "...", "article_html": "..."}}
            
            Keywords & Structure: {secondary_keywords}, {lsi_keywords}, {suggested_headings}.
            Extra Data: {extra_instructions}
            """
            
            with st.spinner(f"⏳ Strategizing human-grade content for {business_name}..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.85
                )
                st.session_state.generated_data = json.loads(response.choices[0].message.content)
                st.success("Humanized Content Strategy Applied!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if st.session_state.generated_data:
    data = st.session_state.generated_data
    st.markdown("---")
    st.header(f"📋 Professional Content: {business_name}")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.write("**Meta Title**")
        copy_to_clipboard(data.get("meta_title", ""), key_suffix="meta_t", is_html=True)
        st.text_input("Edit Title", value=data.get("meta_title", ""), key="mt_edit", label_visibility="collapsed")
    with m_col2:
        st.write("**Meta Description**")
        copy_to_clipboard(data.get("meta_description", ""), key_suffix="meta_d", is_html=True)
        st.text_area("Edit Description", value=data.get("meta_description", ""), height=68, key="md_edit", label_visibility="collapsed")

    st.write("**Article Body**")
    c1, c2, _ = st.columns([1.2, 1.2, 4])
    with c1:
        copy_to_clipboard(data.get("article_html", ""), "💾 Copy HTML Code", key_suffix="body_html", is_html=True)
    with c2:
        copy_to_clipboard(data.get("article_html", ""), "👤 Copy Formatted Text", key_suffix="body_rich", is_html=False)
    
    tab_preview, tab_html = st.tabs(["👁️ Preview Content", "💻 HTML Code Source"])
    with tab_preview:
        st.markdown(data.get("article_html", ""), unsafe_allow_html=True)
    with tab_html:
        st.text_area("HTML Source", value=data.get("article_html", ""), height=500, key="body_edit")
        st.download_button("📥 Download HTML file", data.get("article_html", ""), file_name=f"article.html")
    
    # Audit Stats
    actual_words = len(strip_html(data.get("article_html", "")).split())
    st.markdown("---")
    st.markdown(f"**Final Human Audit:** Word Count: `{actual_words}` | Brand: `{business_name}` | SEO: `Humanized` | Quotes: `Active`")

st.markdown("<p style='text-align: center; color: grey; font-size: 11px; margin-top: 50px;'>Elite SEO & GEO Engine | Sheragim.biz | © 2026</p>", unsafe_allow_html=True)
