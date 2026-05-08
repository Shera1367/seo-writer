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

# JavaScript for Copy to Clipboard Functionality (Supports Rich Text)
def copy_to_clipboard(content, button_label="Copy", key_suffix="", is_html=False):
    # For Rich Text copying, we use a hidden div and select its content
    # For HTML code copying, we use a textarea
    safe_content = content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$').replace('"', '\\"')
    
    if is_html:
        # Standard copy for code/plain text
        js_code = f"""
        var textArea = document.createElement("textarea");
        textArea.value = `{safe_content}`;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("copy");
        document.body.removeChild(textArea);
        """
    else:
        # Rich Text copy to preserve headings/formatting
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
        background-color: #007bff; 
        color: white; 
        border: none; 
        padding: 5px 12px; 
        border-radius: 6px; 
        cursor: pointer;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 8px;
        transition: background 0.2s;
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

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.2em;
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
    industry = st.selectbox("Industry", ["Legal", "Medical", "Travel", "Real Estate", "Technology", "Finance", "E-commerce"])
    search_intent = st.selectbox("Search Intent", ["Informational", "Transactional", "Navigational", "Commercial"])
    tone = st.selectbox("Tone", ["Professional", "Informative", "Casual", "Technical", "Authoritative", "Conversational"])
    word_count = st.select_slider("Target Words", options=[300, 500, 800, 1000, 1500, 2000, 2500], value=1000)
    
    if st.button("🗑️ Clear Results", type="secondary"):
        st.session_state.generated_data = None
        st.rerun()

# Input Section
col1, col2 = st.columns([1, 1])
with col1:
    article_title = st.text_input("Article Title", placeholder="Main Headline (H1)")
    business_name = st.text_input("Business/Brand Name", placeholder="e.g. Deldar Legal")
    target_audience = st.text_input("Target Audience", placeholder="e.g. Accident victims in CA")
    primary_keyword = st.text_input("Primary Keyword")
    secondary_keywords = st.text_area("Secondary Keywords", placeholder="Separate with commas or Enter...")
with col2:
    lsi_keywords = st.text_area("LSI Keywords", placeholder="Contextual synonyms...")
    suggested_headings = st.text_area("Suggested Headings", placeholder="Introduction\nSection 1\nSection 2\nConclusion")
    extra_instructions = st.text_area("Extra Instructions & GEO Data", placeholder="Include local data, citations, or specific stats...")

# Generation Logic
if st.button("✨ GENERATE ELITE CONTENT"):
    if not article_title or not primary_keyword or not business_name:
        st.warning("Please fill required fields (Title, Brand, and Primary Keyword).")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            
            # Elite System Persona
            system_prompt = f"You are an elite SEO content strategist, content writer, and conversion copywriter. Expert in {industry}. Language: {language}."
            
            # Comprehensive User Prompt linking all fields
            user_prompt = f"""
            Task: Write an elite, 100% unique, and E-E-A-T compliant SEO article.
            
            BRAND CONTEXT:
            - Business Name: {business_name} (Use this brand name naturally throughout the article to build authority).
            - Industry: {industry}.
            
            HEADLINE OPTIMIZATION:
            - Current Title: "{article_title}". 
            - Action: Transform this into a magnetic, high-CTR H1 headline using power words while keeping the Primary Keyword integrated.
            
            SEO & GEO STRATEGY:
            - Primary Keyword: {primary_keyword} (Focus).
            - Secondary Keywords: {secondary_keywords} (Integrate naturally).
            - LSI Keywords: {lsi_keywords} (Use for semantic richness).
            - Search Intent: {search_intent} (Satisfy this intent fully).
            - GEO Optimization: Include authoritative citations, stats, and data points.
            - External Linking: Include exactly 2 outbound links to highly authoritative sources (e.g., .gov, .edu, or reputable non-profit organizations) that are strictly relevant to the topic. These MUST NOT be commercial competitors.
            
            AUDIENCE & STRUCTURE:
            - Target Audience: {target_audience}.
            - Tone: {tone}.
            - Structure: Follow this outline if provided: {suggested_headings}.
            - Word Count: {word_count}.
            - Introduction (150-200 words): Hook {target_audience} emotionally/logically.
            - Body: Explain the "Why" and "How". No em-dashes (—). Short paragraphs.
            - FAQ: Include 3 optimized FAQs.
            - CTA: A strong, persuasive closing for {business_name}.
            
            FINAL REVIEW:
            Humanize the content. Review for UX, SEO, and GEO standards.
            
            Return ONLY a valid JSON object: 
            {{"meta_title": "...", "meta_description": "...", "article_html": "..."}}
            
            Extra Context: {extra_instructions}
            """
            
            with st.spinner(f"⏳ Strategizing and Writing for {business_name}..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.7
                )
                st.session_state.generated_data = json.loads(response.choices[0].message.content)
                st.success(f"Strategy applied for {business_name}!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Results Display
if st.session_state.generated_data:
    data = st.session_state.generated_data
    st.markdown("---")
    st.header(f"📋 Content for {business_name}")
    
    # Meta Info Row
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.write("**Meta Title**")
        copy_to_clipboard(data.get("meta_title", ""), key_suffix="meta_t", is_html=True)
        st.text_input("Edit Title", value=data.get("meta_title", ""), key="mt_edit", label_visibility="collapsed")
    with m_col2:
        st.write("**Meta Description**")
        copy_to_clipboard(data.get("meta_description", ""), key_suffix="meta_d", is_html=True)
        st.text_area("Edit Description", value=data.get("meta_description", ""), height=68, key="md_edit", label_visibility="collapsed")

    # Article Content Section
    st.write("**Article Body**")
    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        copy_to_clipboard(data.get("article_html", ""), "Copy Code (HTML)", key_suffix="body_html", is_html=True)
    with c2:
        # Copy as Rich Text to preserve formatting/headings
        copy_to_clipboard(data.get("article_html", ""), "Copy Formatted Text", key_suffix="body_rich", is_html=False)
    
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
    
    # Footer Stats
    actual_words = len(strip_html(data.get("article_html", "")).split())
    st.markdown("---")
    st.markdown(f"**Final Audit:** Word Count: `{actual_words}` | Brand: `{business_name}` | Intent: `{search_intent}`")

# Footer
st.markdown("<p style='text-align: center; color: grey; font-size: 12px; margin-top: 50px;'>Elite SEO & GEO Engine | Built for Professional Content Teams | © 2026</p>", unsafe_allow_html=True)
