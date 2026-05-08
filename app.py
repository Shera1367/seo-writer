import streamlit as st
from openai import OpenAI
import time

# Advanced Page Configuration
st.set_page_config(
    page_title="Professional AI SEO & GEO Writer",
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
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
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
    
    st.markdown("---")
    st.markdown("### SEO & GEO Checklist")
    use_faq = st.checkbox("Include FAQ (SEO)", value=True)
    use_citations = st.checkbox("GEO Optimization (Citations & Stats)", value=True)
    generate_meta = st.checkbox("Generate Meta Tags", value=True)

# Main Input Section
col1, col2 = st.columns([1, 1])

with col1:
    article_title = st.text_input("Article Title", placeholder="e.g. Best Personal Injury Attorney in California")
    primary_keyword = st.text_input("Primary Keyword", placeholder="Main focus keyword...")
    secondary_keywords = st.text_area("Secondary Keywords", placeholder="Separate with commas or Enter...")

with col2:
    lsi_keywords = st.text_area("LSI Keywords", placeholder="Separate with commas or Enter...")
    suggested_headings = st.text_area("Suggested Headings", placeholder="Introduction\nKey Services\nWhy Choose Us\nConclusion")
    extra_instructions = st.text_area("Extra Instructions & GEO Data", placeholder="e.g. Include local Woodland Hills data, mention specific California laws...")

# Generation Button
if st.button("✨ GENERATE OPTIMIZED CONTENT"):
    if not article_title or not primary_keyword:
        st.warning("Please enter the Article Title and at least the Primary Keyword.")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            
            # Elite Prompt Engineering for SEO & GEO
            system_prompt = f"""
            You are an elite SEO content strategist, content writer, and conversion copywriter.
            You specialize in SEO (Search Engine Optimization) and GEO (Generative Engine Optimization).
            Your goal is to write content that ranks in Google AND gets cited by AI engines like Perplexity, Gemini, and ChatGPT.
            Industry Expertise: {industry}.
            Language: {language}.
            """
            
            user_prompt = f"""
            Task: Write a 100% unique, high-utility, and E-E-A-T compliant article specifically for the {industry} industry.
            
            CORE DETAILS:
            - Language: {language}
            - Main Title (H1): {article_title}
            - Primary Keyword: {primary_keyword}
            - Secondary Keywords: {secondary_keywords}
            - LSI Keywords: {lsi_keywords}
            - Search Intent: {search_intent}
            - Tone: {tone}
            - Target Length: {word_count} words
            
            STRATEGIC SEO & GEO GUIDELINES:
            1. KEYWORD INTEGRATION: Naturally use the Primary Keyword in the first paragraph and subheadings. Distribute Secondary and LSI keywords throughout the text.
            2. GEO OPTIMIZATION: Include authoritative citations, data-driven points, and expert-like quotes to make the content "citable" by AI engines.
            3. INDUSTRY CONTEXT: Apply specific knowledge and compliance standards for the {industry} niche.
            4. INTENT ALIGNMENT: Structure the content specifically to satisfy {search_intent} queries.
            5. FAQ: {'Include a structured FAQ section' if use_faq else ''}.
            6. UNIQUE VALUE: Avoid generic fluff. Provide specific insights and technical details.
            
            TECHNICAL REQUIREMENTS & HIERARCHY:
            - The Main Title MUST be wrapped in an <h1> tag.
            - All subsequent subheadings MUST follow a logical hierarchy using <h2> and <h3> tags.
            - Output ONLY raw HTML (h1, h2, h3, p, ul, li, strong).
            - No markdown code blocks.
            - If 'Generate Meta Data' is checked, include <meta-title> and <meta-description> at the very beginning.
            
            EXTRA INSTRUCTIONS: {extra_instructions}
            """

            with st.spinner(f"⏳ Generating {language} content for {industry} industry..."):
                start_time = time.time()
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7
                )
                
                content = response.choices[0].message.content
                end_time = time.time()
                duration = round(end_time - start_time, 1)

            st.success(f"Content generated successfully in {duration} seconds!")

            # Results Display
            tab1, tab2, tab3 = st.tabs(["👁️ Preview Content", "💻 HTML Code", "📊 Analysis"])

            with tab1:
                st.markdown("### Article Preview")
                st.divider()
                st.markdown(content, unsafe_allow_html=True)

            with tab2:
                st.markdown("### HTML Source Code")
                st.code(content, language="html")
                st.download_button(
                    label="📥 Download HTML file",
                    data=content,
                    file_name=f"{article_title.lower().replace(' ', '_')}.html",
                    mime="text/html"
                )

            with tab3:
                word_actual = len(content.split())
                st.write(f"**Actual Word Count:** {word_actual}")
                st.write(f"**Industry Context:** {industry}")
                st.write(f"**Intent Fulfillment:** {search_intent}")
                st.progress(min(word_actual/word_count, 1.0))
                st.info("GEO Tip: Using precise statistics, entities, and specific names (like California street names or specific law codes) increases your chances of being cited by AI search engines.")

        except Exception as e:
            st.error(f"System Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: grey;'>Advanced SEO & GEO Engine | Built for Sheragim | © {time.localtime().tm_year}</p>", unsafe_allow_html=True)
