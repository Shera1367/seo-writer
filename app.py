import streamlit as st
from openai import OpenAI
import time
import json

# Advanced Page Configuration
st.set_page_config(
    page_title="Elite AI SEO & GEO Writer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Professional Look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        border: none;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Check for API Key in Secrets
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("Error: OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

# Header and Introduction
st.title("🚀 SEO & GEO Content Engine")
st.markdown("---")

# Sidebar for Content Strategy
with st.sidebar:
    st.header("⚙️ Content Strategy")
    
    language = st.selectbox(
        "Content Language",
        ["English", "Persian", "Spanish", "French", "German"],
        index=0
    )

    industry = st.selectbox(
        "Industry / Niche",
        ["Legal", "Medical", "Travel", "Real Estate", "Technology", "Finance", "General/Lifestyle"],
        index=0
    )

    search_intent = st.selectbox(
        "Search Intent",
        ["Informational", "Transactional", "Navigational", "Commercial Investigation"],
        index=0
    )

    tone = st.selectbox(
        "Tone of Voice",
        ["Professional", "Informative", "Casual", "Technical", "Authoritative", "Conversational"],
        index=0
    )
    
    word_count = st.select_slider(
        "Target Word Count",
        options=[300, 500, 800, 1000, 1500, 2000, 2500],
        value=1000
    )
    
    st.info("💡 SEO FAQ, GEO Optimization, and Meta Tags are enabled by default for maximum performance.")

# Main Input Section
col1, col2 = st.columns([1, 1])

with col1:
    article_title = st.text_input("Article Title", placeholder="e.g. Best Personal Injury Attorney in California")
    target_audience = st.text_input("Target Audience", placeholder="e.g. Accident victims, Small business owners...")
    primary_keyword = st.text_input("Primary Keyword", placeholder="Main focus keyword...")
    secondary_keywords = st.text_area("Secondary Keywords", placeholder="Separate with commas or Enter...")

with col2:
    lsi_keywords = st.text_area("LSI Keywords", placeholder="Separate with commas or Enter...")
    suggested_headings = st.text_area("Suggested Headings", placeholder="Introduction\nKey Services\nWhy Choose Us\nConclusion")
    extra_instructions = st.text_area("Extra Instructions & GEO Data", placeholder="e.g. Include local Woodland Hills data, mention specific California laws...")

# Generation Button
if st.button("✨ GENERATE ELITE CONTENT"):
    if not article_title or not primary_keyword:
        st.warning("Please enter the Article Title and Primary Keyword.")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            
            system_prompt = f"""
            You are an elite SEO content strategist, content writer, and conversion copywriter.
            You specialize in creating in-depth, highly educational, and structured SEO articles for the {industry} industry.
            Language: {language}.
            """
            
            user_prompt = f"""
            Task: Write a 100% unique, authoritative, and E-E-A-T compliant article specifically for the {industry} industry.
            
            CORE REQUIREMENTS:
            1. Satisfy {search_intent} intent perfectly.
            2. Use a clear H1, H2, and H3 hierarchy.
            3. Include practical insights and actionable advice for {target_audience}.
            4. Build trust and authority.
            5. Mandatory GEO Optimization: Include authoritative citations, data-driven points, and expert-like quotes.
            6. Mandatory SEO Elements: Include exactly 3 highly optimized FAQs at the end.
            7. AVOID em dashes (—) and use short paragraphs.
            8. Humanize the content to sound like a professional expert, not AI.

            STRUCTURE:
            - H1: {article_title}
            - Introduction (150-200 words): Emotional/logical hook.
            - Body Content: Deep dive into "Why" and "How".
            - FAQ & CTA.

            OUTPUT FORMAT:
            You MUST return a JSON object with exactly these keys:
            "meta_title": "A compelling SEO title (under 60 chars)",
            "meta_description": "A high-CTR meta description (under 155 chars)",
            "article_html": "The full article content in HTML (h1, h2, h3, p, ul, li, strong)"

            DATA:
            - Primary Keyword: {primary_keyword}
            - Secondary Keywords: {secondary_keywords}
            - LSI Keywords: {lsi_keywords}
            - Extra Data: {extra_instructions}
            """

            with st.spinner("⏳ Strategizing and generating structured content..."):
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={ "type": "json_object" },
                    temperature=0.7
                )
                
                # Parse JSON result
                result_json = json.loads(response.choices[0].message.content)
                
                st.success("Generation Complete!")

                # --- Display Result Fields ---
                st.subheader("📋 Meta Information")
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.text_input("Meta Title", value=result_json.get("meta_title", ""), key="mt_field")
                with m_col2:
                    st.text_area("Meta Description", value=result_json.get("meta_description", ""), height=68, key="md_field")

                st.subheader("📝 Article Content")
                # Using text_area for easy editing and copying of the HTML
                final_content = st.text_area("HTML Output (Editable)", value=result_json.get("article_html", ""), height=450)
                
                # Preview Tab
                with st.expander("👁️ Preview Rendered Content"):
                    st.markdown(final_content, unsafe_allow_html=True)
                
                # Download Button
                st.download_button(
                    label="📥 Download HTML File",
                    data=final_content,
                    file_name=f"{article_title.lower().replace(' ', '_')}.html",
                    mime="text/html"
                )

        except Exception as e:
            st.error(f"System Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: grey;'>Elite SEO & GEO Engine | Built for Sheragim | © {time.localtime().tm_year}</p>", unsafe_allow_html=True)
