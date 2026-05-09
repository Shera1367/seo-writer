import streamlit as st
from openai import OpenAI
import time
import json
import streamlit.components.v1 as components
import re

st.set_page_config(
    page_title="Elite AI SEO & GEO Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    # We use st.secrets to hide the key from GitHub scanners
    API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("❌ API Key not found! Please add 'OPENAI_API_KEY' to your Streamlit Secrets dashboard.")
    st.stop()

def strip_html(html_string):
    """Removes HTML tags for word count processing."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_string)

def copy_to_clipboard(content, button_label="Copy", key_suffix="", is_html=False):
    """JavaScript-based copy function supporting HTML and Rich Text."""
    safe_content = content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$').replace('"', '\\"')
    if is_html:
        # Standard copy for code
        js_code = f"""
        var textArea = document.createElement("textarea");
        textArea.value = `{safe_content}`;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("copy");
        document.body.removeChild(textArea);
        """
    else:
        # Rich Text copy to preserve headers/formatting for Word/WordPress
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
        background-color: #007bff; color: white; border: none; padding: 8px 16px; 
        border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 600;
        margin-bottom: 8px; transition: all 0.2s; width: 100%;
        ">
        {button_label}
    </button>
    <script>
    document.getElementById("copyBtn{key_suffix}").onclick = function() {{
        {js_code}
        this.innerHTML = "✓ Copied";
        this.style.backgroundColor = "#28a745";
        setTimeout(() => {{ 
            this.innerHTML = "{button_label}"; 
            this.style.backgroundColor = "#007bff";
        }}, 2000);
    }}
    </script>
    """
    components.html(html_button, height=48)

if "research_data" not in st.session_state:
    st.session_state.research_data = None
if "generated_data" not in st.session_state:
    st.session_state.generated_data = None

st.markdown("""
<style>
    .main { background-color: #f9fafb; }
    .deliverable-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .keyword-pill {
        display: inline-block;
        background: #eff6ff;
        color: #1d4ed8;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 4px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid #dbeafe;
    }
    .banner-container {
        width: 100%;
        height: 350px;
        overflow: hidden;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
    }
    .banner-container img { width: 100%; height: 100%; object-fit: cover; }
    .rendered-content h1 { color: #111827; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Elite SEO & GEO Content Engine")
st.markdown("<p style='color: #6b7280; margin-top: -15px;'>Two-Phase Professional AI Writing Platform</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Global Strategy")
    language = st.selectbox("Language", ["English", "Persian", "Spanish", "French", "German"])
    industry = st.selectbox("Industry", ["Legal", "Medical", "Travel", "Real Estate", "Technology", "Finance", "E-commerce"])
    business_name = st.text_input("Business Name", placeholder="e.g. Deldar Legal")
    target_audience = st.text_input("Target Audience", placeholder="e.g. Accident victims in CA")
    
    st.divider()
    if st.button("🗑️ Reset All Progress", type="secondary"):
        st.session_state.research_data = None
        st.session_state.generated_data = None
        st.rerun()

tab_research, tab_generator = st.tabs(["🔍 Phase 1: Research", "✨ Phase 2: Elite Writing"])

with tab_research:
    st.subheader("Topic Discovery & Structure")
    seed_topic = st.text_input("Enter Topic Idea", placeholder="e.g. Best Divorce Lawyer in San Francisco")
    
    if st.button("🔍 START STRATEGIC RESEARCH"):
        if not seed_topic or not business_name:
            st.warning("Please enter the Topic and Business Name.")
        else:
            try:
                client = OpenAI(api_key=API_KEY)
                res_prompt = f"""
                Industry: {industry}. Brand: {business_name}. Topic: "{seed_topic}".
                Generate: 3 High-CTR Magnetic Headlines, 1 Primary Keyword, 5 Secondary Keywords, 10 LSI Keywords, and a deep-dive H2-H4 outline.
                Return ONLY JSON: {{"headlines": [], "primary": "", "secondary": "", "lsi": "", "structure_text": ""}}
                """
                with st.spinner("⏳ Analyzing search landscape..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": res_prompt}],
                        response_format={"type": "json_object"}
                    )
                    st.session_state.research_data = json.loads(response.choices[0].message.content)
                    st.success("Research Complete! Values transferred to Phase 2.")
            except Exception as e:
                st.error(f"Research Error: {e}")

    if st.session_state.research_data:
        res = st.session_state.research_data
        st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
        st.write("**Magnetic Headlines:**")
        for h in res.get('headlines', []): st.info(h)
        st.write("**Primary Keyword:**", res.get('primary', ''))
        st.write("**Suggested Outline:**")
        st.code(res.get('structure_text', ''))
        st.markdown("</div>", unsafe_allow_html=True)

with tab_generator:
    res_data = st.session_state.research_data or {}
    col_l, col_r = st.columns(2)
    with col_l:
        article_title = st.text_input("Final H1 Title", value=res_data.get("headlines", [""])[0] if res_data else "")
        primary_k = st.text_input("Primary Keyword (H1)", value=res_data.get("primary", "") if res_data else "")
        secondary_k = st.text_area("Secondary Keywords", value=res_data.get("secondary", "") if res_data else "")
    with col_r:
        lsi_k = st.text_area("LSI Keywords", value=res_data.get("lsi", "") if res_data else "")
        headings_k = st.text_area("Heading Hierarchy (H2-H4)", value=res_data.get("structure_text", "") if res_data else "")
    
    search_intent = st.selectbox("Search Intent", ["Informational", "Transactional", "Commercial"])
    word_count_goal = st.select_slider("Target Words", [500, 1000, 1500, 2000], value=1000)

    if st.button("✨ GENERATE HUMANIZED ELITE ARTICLE"):
        if not article_title or not primary_k:
            st.warning("H1 Title and Primary Keyword are required.")
        else:
            try:
                client = OpenAI(api_key=API_KEY)
                with st.spinner("⏳ Synthesizing deep-dive content and DALL-E 3 banner..."):
                    # Text Generation
                    sys_p = f"You are an elite SEO/GEO Investigative Journalist for {industry}."
                    user_p = f"""
                    Write a 100% unique, human-grade deep-dive for {business_name} in {language}.
                    Title: {article_title}. Target words: {word_count_goal}. Intent: {search_intent}.
                    Structure: {headings_k}. 
                    Strict Rules: No em-dashes. Vary sentence lengths. No clichés. 
                    Include 2 .gov/.edu links. Include 3 FAQs. Use <strong> and <u> tags.
                    Return JSON: {{'meta_title': '', 'meta_description': '', 'article_html': ''}}
                    """
                    
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "system", "content": sys_p}, {"role": "user", "content": user_p}],
                        response_format={"type": "json_object"}
                    )
                    gen_data = json.loads(response.choices[0].message.content)
                    
                    # Image Generation
                    img_prompt = f"Professional high-resolution realistic photography for '{article_title}' in {industry} field, cinematic lighting, wide angle, no text."
                    img_res = client.images.generate(model="dall-e-3", prompt=img_prompt, size="1792x1024", quality="hd")
                    gen_data["image_url"] = img_res.data[0].url
                    
                    st.session_state.generated_data = gen_data
                    st.success("Deliverables Generated!")
            except Exception as e:
                st.error(f"Generation Error: {e}")

if st.session_state.generated_data:
    data = st.session_state.generated_data
    if "image_url" in data:
        st.markdown(f'<div class="banner-container"><img src="{data["image_url"]}"></div>', unsafe_allow_html=True)

    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.write("**Meta Title**")
        st.text_input("Title", value=data.get("meta_title", ""), label_visibility="collapsed")
        copy_to_clipboard(data.get("meta_title", ""), "📋 Copy Title", "mt", True)
    with m2:
        st.write("**Meta Description**")
        st.text_area("Desc", value=data.get("meta_description", ""), height=68, label_visibility="collapsed")
        copy_to_clipboard(data.get("meta_description", ""), "📋 Copy Desc", "md", True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.write("**Article Content**")
    c1, c2, _ = st.columns([1, 1, 2])
    with c1: copy_to_clipboard(data.get("article_html", ""), "💾 Copy HTML Code", "html", True)
    with c2: copy_to_clipboard(data.get("article_html", ""), "👤 Copy Formatted Text", "rich", False)
    
    t1, t2 = st.tabs(["👁️ Preview", "💻 HTML Source"])
    with t1: st.markdown(f"<div class='rendered-content'>{data.get('article_html', '')}</div>", unsafe_allow_html=True)
    with t2: st.text_area("Code", value=data.get("article_html", ""), height=400, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    actual_words = len(strip_html(data.get("article_html", "")).split())
    st.markdown(f"<div style='background:#f3f4f6;padding:12px;border-radius:8px;'>Audit: {actual_words} words | Brand: {business_name} | Grade: Elite</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 11px; margin-top: 60px;'>Elite SEO & GEO Engine | Powered by OpenAI | © 2026</p>", unsafe_allow_html=True)
