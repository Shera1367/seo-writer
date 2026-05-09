import streamlit as st
from openai import OpenAI
import time
import json
import streamlit.components.v1 as components
import re
import requests
import base64
from io import BytesIO

st.set_page_config(
    page_title="Elite AI SEO & GEO Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration for APIs
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    # The environment provides Google API key automatically via an empty string constant
    GOOGLE_API_KEY = "" 
except Exception:
    st.error("❌ API Keys not properly configured in Streamlit Secrets.")
    st.stop()

def strip_html(html_string):
    """Removes HTML tags for word count auditing."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_string)

def generate_google_image(prompt):
    """Generates an image using Google's Imagen 4.0 model with exponential backoff."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={GOOGLE_API_KEY}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1}
    }
    
    retries = 5
    for i in range(retries):
        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                img_data = result['predictions'][0]['bytesBase64Encoded']
                return f"data:image/png;base64,{img_data}"
            elif response.status_code in [429, 500, 503]:
                time.sleep(2**i) 
            else:
                break
        except Exception:
            time.sleep(2**i)
            
    return None

def copy_to_clipboard(content, button_label="Copy", key_suffix="", is_html=False):
    """JavaScript for Rich Text and HTML copying."""
    safe_content = content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$').replace('"', '\\"')
    if is_html:
        js_code = f"var t=document.createElement('textarea');t.value=`{safe_content}`;document.body.appendChild(t);t.select();document.execCommand('copy');document.body.removeChild(t);"
    else:
        js_code = f"var c=document.createElement('div');c.innerHTML=`{safe_content}`;c.style.position='fixed';c.style.opacity=0;document.body.appendChild(c);window.getSelection().removeAllRanges();var r=document.createRange();r.selectNode(c);window.getSelection().addRange(r);document.execCommand('copy');window.getSelection().removeAllRanges();document.body.removeChild(c);"

    html_button = f"""
    <button id="copyBtn{key_suffix}" style="background-color:#007bff;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:13px;font-weight:600;width:100%;">
        {button_label}
    </button>
    <script>
    document.getElementById("copyBtn{key_suffix}").onclick = function() {{
        {js_code}
        this.innerHTML = "✓ Copied"; this.style.backgroundColor = "#28a745";
        setTimeout(() => {{ this.innerHTML = "{button_label}"; this.style.backgroundColor = "#007bff"; }}, 2000);
    }}
    </script>
    """
    components.html(html_button, height=45)

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
        max-width: 100%;
        height: auto;
        border-radius: 12px;
        margin: 20px 0;
        border: 1px solid #e5e7eb;
        overflow: hidden;
    }
    .banner-container img { width: 100%; height: auto; display: block; }
    
    .rendered-content h1 { color: #111827 !important; font-weight: 800; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }
    .rendered-content h2 { color: #1f2937 !important; margin-top: 30px; font-weight: 700; }
    .rendered-content p { line-height: 1.8; color: #374151 !important; margin-bottom: 20px; }
    
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
    }
    .data-table th { background-color: #3b82f6; color: white; padding: 15px; text-align: left; }
    .data-table td { padding: 12px 15px; border-bottom: 1px solid #e5e7eb; color: #1e293b !important; }

    .visual-infographic {
        background: #f8fafc;
        border: 2px dashed #3b82f6;
        padding: 25px;
        border-radius: 15px;
        margin: 30px 0;
    }
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

if "research_data" not in st.session_state:
    st.session_state.research_data = None
if "generated_data" not in st.session_state:
    st.session_state.generated_data = None

st.title("🚀 Elite SEO & GEO Content Engine")

word_options = list(range(200, 2100, 100))

with st.sidebar:
    st.header("⚙️ Global Strategy")
    language = st.selectbox("Language", ["Persian", "English", "Spanish", "French", "German"])
    industry = st.selectbox("Industry", ["Legal", "Medical", "Travel", "Real Estate", "Technology", "Finance", "E-commerce"])
    business_name = st.text_input("Business Name", placeholder="e.g. Deldar Legal")
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
            client = OpenAI(api_key=OPENAI_API_KEY)
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
            openai_client = OpenAI(api_key=OPENAI_API_KEY)
            with st.spinner(f"⏳ Synthesizing master-level content and banners..."):
                
                table_instr = "MANDATORY: Include a comparison table wrapping it in <div class='data-table-container'><table class='data-table'>...</table></div>." if include_table else ""
                info_instr = "MANDATORY: Include a 'Visual Infographic' section using ONLY CSS-styled boxes (no <img> tags) with class 'visual-infographic' and 'infographic-step'." if include_infographic else ""

                user_p = f"""
                Write a deep-dive SEO article for {business_name} in {language}. Words: {sidebar_word_count}. Intent: {search_intent}. 
                H1 Title: {final_h1}. Structure: {headings_k}. Website: {business_url}.
                
                CRITICAL INSTRUCTIONS:
                - EVERY heading MUST be followed by significant informative text (min 150 words per H2).
                - Use exactly 2 outbound links to .gov or .edu sources.
                - Start with <div class='key-takeaways'><strong>Key Highlights:</strong> [List]</div>.
                - {table_instr}
                - {info_instr}
                - Professional tone, actionable expert advice.
                - END with a strong CTA mentioning {business_url}.
                - NO placeholders like [Image Here].
                
                Return JSON: {{'meta_title': '', 'meta_description': '', 'article_html': ''}}
                """
                
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "Master SEO Journalist."}, {"role": "user", "content": user_p}],
                    response_format={"type": "json_object"}
                )
                article_data = json.loads(response.choices[0].message.content)
                
                # Image generation and direct embedding
                img_data_urls = []
                embedded_images_html = "<hr><h2>Visual Assets</h2>"
                for i in range(num_images):
                    v_prompt = f"Authentic professional photography for {final_h1}. 35mm DSLR, natural light, realistic textures, professional environment. No text."
                    data_url = generate_google_image(v_prompt)
                    if data_url:
                        img_data_urls.append(data_url)
                        embedded_images_html += f'<div class="banner-container"><img src="{data_url}"></div>'
                
                # Append images to the main HTML so they are part of the preview and export
                article_data["article_html"] += embedded_images_html
                article_data["image_urls"] = img_data_urls
                
                st.session_state.generated_data = article_data
                st.success("Article Generated with Embedded Google Imagen 4.0 Banners!")
        except Exception as e: st.error(f"Error: {e}")

if st.session_state.generated_data:
    data = st.session_state.generated_data
    st.divider()
    
    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.subheader("📋 Meta Data")
    m1, m2 = st.columns(2)
    with m1:
        st.text_area("Meta Title", value=data.get("meta_title", ""), height=80, key="mt_disp")
        copy_to_clipboard(data.get("meta_title", ""), "📋 Copy Title", "mt", True)
    with m2:
        st.text_area("Meta Description", value=data.get("meta_description", ""), height=80, key="md_disp")
        copy_to_clipboard(data.get("meta_description", ""), "📋 Copy Desc", "md", True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.subheader("📄 Article Content & Embedded Media")
    st.markdown(f"<div class='rendered-content'>{data.get('article_html', '')}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.subheader("🛠️ Export & Download")
    c1, c2 = st.columns(2)
    with c1: copy_to_clipboard(data.get("article_html", ""), "💾 Copy HTML (Images Included)", "html", True)
    with c2: copy_to_clipboard(data.get("article_html", ""), "👤 Copy Formatted Text", "rich", False)
    
    st.download_button(
        label="📥 Download Article (HTML with Images)", 
        data=data.get("article_html", ""), 
        file_name="complete_article.html", 
        mime="text/html", 
        use_container_width=True
    )
    
    # Separate download buttons for individual PNGs
    if "image_urls" in data:
        st.write("**Download Individual Banners:**")
        cols = st.columns(len(data["image_urls"]))
        for idx, url in enumerate(data["image_urls"]):
            with cols[idx]:
                st.download_button(
                    label=f"Banner {idx+1} (PNG)", 
                    data=base64.b64decode(url.split(",")[1]), 
                    file_name=f"banner_{idx+1}.png", 
                    mime="image/png", 
                    key=f"dl_single_{idx}"
                )
    
    actual_words = len(strip_html(data.get("article_html", "")).split())
    st.info(f"Audit: {actual_words} words | Grade: Elite SEO Content")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 11px; margin-top: 60px;'>Elite SEO & GEO Engine | Google Imagen 4.0 | © 2026</p>", unsafe_allow_html=True)
