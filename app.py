import streamlit as st
from openai import OpenAI
import time

# تنظیمات پیشرفته صفحه
st.set_page_config(
    page_title="Professional AI SEO & GEO Writer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# استایل‌دهی سفارشی برای ظاهر حرفه‌ای
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

# بررسی وجود کلید API در Secrets
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("خطا: کلید API در بخش Secrets تنظیم نشده است.")
    st.stop()

# تیتر و معرفی ابزار
st.title("🚀 SEO & GEO Content Engine")
st.markdown("---")

# ستون‌بندی تنظیمات در سایدبار
with st.sidebar:
    st.header("⚙️ استراتژی محتوا")
    
    language = st.selectbox(
        "زبان محتوا (Language)",
        ["English", "Persian", "Spanish", "French", "German"],
        index=0
    )

    search_intent = st.selectbox(
        "هدف جستجو (Search Intent)",
        ["Informational (آموزشی)", "Transactional (خرید/خدمات)", "Navigational (برند)", "Commercial Investigation (مقایسه‌ای)"],
        index=0
    )

    tone = st.selectbox(
        "لحن مقاله (Tone)",
        ["Professional", "Informative", "Casual", "Technical", "Authoritative", "Conversational"],
        index=0
    )
    
    word_count = st.select_slider(
        "تعداد کلمات حدودی (Word Count)",
        options=[300, 500, 800, 1000, 1500, 2000, 2500],
        value=1000
    )
    
    st.markdown("---")
    st.markdown("### SEO & GEO Checklist")
    use_faq = st.checkbox("Include FAQ (SEO)", value=True)
    use_citations = st.checkbox("GEO Optimization (Citations & Stats)", value=True)
    generate_meta = st.checkbox("Generate Meta Tags", value=True)

# بخش ورودی‌های اصلی
col1, col2 = st.columns([1, 1])

with col1:
    article_title = st.text_input("عنوان مقاله (Article Title)", placeholder="e.g. Best Personal Injury Attorney in California")
    keywords = st.text_area("کلمات کلیدی (Target Keywords)", placeholder="primary keyword, secondary keyword, LSI keywords...", help="با کاما جدا کنید.")

with col2:
    suggested_headings = st.text_area("ساختار پیشنهادی (Suggested Headings)", placeholder="Introduction\nKey Services\nWhy Choose Us\nConclusion")
    extra_instructions = st.text_area("پیشنهادات اضافی و GEO (Extra Instructions)", placeholder="e.g. Include local Woodland Hills data, mention specific California laws...")

# دکمه تولید محتوا
if st.button("✨ GENERATE OPTIMIZED CONTENT"):
    if not article_title or not keywords:
        st.warning("لطفاً عنوان و کلمات کلیدی را وارد کنید.")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            
            # مهندسی پرامپت حرفه‌ای برای سئو و GEO
            system_prompt = f"""
            You are a world-class Digital Strategist specializing in SEO (Search Engine Optimization) and GEO (Generative Engine Optimization).
            Your goal is to write content that ranks in Google AND gets cited by AI engines like Perplexity, Gemini, and ChatGPT.
            Language: {language}.
            """
            
            user_prompt = f"""
            Task: Write a 100% unique, high-utility, and E-E-A-T compliant article.
            
            CORE DETAILS:
            - Language: {language}
            - Title: {article_title}
            - Primary Keywords: {keywords}
            - Search Intent: {search_intent}
            - Tone: {tone}
            - Target Length: {word_count} words
            
            STRATEGIC GUIDELINES:
            1. GEO OPTIMIZATION: Include authoritative citations, data-driven points, and expert-like quotes to make the content "citable" by AI engines.
            2. LOCAL RELEVANCE: Integrate geographic context (GEO) naturally if mentioned in extra instructions.
            3. INTENT ALIGNMENT: Structure the content specifically to satisfy a {search_intent} user query.
            4. FAQ & TAKEAWAYS: {'Include a structured FAQ section' if use_faq else ''}.
            5. UNIQUE VALUE: Avoid generic fluff. Provide specific insights, step-by-step guides, or technical details.
            
            TECHNICAL REQUIREMENTS:
            - Output ONLY raw HTML (h2, h3, p, ul, li, strong).
            - No markdown code blocks.
            - If 'Generate Meta Data' is checked, include <meta-title> and <meta-description> at the very beginning.
            
            EXTRA INSTRUCTIONS: {extra_instructions}
            """

            with st.spinner(f"⏳ در حال تولید محتوای {language} با رویکرد SEO & GEO..."):
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

            st.success(f"محتوا در {duration} ثانیه تولید شد!")

            # پردازش و نمایش خروجی
            tab1, tab2, tab3 = st.tabs(["👁️ Preview Content", "💻 HTML Code", "📊 SEO/GEO Analysis"])

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
                st.write(f"**Language:** {language}")
                st.write(f"**Intent Fulfillment:** {search_intent}")
                st.progress(min(word_actual/word_count, 1.0))
                st.info("نکته GEO: استفاده از آمار دقیق و اسامی خاص (مثل نام خیابان‌ها در کالیفرنیا یا نام قوانین خاص) احتمال دیده شدن شما در موتورهای جستجوی مبتنی بر هوش مصنوعی را افزایش می‌دهد.")

        except Exception as e:
            st.error(f"خطای سیستمی: {str(e)}")

# فوتر سایت
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: grey;'>Advanced SEO & GEO Engine | Built for Sheragim | © {time.localtime().tm_year}</p>", unsafe_allow_html=True)
