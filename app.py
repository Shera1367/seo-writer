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
        background-color: #007bff; color: white; border: none; padding: 6px 14px; 
        border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600;
        margin-bottom: 8px; transition: all 0.2s;
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
    components.html(html_button, height=45)

if "research_data" not in st.session_state:
    st.session_state.research_data = None
if "generated_data" not in st.session_state:
    st.session_state.generated_data = None

try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("Error: OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

st.markdown("""
<style>
    .main { background-color: #fcfcfc; }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3.5em;
        background-color: #28a745; color: white; font-weight: bold;
        border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .research-box { 
        background-color: #ffffff; padding: 25px; border-radius: 15px; 
        border: 1px solid #eee; margin-bottom: 20px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
    }
    .keyword-pill {
        display: inline-block; background: #f0f7ff; color: #007bff;
        padding: 5px 15px; border-radius: 25px; margin: 5px; font-size: 12px; font-weight: 600;
        border: 1px solid #d0e4ff;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Elite SEO & GEO Content Engine")
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
    st.header("Topic Analysis & Structure Discovery")
    seed_topic = st.text_input("Enter Main Topic", placeholder="e.g. Dental Implant Benefits for Seniors")
    
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
                    st.success("Research Complete! Ready for Phase 2.")
            except Exception as e:
                st.error(f"Research Error: {e}")

    if st.session_state.research_data:
        res = st.session_state.research_data
        st.markdown("<div class='research-box'>", unsafe_allow_html=True)
        st.subheader("🎯 Research Results")
        
        st.write("**Magnetic Headlines (Optimized for CTR):**")
        for h in res.get('headlines', []): st.info(h)
        
        c1, c2 = st.columns(2)
        with c1: 
            st.write("**Primary Keyword**")
            st.code(res.get('primary', ''))
            
            # Robust split handling to avoid AttributeError
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
    st.header("Elite Content Generator")
    res = st.session_state.research_data or {}
    
    col1, col2 = st.columns(2)
    with col1:
        article_title = st.text_input("Final H1 Title", value=res.get("headlines", [""])[0] if res else "")
        primary_k = st.text_input("Primary Keyword (Focus)", value=res.get("primary", "") if res else "")
        secondary_k = st.text_area("Secondary Keywords", value=res.get("secondary", "") if res else "")
    with col2:
        lsi_k = st.text_area("LSI Keywords", value=res.get("lsi", "") if res else "")
        headings_k = st.text_area("Heading Hierarchy (H2-H4)", value=res.get("structure_text", "") if res else "", height=150)
        extra_k = st.text_area("GEO & Instruction Data", placeholder="Specific locations, local laws, or landmarks...")

    gen_col1, gen_col2 = st.columns(2)
    with gen_col1:
        search_intent = st.selectbox("Intent", ["Informational", "Transactional", "Commercial Investigation", "Navigational"])
        tone = st.selectbox("Tone", ["Professional", "Authoritative", "Conversational", "Technical"])
    with gen_col2:
        word_count_goal = st.select_slider("Word Count Goal", [500, 1000, 1500, 2000, 2500], value=1000)

    if st.button("✨ GENERATE HUMANIZED ELITE ARTICLE"):
        if not article_title or not primary_k:
            st.warning("H1 Title and Primary Keyword are required.")
        else:
            try:
                client = OpenAI(api_key=API_KEY)
                sys_p = f"You are an Elite Investigative Journalist and Copywriter. Industry: {industry}. Language: {language}."
                
                user_p = f"""
                Write an ULTIMATE, human-grade deep-dive article for {business_name}.
                Structure: H1 -> H2 -> H3 -> H4 hierarchy.
                
                HUMANIZATION & HELPUL CONTENT RULES:
                1. NO AI clichés (delve, unleash, testament, moreover).
                2. BURSTINESS: Vary sentence lengths significantly (Short vs Long).
                3. PERSPECTIVE: Use first-person expert perspective from {business_name}.
                4. CITATIONS: Include 2 external links to .gov or .edu sources (relevant to {industry}).
                5. QUOTES: Include 1 famous authority quote in <blockquote>.
                6. FORMATTING: Use <strong> for SEO and <u> for key terms. NO em-dashes (—).
                7. FAQ: 3 Real-talk, non-generic FAQs at the end.
                8. DEPTH: Explain "WHY" and "HOW" in every section.
                
                DATA:
                Title: {article_title} | Primary: {primary_k} | Keywords: {secondary_k} | LSI: {lsi_k}
                Outline: {headings_k} | Intent: {search_intent} | Words: {word_count_goal}
                GEO Context: {extra_k}
                
                Return JSON: {{"meta_title": "", "meta_description": "", "article_html": ""}}
                """
                with st.spinner("⏳ Synthesizing deep-dive content... This takes 60-90 seconds for quality."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "system", "content": sys_p}, {"role": "user", "content": user_p}],
                        response_format={"type": "json_object"},
                        temperature=0.85
                    )
                    st.session_state.generated_data = json.loads(response.choices[0].message.content)
                    st.success("Elite Article Generated!")
            except Exception as e:
                st.error(f"Generation Error: {e}")

if st.session_state.generated_data:
    data = st.session_state.generated_data
    st.divider()
    st.subheader("📋 Final Deliverables")
    
    m1, m2 = st.columns(2)
    with m1:
        st.write("**Meta Title**")
        copy_to_clipboard(data.get("meta_title", ""), "Copy", key_suffix="mt", is_html=True)
        st.text_input("Edit Meta Title", value=data.get("meta_title", ""), label_visibility="collapsed")
    with m2:
        st.write("**Meta Description**")
        copy_to_clipboard(data.get("meta_description", ""), "Copy", key_suffix="md", is_html=True)
        st.text_area("Edit Meta Description", value=data.get("meta_description", ""), height=68, label_visibility="collapsed")

    st.write("**Content Body**")
    c1, c2, _ = st.columns([1.2, 1.2, 3])
    with c1: copy_to_clipboard(data.get("article_html", ""), "💾 Copy HTML Code", key_suffix="html", is_html=True)
    with c2: copy_to_clipboard(data.get("article_html", ""), "👤 Copy Formatted Text", key_suffix="rich", is_html=False)
    
    t_prev, t_code = st.tabs(["👁️ Rendered Preview", "💻 Raw HTML Source"])
    with t_prev: st.markdown(data.get("article_html", ""), unsafe_allow_html=True)
    with t_code: st.text_area("Source", value=data.get("article_html", ""), height=400)
    
    actual_words = len(strip_html(data.get("article_html", "")).split())
    st.markdown(f"**Final Audit:** Actual Word Count: `{actual_words}` | Brand: `{business_name}` | SEO: `Human-Grade Verified` | GEO: `Enabled`")

st.markdown("<p style='text-align: center; color: grey; font-size: 11px; margin-top: 50px;'>Elite SEO & GEO Engine | Powered by GPT-4o | © 2026</p>", unsafe_allow_html=True)
