import streamlit as st
from openai import OpenAI
import time
import json
import streamlit.components.v1 as components
import re
import requests
from io import BytesIO

st.set_page_config(
    page_title="Elite AI SEO & GEO Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("❌ API Key not found! Please add 'OPENAI_API_KEY' to your Streamlit Secrets.")
    st.stop()

def strip_html(html_string):
    """Removes HTML tags for word count auditing."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_string)

def download_image_bytes(url):
    """Fetch image bytes from URL for download button."""
    try:
        response = requests.get(url)
        return response.content
    except:
        return None

def copy_to_clipboard(content, button_label="Copy", key_suffix="", is_html=False):
    """JavaScript-based copy function supporting HTML and Rich Text."""
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
    .banner-container {
        width: 100%;
        height: 400px;
        overflow: hidden;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #e5e7eb;
    }
    .banner-container img { width: 100%; height: 100%; object-fit: cover; }
    .rendered-content h1 { color: #111827; font-weight: 800; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }
    .rendered-content h2 { color: #1f2937; margin-top: 30px; font-weight: 700; }
    .rendered-content p { line-height: 1.8; color: #374151; margin-bottom: 20px; }
    
    .key-takeaways { 
        background: #f0f7ff; 
        border-left: 5px solid #007bff; 
        padding: 20px; 
        border-radius: 8px; 
        margin: 20px 0; 
        color: #1e293b !important; 
    }
    
    .data-table-container { overflow-x: auto; margin: 25px 0; }
    .data-table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        font-family: inherit;
        font-size: 0.95em;
    }
    .data-table th {
        background-color: #3b82f6;
        color: white;
        padding: 15px;
        text-align: left;
    }
    .data-table td {
        padding: 12px 15px;
        border-bottom: 1px solid #e5e7eb;
        color: #1e293b;
    }
    .data-table tr:nth-child(even) { background-color: #f8fafc; }

    /* INFOGRAPHIC STYLING */
    .visual-infographic {
        background: #f8fafc;
        border: 2px dashed #3b82f6;
        padding: 25px;
        border-radius: 15px;
        margin: 30px 0;
    }
    .visual-infographic h3 { color: #1e293b !important; margin-top: 0 !important; margin-bottom: 20px !important; }
    .infographic-step {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        padding: 15px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .step-text { color: #1e293b !important; font-weight: 500; font-size: 1.1em; }
    .step-number {
        background: #3b82f6;
        color: white !important;
        min-width: 35px;
        height: 35px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        font-weight: 900;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Elite SEO & GEO Content Engine")

word_options = list(range(200, 2100, 100))

with st.sidebar:
    st.header("⚙️ Global Strategy")
    language = st.selectbox("Language", ["English", "Persian", "Spanish", "French", "German"])
    industry = st.selectbox("Industry", ["Legal", "Medical", "Travel", "Real Estate", "Technology", "Finance", "E-commerce"])
    business_name = st.text_input("Business Name", placeholder="e.g. My Agency")
    business_url = st.text_input("Business Website URL", placeholder="e.g. https://yoursite.com")
    target_audience = st.text_input("Target Audience", placeholder="e.g. Local customers")
    st.divider()
    sidebar_word_count = st.select_slider("Target Words (Global)", options=word_options, value=1000)
    
    num_images = st.slider("Number of Images", 1, 3, 1)
    include_infographic = st.checkbox("Include Visual Infographic", value=True)
    include_table = st.checkbox("Include Summary/Stats Table", value=True)
    
    st.divider()
    if st.button("🗑️ Reset Application", type="secondary"):
        st.session_state.research_data = None
        st.session_state.generated_data = None
        st.rerun()

st.subheader("Step 1: Strategic Research & Competitor Analysis")
col_s1, col_s2 = st.columns(2)
with col_s1:
    seed_topic = st.text_input("Enter Seed Topic", placeholder="e.g. Benefits of Dental Implants")
with col_s2:
    competitor_links = st.text_area("Competitor URLs (One per line)", placeholder="Paste top ranking links")

if st.button("🔍 START RESEARCH & ANALYSIS"):
    if not seed_topic or not business_name:
        st.warning("Please enter Seed Topic and Business Name.")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            res_prompt = f"Analyze topic '{seed_topic}' for {business_name} ({industry}) and these competitors: {competitor_links}. Generate 3 Headlines (front-load keyword, numbers, brackets [2026]), 1 Primary, 5 Secondary, 10 LSI, and an outline. Return JSON: {{'headlines': [], 'primary': '', 'secondary': [], 'lsi': [], 'structure_text': ''}}"
            with st.spinner("⏳ Analyzing search landscape..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": res_prompt}],
                    response_format={"type": "json_object"}
                )
                raw_res = json.loads(response.choices[0].message.content)
                st.session_state.research_data = {
                    "headline": raw_res.get('headlines', [""])[0],
                    "primary": raw_res.get('primary', ""),
                    "secondary": ", ".join(raw_res.get('secondary', [])) if isinstance(raw_res.get('secondary'), list) else raw_res.get('secondary', ""),
                    "lsi": ", ".join(raw_res.get('lsi', [])) if isinstance(raw_res.get('lsi'), list) else raw_res.get('lsi', ""),
                    "outline": raw_res.get('structure_text', "")
                }
                st.success("Research & Analysis Complete!")
        except Exception as e: st.error(f"Error: {e}")

st.divider()
st.subheader("Step 2: Elite Article Generation")
res = st.session_state.research_data or {}
col_l, col_r = st.columns(2)
with col_l:
    final_h1 = st.text_input("Final H1 Title", value=res.get("headline", ""))
    primary_k = st.text_input("Primary Keyword", value=res.get("primary", ""))
    secondary_k = st.text_area("Secondary Keywords", value=res.get("secondary", ""))
with col_r:
    lsi_k = st.text_area("LSI Keywords", value=res.get("lsi", ""))
    headings_k = st.text_area("Heading Hierarchy", value=res.get("outline", ""), height=130)

search_intent = st.selectbox("Search Intent", ["Informational", "Transactional", "Commercial"])

if st.button("✨ GENERATE HUMANIZED ELITE ARTICLE"):
    if not final_h1 or not primary_k:
        st.warning("H1 and Primary Keyword are required.")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            with st.spinner(f"⏳ Synthesizing elite deep-dive content..."):
                
                table_instr = "MANDATORY: Include a detailed comparison table using: <div class='data-table-container'><table class='data-table'>...</table></div>." if include_table else ""
                
                info_instr = ""
                if include_infographic:
                    info_instr = """
                    MANDATORY: Include a 'Visual Infographic' section. 
                    DO NOT USE <img> TAGS. Use this EXACT HTML structure:
                    <div class='visual-infographic'>
                        <h3>Process Overview</h3>
                        <div class='infographic-step'><div class='step-number'>1</div><div class='step-text'>Step Description</div></div>
                        ...
                    </div>
                    """

                user_p = f"""
                Write a MASTER-LEVEL, high-authority SEO article for {business_name} in {language}. 
                Target Words: {sidebar_word_count} (MANDATORY: You must hit this word count).
                Intent: {search_intent}. 
                H1 Title: {final_h1}. 
                Structure provided: {headings_k}. 
                Website: {business_url}.
                
                CRITICAL DEPTH RULES:
                - EVERY H2, H3, and H4 heading MUST be followed by at least 150-200 words of substantial, informative text.
                - DO NOT write one-sentence explanations. 
                - Deep-dive into the "Why" and "How". Provide actionable advice and expert insights.
                - Paragraphs should be concise (2-4 sentences) but MUST be numerous to build total depth.
                - Use a humanized, authoritative first-person perspective (as an expert from {business_name}).
                
                STRICT FORMATTING:
                - No labels like "H1:", "H2:". Use raw <h1>, <h2> tags.
                - {table_instr}
                - {info_instr}
                - Start with <div class='key-takeaways'><strong>Key Highlights:</strong> [List]</div>.
                - CTA at end with {business_url}.
                
                META:
                - 'meta_title': 50-60 chars, front-load "{primary_k}".
                - 'meta_description': 150 chars max.
                Return ONLY JSON: {{'meta_title': '', 'meta_description': '', 'article_html': ''}}
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "SEO Master Writer. Expert in clean HTML and CSS-based visual layouts."}, {"role": "user", "content": user_p}],
                    response_format={"type": "json_object"}
                )
                gen_data = json.loads(response.choices[0].message.content)
                
                img_urls = []
                for i in range(num_images):
                    v_prompt = f"PHOTOREALISTIC high-end photography of {final_h1} in {industry} context. Natural light, real environment, 8k DSLR, no text."
                    img_res = client.images.generate(model="dall-e-3", prompt=v_prompt, size="1792x1024", quality="hd")
                    img_urls.append(img_res.data[0].url)
                
                gen_data["image_urls"] = img_urls
                st.session_state.generated_data = gen_data
                st.success("Elite Article Generated!")
        except Exception as e: st.error(f"Error: {e}")

if st.session_state.generated_data:
    data = st.session_state.generated_data
    st.divider()
    
    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.subheader("📋 SEO Meta Data")
    m1, m2 = st.columns(2)
    with m1:
        st.write("**Meta Title**")
        st.text_area("Title", value=data.get("meta_title", ""), height=100, label_visibility="collapsed", key="mt_disp")
        copy_to_clipboard(data.get("meta_title", ""), "📋 Copy Title", "mt", True)
    with m2:
        st.write("**Meta Description**")
        st.text_area("Desc", value=data.get("meta_description", ""), height=100, label_visibility="collapsed", key="md_disp")
        copy_to_clipboard(data.get("meta_description", ""), "📋 Copy Desc", "md", True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.subheader("📄 Interactive Content Preview")
    st.markdown(f"<div class='rendered-content'>{data.get('article_html', '')}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if "image_urls" in data:
        st.subheader(f"🖼️ Authentic Banners ({len(data['image_urls'])} total)")
        for idx, url in enumerate(data["image_urls"]):
            st.markdown(f'<div class="banner-container"><img src="{url}"></div>', unsafe_allow_html=True)
            img_bytes = download_image_bytes(url)
            if img_bytes:
                st.download_button(label=f"📥 Download Banner {idx+1}", data=img_bytes, file_name=f"banner_{idx+1}.jpg", mime="image/jpeg", key=f"dl_i_{idx}")

    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.subheader("🛠️ Final Tools & Export")
    c1, c2 = st.columns(2)
    with c1: copy_to_clipboard(data.get("article_html", ""), "💾 Copy HTML Code", "html", True)
    with c2: copy_to_clipboard(data.get("article_html", ""), "👤 Copy Formatted Text", "rich", False)
    st.download_button(label="📥 Download Article (HTML File)", data=data.get("article_html", ""), file_name="seo_article.html", mime="text/html", use_container_width=True)
    
    actual_words = len(strip_html(data.get("article_html", "")).split())
    st.markdown(f"<div style='background: #1e293b; color: white; padding: 16px; border-radius: 10px; border-left: 5px solid #3b82f6;'><strong>Audit:</strong> {actual_words} words | <strong>Grade:</strong> Elite SEO Content</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 11px; margin-top: 60px;'>Elite SEO & GEO Engine | Powered by OpenAI | © 2026</p>", unsafe_allow_html=True)
