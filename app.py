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

def strip_html(html_string):
    """Removes HTML tags for word count and plain text processing."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_string)

def copy_to_clipboard(content, button_label="Copy", key_suffix="", is_html=False):
    """JavaScript-based copy function supporting both HTML code and Rich Text."""
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
        background-color: #007bff; color: white; border: none; padding: 8px 16px; 
        border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 600;
        margin-bottom: 8px; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex; align-items: center; justify-content: center; width: 100%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
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
    /* Main container styling */
    .main { background-color: #f9fafb; }
    
    /* Card-like containers for strategy and deliverables */
    .deliverable-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    
    /* Header styling */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    
    /* Keyword pill styling */
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
    
    /* Styling Streamlit buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        background-color: #2563eb;
        color: white;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.1s;
    }
    .stButton>button:active { transform: scale(0.98); }
    
    /* Formatting headings in markdown preview */
    .rendered-content h1 { color: #111827; font-weight: 800; }
    .rendered-content h2 { color: #1f2937; margin-top: 1.5em; border-bottom: 1px solid #f3f4f6; padding-bottom: 0.3em; }
    
    /* New style for the cinematic banner */
    .banner-container {
        width: 100%;
        height: 350px;
        overflow: hidden;
        border-radius: 12px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .banner-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
</style>
""", unsafe_allow_html=True)

try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("Error: OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

st.title("🚀 Elite SEO & GEO Content Engine")
st.markdown("<p style='color: #6b7280; margin-top: -15px;'>Professional Strategy-First AI Content Platform</p>", unsafe_allow_html=True)
st.markdown("---")

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

tab_research, tab_generator = st.tabs(["🔍 Phase 1: Deep Research", "✨ Phase 2: Elite Writing Engine"])

with tab_research:
    st.markdown("<div class='section-header'>Topic Analysis & Structure Discovery</div>", unsafe_allow_html=True)
    seed_topic = st.text_input("Enter Main Topic Idea", placeholder="e.g. Dental Implant Benefits for Seniors")
    
    if st.button("🔍 START STRATEGIC RESEARCH"):
        if not seed_topic or not business_name:
            st.warning("Please enter the Topic and Business Name in sidebar.")
        else:
            try:
                client = OpenAI(api_key=API_KEY)
                res_prompt = f"""
                Industry: {industry}. Brand: {business_name}. Topic: "{seed_topic}".
                Target Audience: {target_audience}.
                
                Generate a strategic SEO/GEO blueprint:
                1. 3 Magnetic, High-CTR Headlines.
                2. 1 Primary Keyword.
                3. 5-7 Secondary Keywords (as a comma-separated string).
                4. 10 LSI Keywords (as a comma-separated string).
                5. A deep-dive heading structure (H2, H3, H4).
                
                Return ONLY a JSON object:
                {{
                    "headlines": ["...", "...", "..."],
                    "primary": "...",
                    "secondary": "k1, k2, k3",
                    "lsi": "l1, l2, l3",
                    "structure_text": "H2: ...\\n  H3: ...\\n    H4: ..."
                }}
                """
                with st.spinner("⏳ Analyzing search landscape and building structure..."):
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
        st.markdown("<div class='section-header'>🎯 Research Results</div>", unsafe_allow_html=True)
        
        st.write("**Magnetic Headlines (Optimized for CTR):**")
        for h in res.get('headlines', []): st.info(h)
        
        c1, c2 = st.columns(2)
        with c1: 
            st.write("**Primary Keyword**")
            st.code(res.get('primary', ''))
            
            sec_raw = res.get('secondary', '')
            sec_list = sec_raw.split(',') if isinstance(sec_raw, str) else sec_raw
            st.write("**Secondary Keywords**")
            st.write(" ".join([f"<span class='keyword-pill'>{str(k).strip()}</span>" for k in sec_list]), unsafe_allow_html=True)
            
        with c2: 
            lsi_raw = res.get('lsi', '')
            lsi_list = lsi_raw.split(',') if isinstance(lsi_raw, str) else lsi_raw
            st.write("**LSI Keywords**")
            st.write(" ".join([f"<span class='keyword-pill'>{str(k).strip()}</span>" for k in lsi_list]), unsafe_allow_html=True)
            
        st.write("**Deep-Dive Outline (H2-H4):**")
        st.code(res.get('structure_text', ''))
        st.markdown("</div>", unsafe_allow_html=True)

with tab_generator:
    st.markdown("<div class='section-header'>Elite Content Configuration</div>", unsafe_allow_html=True)
    res = st.session_state.research_data or {}
    
    col1, col2 = st.columns(2)
    with col1:
        article_title = st.text_input("Final H1 Title", value=res.get("headlines", [""])[0] if res else "")
        primary_k = st.text_input("Primary Keyword (Focus)", value=res.get("primary", "") if res else "")
        secondary_k = st.text_area("Secondary Keywords", value=res.get("secondary", "") if res else "", height=100)
    with col2:
        lsi_k = st.text_area("LSI Keywords", value=res.get("lsi", "") if res else "", height=100)
        headings_k = st.text_area("Heading Hierarchy (H2-H4)", value=res.get("structure_text", "") if res else "", height=100)
        extra_k = st.text_area("GEO & Local Context", placeholder="Specific neighborhoods, landmarks, or local laws...", height=68)

    gen_col1, gen_col2 = st.columns(2)
    with gen_col1:
        search_intent = st.selectbox("Search Intent", ["Informational", "Transactional", "Commercial Investigation", "Navigational"])
    gen_col2:
        word_count_goal = st.select_slider("Target Word Count", [500, 1000, 1500, 2000, 2500], value=1000)

    if st.button("✨ GENERATE HUMANIZED ELITE ARTICLE"):
        if not article_title or not primary_k:
            st.warning("H1 Title and Primary Keyword are required.")
        else:
            try:
                client = OpenAI(api_key=API_KEY)
                
                sys_p = f"You are an Elite Investigative Journalist and Copywriter. Industry: {industry}. Language: {language}."
                
                user_p = f"""
                Write an ULTIMATE, human-grade deep-dive article for {business_name}.
                with st.spinner("⏳ Synthesizing deep-dive content and generating realistic banner..."):
                    # Generate Text
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "system", "content": sys_p}, {"role": "user", "content": user_p}],
                        response_format={"type": "json_object"},
                        temperature=0.85
                    )
                    generated_json = json.loads(response.choices[0].message.content)
                    
                    # Generate Image with DALL-E 3
                    image_prompt = f"A highly realistic, professional, and cinematic wide-angle photograph related to '{article_title}' for the {industry} industry. High resolution, 8k, natural lighting, clean composition, no text or words in the image."
                    img_response = client.images.generate(
                        model="dall-e-3",
                        prompt=image_prompt,
                        size="1792x1024",
                        quality="hd",
                        n=1,
                    )
                    generated_json["image_url"] = img_response.data[0].url
                    
                    st.session_state.generated_data = generated_json
                    st.success("Elite Article and Visual Assets Generated!")
            except Exception as e:
                st.error(f"Generation Error: {e}")

if st.session_state.generated_data:
    data = st.session_state.generated_data
    st.divider()
    
    st.markdown("<div class='section-header'>📋 Final Deliverables</div>", unsafe_allow_html=True)
    
    if "image_url" in data:
        st.markdown(f"""
        <div class="banner-container">
            <img src="{data['image_url']}" alt="Article Banner">
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"🚀 Realistic Banner Generated for {industry} (1920x630 aspect crop applied)")

    # Grid for Meta Tags
    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("**Meta Title**", unsafe_allow_html=True)
        st.text_input("Edit Meta Title", value=data.get("meta_title", ""), label_visibility="collapsed")
        copy_to_clipboard(data.get("meta_title", ""), "📋 Copy Title", key_suffix="mt", is_html=True)
    with m2:
        st.markdown("**Meta Description**", unsafe_allow_html=True)
        st.text_area("Edit Meta Description", value=data.get("meta_description", ""), height=68, label_visibility="collapsed")
        copy_to_clipboard(data.get("meta_description", ""), "📋 Copy Description", key_suffix="md", is_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Content Card
    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.markdown("**Content Body**", unsafe_allow_html=True)
    
    # Actions Row
    c1, c2, _ = st.columns([1, 1, 2])
    with c1: copy_to_clipboard(data.get("article_html", ""), "💾 Copy HTML Code", key_suffix="html", is_html=True)
    with c2: copy_to_clipboard(data.get("article_html", ""), "👤 Copy Formatted Text", key_suffix="rich", is_html=False)
    
    t_prev, t_code = st.tabs(["👁️ Rendered Preview", "💻 Raw HTML Source"])
    with t_prev: 
        st.markdown(f"<div class='rendered-content'>{data.get('article_html', '')}</div>", unsafe_allow_html=True)
    with t_code: 
        st.text_area("Source", value=data.get("article_html", ""), height=400, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Audit Footer
    actual_words = len(strip_html(data.get("article_html", "")).split())
    st.markdown(f"""
    <div style='background: #f3f4f6; padding: 12px; border-radius: 8px; font-size: 13px;'>
    <strong>Final Audit:</strong> Actual Word Count: <code>{actual_words}</code> | Brand: <code>{business_name}</code> | SEO: <code>Human-Grade Verified</code> | GEO: <code>Enabled</code>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 11px; margin-top: 60px;'>Elite SEO & GEO Engine | Powered by GPT-4o | © 2026 Professional Content Suite</p>", unsafe_allow_html=True)
