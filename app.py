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

try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("❌ API Keys missing! Please add 'OPENAI_API_KEY' and 'GOOGLE_API_KEY' to Streamlit Secrets.")
    st.stop()

def strip_html(html_string):
    """Removes HTML tags for word count auditing."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_string)

def generate_google_image(prompt, is_infographic=False):
    """Google Imagen 4.0 generator for 16:9 banners and visual infographics."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={GOOGLE_API_KEY}"
    
    if is_infographic:
        # User requested "real" theme for infographics
        final_prompt = f"High-end professional realistic educational visual for '{prompt}'. Realistic 35mm photography of professional tools or environment mixed with clean minimal instructional layout, real-world textures, natural lighting, high contrast, 16:9 ratio, professional slide quality."
    else:
        final_prompt = f"{prompt}. Cinematic widescreen 16:9 composition, professional 35mm photography, single unified frame, natural lighting, high-end commercial quality, no text."
    
    payload = {
        "instances": [{"prompt": final_prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9"
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            if 'predictions' in result and len(result['predictions']) > 0:
                img_data = result['predictions'][0]['bytesBase64Encoded']
                return f"data:image/png;base64,{img_data}"
        else:
            st.error(f"Google Image API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
            
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
    .main { background-color: #0f172a; }
    .deliverable-card {
        background-color: #1e293b;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .banner-container {
        width: 100%;
        max-width: 1200px;
        aspect-ratio: 16 / 9;
        border-radius: 12px;
        margin: 25px 0;
        border: 1px solid #334155;
        overflow: hidden;
        background: #1e293b;
    }
    .banner-container img { width: 100%; height: 100%; object-fit: cover; display: block; }
    
    /* FIXING VISIBILITY FOR RENDERED CONTENT */
    .rendered-content h1 { color: #f8fafc !important; font-weight: 800; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; margin-bottom: 20px; }
    .rendered-content h2 { color: #f1f5f9 !important; margin-top: 40px; font-weight: 700; border-left: 5px solid #3b82f6; padding-left: 15px; margin-bottom: 15px; }
    .rendered-content h3 { color: #e2e8f0 !important; margin-top: 25px; font-weight: 600; margin-bottom: 10px; }
    .rendered-content p { line-height: 1.9; color: #cbd5e1 !important; margin-bottom: 20px; font-size: 1.1em; }
    .rendered-content ul, .rendered-content ol { color: #cbd5e1 !important; margin-bottom: 20px; padding-left: 20px; }
    .rendered-content li { margin-bottom: 8px; }
    
    .key-takeaways { background: #1e293b; border: 1px solid #3b82f6; border-left: 5px solid #3b82f6; padding: 25px; border-radius: 12px; margin: 25px 0; color: #f1f5f9 !important; }
    .key-takeaways strong { color: #60a5fa !important; }
    
    .data-table-container { overflow-x: auto; margin: 30px 0; border-radius: 12px; border: 1px solid #334155; }
    .data-table { width: 100%; border-collapse: collapse; background: #0f172a; }
    .data-table th { background-color: #3b82f6; color: white; padding: 15px; text-align: left; }
    .data-table td { padding: 15px; border-bottom: 1px solid #334155; color: #cbd5e1 !important; }
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
    language = st.selectbox("Language", ["English", "Persian", "Spanish", "French", "German"])
    industry = st.selectbox("Industry", ["Legal", "Medical", "Travel", "Real Estate", "Technology", "Finance", "E-commerce"])
    business_name = st.text_input("Business Name", placeholder="e.g. Acme Corp")
    business_url = st.text_input("Business Website URL", placeholder="e.g. https://yoursite.com")
    target_audience = st.text_input("Target Audience", placeholder="e.g. Local customers")
    st.divider()
    sidebar_word_count = st.select_slider("Target Words (Global)", options=word_options, value=1000)
    num_images = st.slider("Number of Images", 1, 3, 1)
    include_infographic = st.checkbox("Include Realistic Visual Infographic", value=True)
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
            
            with st.spinner(f"⏳ Synthesizing master-level SEO content..."):
                table_instr = "MANDATORY: Include a detailed data table using <table class='data-table'>." if include_table else ""
                
                user_p = f"""
                Write a comprehensive expert article for {business_name} in {language}. Words: {sidebar_word_count}. Intent: {search_intent}. 
                H1 Title: {final_h1}. Structure: {headings_k}. Website: {business_url}.
                
                CRITICAL INSTRUCTIONS:
                - EVERY H2 heading MUST have at least 200 words of substance.
                - Use 2 authority links (.gov or .edu).
                - Start with <div class='key-takeaways'><strong>Key Highlights:</strong> [List]</div>.
                - {table_instr}
                - ABSOLUTELY NO Markdown hashtags. Use ONLY raw <h1>, <h2>, <h3> tags.
                - Professional authoritative expert perspective.
                - END with a CTA mentioning {business_url}.
                
                Return JSON: {{'meta_title': '', 'meta_description': '', 'article_html': ''}}
                """
                
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "SEO Specialist."}, {"role": "user", "content": user_p}],
                    response_format={"type": "json_object"}
                )
                article_data = json.loads(response.choices[0].message.content)

            img_data_urls = []
            info_img_url = None
            
            if num_images > 0:
                img_status = st.status(f"📸 Generating {num_images} realistic banners...", expanded=True)
                for i in range(num_images):
                    img_status.write(f"Generating banner {i+1} of {num_images}...")
                    v_prompt = f"Professional authentic high-end photography for {final_h1} in {industry}. Real textures, natural lighting, sharp focus, 35mm DSLR."
                    data_url = generate_google_image(v_prompt)
                    if data_url:
                        img_data_urls.append(data_url)
                img_status.update(label="✅ Banners processed!", state="complete", expanded=False)

            if include_infographic:
                with st.spinner("🎨 Creating Realistic Visual Educational Visual..."):
                    info_url = generate_google_image(final_h1, is_infographic=True)
                    if info_url:
                        info_img_url = info_url
            
            embedded_html = ""
            
            if info_img_url:
                embedded_html += f'<hr><h2>Visual Educational Guide</h2><div class="banner-container"><img src="{info_img_url}"></div>'
            
            if img_data_urls:
                embedded_html += f'<hr><h2>Professional Imagery (1200x675)</h2>'
                for url in img_data_urls:
                    embedded_html += f'<div class="banner-container"><img src="{url}"></div>'
            
            article_data["article_html"] += embedded_html
            article_data["image_urls"] = img_data_urls
            if info_img_url:
                article_data["infographic_url"] = info_img_url
            
            st.session_state.generated_data = article_data
            st.success("Elite Article with Realistic Visuals Ready!")
            
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
    st.subheader("📄 High-Contrast Article Preview")
    st.markdown(f"<div class='rendered-content'>{data.get('article_html', '')}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.subheader("🛠️ Export & Download")
    c1, c2 = st.columns(2)
    with c1: copy_to_clipboard(data.get("article_html", ""), "💾 Copy HTML", "html", True)
    with c2: copy_to_clipboard(data.get("article_html", ""), "👤 Copy Formatted Text", "rich", False)
    
    st.download_button(
        label="📥 Download Article (Full HTML Package)", 
        data=data.get("article_html", ""), 
        file_name="elite_seo_article.html", 
        mime="text/html", 
        use_container_width=True
    )
    
    if "infographic_url" in data:
        st.write("**Download Realistic Infographic:**")
        try:
            info_bytes = base64.b64decode(data["infographic_url"].split(",")[1])
            st.download_button(label="📥 Download Visual (PNG)", data=info_bytes, file_name="visual_guide.png", mime="image/png", use_container_width=True)
        except Exception: pass

    if "image_urls" in data and len(data["image_urls"]) > 0:
        st.write("**Download Original High-Res Banners:**")
        cols = st.columns(len(data["image_urls"]))
        for idx, url in enumerate(data["image_urls"]):
            with cols[idx]:
                try:
                    img_bytes = base64.b64decode(url.split(",")[1])
                    st.download_button(label=f"Banner {idx+1}", data=img_bytes, file_name=f"banner_{idx+1}.png", mime="image/png", key=f"dl_single_{idx}")
                except Exception: pass
    
    actual_words = len(strip_html(data.get("article_html", "")).split())
    st.info(f"Audit: {actual_words} words | Assets: High-Resolution Real-World Visuals Included")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 11px; margin-top: 60px;'>Elite SEO & GEO Engine | Google Imagen 4.0 | © 2026</p>", unsafe_allow_html=True)
