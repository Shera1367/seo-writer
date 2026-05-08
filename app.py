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
    use_faq = st.checkbox("Include 3 Optimized FAQs", value=True)
    use_citations = st.checkbox("GEO Optimization (Citations & Stats)", value=True)
    generate_meta = st.checkbox("Generate Meta Tags", value=True)

# Main Input Section
col1, col2 = st.columns([1, 1])

with col1:
    article_title = st.text_input("Article Title", placeholder="e.g. Best Personal Injury Attorney in California")
    target_audience = st.text_input("Target Audience", placeholder="e.g. Accident victims, Small business owners, Seniors...")
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
            You specialize in creating in-depth, highly educational, and structured SEO articles for the {industry} industry.
            Your goal is to fully satisfy search intent and go deeper than competitors by explaining the "why" and "how" of topics, not just providing definitions.
            You must write in {language}.
            """
            
            user_prompt = f"""
            Task: Write a 100% unique, authoritative, and E-E-A-T compliant article.
            
            OBJECTIVE:
            1. Satisfy {search_intent} intent perfectly.
            2. Use a clear H1, H2, and H3 hierarchy.
            3. Include practical insights, examples, and actionable advice for {target_audience}.
            4. Build trust and authority throughout the content.
            5. AVOID em dashes (—) entirely.
            6. AVOID fluff, filler, and vague generalizations.
            7. Use short paragraphs for maximum readability.
            
            STRUCTURE REQUIREMENTS:
            - H1: {article_title} (Must include the primary keyword naturally and be compelling).
            - Introduction (150 to 200 words): Hook the reader emotionally or logically and clearly define the problem.
            - Body Content: Dive deep into details. Explain the mechanics behind the topic.
            - FAQ: {'Include 3 highly optimized FAQs at the end' if use_faq else ''}.
            - Conclusion & CTA: End with a strong, persuasive Call-to-Action tailored to {target_audience}.
            
            CORE DATA:
            - Primary Keyword: {primary_keyword}
            - Secondary Keywords: {secondary_keywords}
            - LSI Keywords: {lsi_keywords}
            - Search Intent: {search_intent}
            - Tone: {tone}
            - Word Count: {word_count}
            
            TECHNICAL REQUIREMENTS:
            - Output ONLY raw HTML (h1, h2, h3, p, ul, li, strong).
            - No markdown code blocks.
            - If 'Generate Meta Data' is checked, include <meta-title> and <meta-description> at the beginning.
            
            FINAL QUALITY CHECK & HUMANIZATION:
            After writing the full article, perform a self-review of the content based on Quality, User Experience (UX), SEO, and GEO standards. 
            Humanize the tone and style to ensure it sounds like a real expert author with professional experience in the {industry} field. 
            Eliminate AI-typical patterns, predictable sentence structures, or generic filler. 
            The final result must feel authentic, engaging, and indistinguishable from professional human-written content.

            GEO & EXTRA: {extra_instructions}
            """

            with st.spinner(f"⏳ Strategizing and writing your elite {industry} content..."):
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

            st.success(f"Professional Content generated in {duration} seconds!")

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
                st.write(f"**Industry:** {industry}")
                st.write(f"**Target Audience:** {target_audience}")
                st.write(f"**Search Intent:** {search_intent}")
                st.progress(min(word_actual/word_count, 1.0))
                st.info("Elite Content Tip: By avoiding generalizations and explaining the 'why', you are signaling much higher E-E-A-T to search engines.")

        except Exception as e:
            st.error(f"System Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: grey;'>Elite SEO & GEO Engine | Built for Sheragim | © {time.localtime().tm_year}</p>", unsafe_allow_html=True)
