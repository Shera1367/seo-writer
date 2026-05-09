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
        height: 350px;
        overflow: hidden;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #e5e7eb;
    }
    .banner-container img { width: 100%; height: 100%; object-fit: cover; }
    .infographic-box {
        background: #f0f7ff;
        border: 2px dashed #007bff;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .rendered-content h1 { color: #111827; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Elite SEO & GEO Content Engine")

word_options = list(range(200, 2100, 100))

with st.sidebar:
    st.header("⚙️ Global Strategy")
    language = st.selectbox("Language", ["English", "Persian", "Spanish", "French", "German"])
    industry = st.selectbox("Industry", ["Legal", "Medical", "Travel", "Real Estate", "Technology", "Finance", "E-commerce"])
    business_name = st.text_input("Business Name", placeholder="e.g. Deldar Legal")
    target_audience = st.text_input("Target Audience", placeholder="e.g. Accident victims in CA")
    st.divider()
    sidebar_word_count = st.select_slider("Default Target Words", options=word_options, value=1000)
    if st.button("🗑️ Reset Application", type="secondary"):
        st.session_state.research_data = None
        st.session_state.generated_data = None
        st.rerun()

st.subheader("Step 1: Strategic Research & Competitor Analysis")
col_s1, col_s2 = st.columns(2)
with col_s1:
    seed_topic = st.text_input("Enter Seed Topic", placeholder="e.g. Benefits of Dental Implants")
with col_s2:
    competitor_links = st.text_area("Competitor URLs (One per line)", placeholder="https://competitor1.com/blog\nhttps://competitor2.com/article")

if st.button("🔍 START RESEARCH & ANALYSIS"):
    if not seed_topic or not business_name:
        st.warning("Please enter Seed Topic and Business Name.")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            res_prompt = f"""
            Industry: {industry}. Brand: {business_name}. Topic: '{seed_topic}'. 
            Analyze these competitor links to find content gaps: {competitor_links}.
            Action: Generate 3 High-CTR Headlines, 1 Primary Keyword, 5 Secondary, 10 LSI, and a deep H2-H4 outline that outperforms them.
            RULES: Never mention competitor names. Return JSON: {{'headlines': [], 'primary': '', 'secondary': [], 'lsi': [], 'structure_text': ''}}
            """
            with st.spinner("⏳ Analyzing search landscape and competitors..."):
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

col_opt1, col_opt2 = st.columns(2)
with col_opt1:
    num_images = st.slider("Number of Images needed", 1, 3, 2)
    include_infographic = st.checkbox("Include Educational Step-by-Step Infographic", value=True)
with col_opt2:
    search_intent = st.selectbox("Search Intent", ["Informational", "Transactional", "Commercial"])
    word_count_goal = st.select_slider("Target Words", options=word_options, value=sidebar_word_count)

if st.button("✨ GENERATE HUMANIZED ELITE ARTICLE"):
    if not final_h1 or not primary_k:
        st.warning("H1 and Primary Keyword are required.")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            with st.spinner(f"⏳ Synthesizing content and {num_images} realistic banners..."):
                infographic_instr = "Include a 'Step-by-Step Educational Infographic' section styled as an HTML block with a distinct background-color." if include_infographic else ""
                
                user_p = f"Write unique human-grade article for {business_name} in {language}. Title: {final_h1}. Words: {word_count_goal}. Intent: {search_intent}. Structure: {headings_k}. {infographic_instr} No em-dashes. 2 .gov links. 3 FAQs. Use <strong> and <u>. Return JSON: {{'meta_title': '', 'meta_description': '', 'article_html': ''}}"
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "Professional SEO journalist."}, {"role": "user", "content": user_p}],
                    response_format={"type": "json_object"}
                )
                gen_data = json.loads(response.choices[0].message.content)
                
                img_urls = []
                for i in range(num_images):
                    v_prompt = f"Authentic professional high-end photography of {final_h1} in {industry}, variant {i+1}. Natural light, real textures, no AI look, high quality."
                    img_res = client.images.generate(model="dall-e-3", prompt=v_prompt, size="1792x1024", quality="hd")
                    img_urls.append(img_res.data[0].url)
                
                gen_data["image_urls"] = img_urls
                st.session_state.generated_data = gen_data
                st.success("Article Generated!")
        except Exception as e: st.error(f"Error: {e}")

if st.session_state.generated_data:
    data = st.session_state.generated_data
    st.divider()
    
    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.subheader("📋 Meta Information")
    m1, m2 = st.columns(2)
    fh = 100
    with m1:
        st.write("**Meta Title**")
        st.text_area("Title", value=data.get("meta_title", ""), height=fh, label_visibility="collapsed", key="mt_disp")
        copy_to_clipboard(data.get("meta_title", ""), "📋 Copy Title", "mt", True)
    with m2:
        st.write("**Meta Description**")
        st.text_area("Desc", value=data.get("meta_description", ""), height=fh, label_visibility="collapsed", key="md_disp")
        copy_to_clipboard(data.get("meta_description", ""), "📋 Copy Desc", "md", True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.subheader("📄 Content Preview")
    st.markdown(f"<div class='rendered-content'>{data.get('article_html', '')}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if "image_urls" in data:
        st.subheader(f"🖼️ Realistic Banners ({num_images} total)")
        for idx, url in enumerate(data["image_urls"]):
            st.markdown(f'<div class="banner-container"><img src="{url}"></div>', unsafe_allow_html=True)
            img_bytes = download_image_bytes(url)
            if img_bytes:
                st.download_button(label=f"📥 Download Banner {idx+1}", data=img_bytes, file_name=f"banner_{idx+1}.jpg", mime="image/jpeg", key=f"dl_i_{idx}")

    st.markdown("<div class='deliverable-card'>", unsafe_allow_html=True)
    st.subheader("🛠️ Final Export")
    c1, c2 = st.columns(2)
    with c1: copy_to_clipboard(data.get("article_html", ""), "💾 Copy HTML Code", "html", True)
    with c2: copy_to_clipboard(data.get("article_html", ""), "👤 Copy Formatted Text", "rich", False)
    st.download_button(label="📥 Download Article (HTML File)", data=data.get("article_html", ""), file_name="article.html", mime="text/html", use_container_width=True)
    actual_words = len(strip_html(data.get("article_html", "")).split())
    st.markdown(f"<div style='background: #1e293b; color: white; padding: 16px; border-radius: 10px; border-left: 5px solid #3b82f6;'><strong>Audit:</strong> {actual_words} words | <strong>Brand:</strong> {business_name}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 11px; margin-top: 60px;'>Elite SEO & GEO Engine | © 2026</p>", unsafe_allow_html=True)
