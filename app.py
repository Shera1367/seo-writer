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

if "research_data" not in st.session_state:
    st.session_state.research_data = None
if "generated_data" not in st.session_state:
    st.session_state.generated_data = None

# API Key check
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("Error: OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.2em;
        background-color: #28a745; color: white; font-weight: bold;
        border: none; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { background-color: #218838; }
    .research-box { background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196f3; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Elite SEO & GEO Strategy Engine")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Strategy Settings")
    industry = st.selectbox("Industry", ["Legal", "Medical", "Travel", "Real Estate", "Technology", "Finance", "E-commerce"])
    target_audience = st.text_input("Target Audience", placeholder="e.g. Accident victims in CA")
    language = st.selectbox("Language", ["English", "Persian", "Spanish", "French", "German"])
    
    st.divider()
    if st.button("🗑️ Clear All Data", type="secondary"):
        st.session_state.research_data = None
        st.session_state.generated_data = None
        st.rerun()

tab_research, tab_generator = st.tabs(["🔍 Phase 1: Research & Structure", "✨ Phase 2: Elite Content Engine"])

# --- PHASE 1: RESEARCH ---
with tab_research:
    st.header("Keyword & Structure Discovery")
    seed_topic = st.text_input("Enter Seed Topic / Main Idea", placeholder="e.g. Dental Implants benefits")
    
    if st.button("🔍 START RESEARCH"):
        if not seed_topic:
            st.warning("Please enter a topic.")
        else:
            try:
                client = OpenAI(api_key=API_KEY)
                res_prompt = f"""
                You are a Senior SEO Researcher. Analyze the topic: "{seed_topic}" for the {industry} industry.
                Target Audience: {target_audience}.
                
                Generate:
                1. 3 High-CTR Magnetic Headlines.
                2. 1 Primary Keyword.
                3. 5-7 Secondary Keywords.
                4. 10 LSI Keywords.
                5. A mandatory heading structure (H2, H3, H4) for a deep-dive article.
                
                Return ONLY a JSON object:
                {{"headlines": [], "primary": "", "secondary": "", "lsi": "", "structure": ""}}
                """
                with st.spinner("⏳ Analyzing market and keywords..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": res_prompt}],
                        response_format={"type": "json_object"}
                    )
                    st.session_state.research_data = json.loads(response.choices[0].message.content)
                    st.success("Research Complete! You can now use this data in Phase 2.")
            except Exception as e:
                st.error(f"Research Error: {e}")

    if st.session_state.research_data:
        res = st.session_state.research_data
        st.markdown("<div class='research-box'>", unsafe_allow_html=True)
        st.subheader("🎯 Research Results")
        st.write("**Suggested Headlines (High CTR):**")
        for h in res['headlines']: st.write(f"- {h}")
        
        c1, c2, c3 = st.columns(3)
        with c1: 
            st.write("**Primary**")
            st.code(res['primary'])
        with c2: 
            st.write("**Secondary**")
            st.code(res['secondary'])
        with c3: 
            st.write("**LSI**")
            st.code(res['lsi'])
            
        st.write("**Recommended Heading Structure:**")
        st.code(res['structure'])
        st.markdown("</div>", unsafe_allow_html=True)

# --- PHASE 2: GENERATOR ---
with tab_generator:
    st.header("Elite Content Generator")
    
    # Auto-fill from research if available
    res = st.session_state.research_data or {}
    
    col1, col2 = st.columns(2)
    with col1:
        business_name = st.text_input("Business Name", placeholder="e.g. Golden State Dental")
        article_title = st.text_input("Article Title (H1)", value=res.get("headlines", [""])[0] if res else "")
        primary_k = st.text_input("Primary Keyword", value=res.get("primary", "") if res else "")
        secondary_k = st.text_area("Secondary Keywords", value=res.get("secondary", "") if res else "")
    with col2:
        lsi_k = st.text_area("LSI Keywords", value=res.get("lsi", "") if res else "")
        headings_k = st.text_area("Structure (H2-H4)", value=res.get("structure", "") if res else "", height=150)
        extra_k = st.text_area("Extra/GEO Info", placeholder="Nearby highways, local laws...")

    gen_col1, gen_col2 = st.columns(2)
    with gen_col1:
        search_intent = st.selectbox("Intent", ["Informational", "Transactional", "Commercial"])
        tone = st.selectbox("Tone", ["Professional", "Authoritative", "Conversational"])
    with gen_col2:
        word_count = st.select_slider("Word Count", [500, 1000, 1500, 2000, 2500], value=1000)

    if st.button("✨ GENERATE ELITE HUMANIZED CONTENT"):
        if not article_title or not primary_k:
            st.warning("Headline and Primary Keyword are required.")
        else:
            try:
                client = OpenAI(api_key=API_KEY)
                sys_prompt = f"Elite Investigative Journalist and Practitioner in {industry}. Despises robotic AI writing. Language: {language}."
                user_prompt = f"""
                Write an ULTIMATE, human-grade deep-dive article for {business_name}.
                Structure: H1 -> H2 -> H3 -> H4 hierarchy.
                
                HUMANIZATION RULES:
                1. No AI clichés (delve, unleash, moreover).
                2. Vary sentence length (Burstiness).
                3. Use first-person expert perspective.
                4. Include 1 famous authority quote in <blockquote>.
                5. Use <strong> for emphasis and <u> for specific terms.
                6. 2 External links to .gov or .edu.
                7. 3 Real-talk FAQs.
                
                DATA:
                Title: {article_title}
                Primary: {primary_k} | Secondary: {secondary_k} | LSI: {lsi_k}
                Intent: {search_intent} | Tone: {tone} | Words: {word_count}
                GEO/Extra: {extra_k}
                
                Return JSON: {{"meta_title": "", "meta_description": "", "article_html": ""}}
                """
                with st.spinner("⏳ Synthesizing elite content..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}],
                        response_format={"type": "json_object"},
                        temperature=0.85
                    )
                    st.session_state.generated_data = json.loads(response.choices[0].message.content)
                    st.success("Article Generated!")
            except Exception as e:
                st.error(f"Generation Error: {e}")

    if st.session_state.generated_data:
        data = st.session_state.generated_data
        st.divider()
        st.subheader("📋 Final Deliverables")
        
        m1, m2 = st.columns(2)
        with m1:
            st.write("**Meta Title**")
            copy_to_clipboard(data.get("meta_title", ""), key_suffix="mt", is_html=True)
            st.text_input("Edit Meta Title", value=data.get("meta_title", ""), label_visibility="collapsed")
        with m2:
            st.write("**Meta Description**")
            copy_to_clipboard(data.get("meta_description", ""), key_suffix="md", is_html=True)
            st.text_area("Edit Meta Description", value=data.get("meta_description", ""), label_visibility="collapsed")

        st.write("**Content Body**")
        c1, c2, _ = st.columns([1, 1, 3])
        with c1: copy_to_clipboard(data.get("article_html", ""), "💾 Copy HTML", key_suffix="html", is_html=True)
        with c2: copy_to_clipboard(data.get("article_html", ""), "👤 Copy Rich Text", key_suffix="rich", is_html=False)
        
        t_prev, t_code = st.tabs(["👁️ Preview", "💻 HTML Code"])
        with t_prev: st.markdown(data.get("article_html", ""), unsafe_allow_html=True)
        with t_code: st.text_area("Source", value=data.get("article_html", ""), height=400)
        
        actual_words = len(strip_html(data.get("article_html", "")).split())
        st.markdown(f"**Audit:** Word Count: `{actual_words}` | Brand: `{business_name}` | SEO: `Human-Grade`")

st.markdown("<p style='text-align: center; color: grey; font-size: 11px; margin-top: 50px;'>Sheragim.biz Elite Engine | © 2026</p>", unsafe_allow_html=True)
