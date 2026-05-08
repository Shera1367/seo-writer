import streamlit as st
from openai import OpenAI
import time

# تنظیمات پیشرفته صفحه
st.set_page_config(
    page_title="Professional AI SEO Writer",
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
st.title("🚀 Professional AI SEO Content Engine")
st.markdown("---")

# ستون‌بندی تنظیمات در سایدبار
with st.sidebar:
    st.header("⚙️ Settings")
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
    st.markdown("### SEO Checklist")
    use_faq = st.checkbox("Include FAQ Section", value=True)
    use_takeaways = st.checkbox("Include Key Takeaways", value=True)
    generate_meta = st.checkbox("Generate Meta Tags", value=True)

# بخش ورودی‌های اصلی
col1, col2 = st.columns([1, 1])

with col1:
    article_title = st.text_input("عنوان مقاله (Article Title)", placeholder="e.g. The Future of Personal Injury Law in California")
    keywords = st.text_area("کلمات کلیدی (Target Keywords)", placeholder="primary keyword, secondary keyword, LSI keywords...", help="با کاما جدا کنید.")

with col2:
    suggested_headings = st.text_area("ساختار پیشنهادی (Suggested Headings)", placeholder="Introduction\nKey Trends\nCase Studies\nConclusion")
    extra_instructions = st.text_area("پیشنهادات اضافی (Extra Instructions)", placeholder="e.g. Focus on Woodland Hills area, mention E-E-A-T principles...")

# دکمه تولید محتوا
if st.button("✨ GENERATE SEO CONTENT"):
    if not article_title or not keywords:
        st.warning("لطفاً عنوان و کلمات کلیدی را وارد کنید.")
    else:
        try:
            client = OpenAI(api_key=API_KEY)
            
            # مهندسی پرامپت حرفه‌ای برای سئو
            system_prompt = "You are a world-class SEO specialist and expert content writer with 10+ years of experience in Digital Marketing."
            
            user_prompt = f"""
            Write a high-quality, comprehensive, and SEO-optimized article in English.
            
            PROJECT DETAILS:
            - Title: {article_title}
            - Keywords: {keywords}
            - Headings: {suggested_headings}
            - Tone: {tone}
            - Target Length: {word_count} words
            - FAQ Section: {'Yes' if use_faq else 'No'}
            - Key Takeaways: {'Yes' if use_takeaways else 'No'}
            - Generate Meta Data: {'Yes' if generate_meta else 'No'}
            - Extra Instructions: {extra_instructions}
            
            TECHNICAL REQUIREMENTS:
            1. Output MUST be in raw HTML (using <h2>, <h3>, <p>, <ul>, <li>, <strong>).
            2. Do NOT use markdown code blocks (no ```html).
            3. Do NOT include <html>, <head>, or <body>.
            4. If 'Generate Meta Data' is Yes, start the response with <meta-title> and <meta-description> tags.
            5. Follow E-E-A-T guidelines.
            """

            with st.spinner("⏳ در حال تولید محتوا توسط هوش مصنوعی... این فرایند ممکن است ۱ تا ۲ دقیقه زمان ببرد."):
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

            st.success(f"محتوا با موفقیت در {duration} ثانیه تولید شد!")

            # پردازش و نمایش خروجی
            tab1, tab2, tab3 = st.tabs(["👁️ Preview Content", "💻 HTML Code", "📊 SEO Stats"])

            with tab1:
                st.markdown("### Article Preview")
                st.divider()
                st.markdown(content, unsafe_allow_html=True)

            with tab2:
                st.markdown("### HTML Source Code")
                st.code(content, language="html")
                st.download_button(
                    label="📥 Download as HTML file",
                    data=content,
                    file_name=f"{article_title.lower().replace(' ', '_')}.html",
                    mime="text/html"
                )

            with tab3:
                # آنالیز ساده سئو
                word_actual = len(content.split())
                st.write(f"**Actual Word Count:** {word_actual}")
                st.write(f"**SEO Density:** Optimized for {len(keywords.split(','))} keywords.")
                st.progress(min(word_actual/word_count, 1.0))
                st.info("نکته: برای سئو بهتر، تصاویر مرتبط و لینک‌های داخلی را به صورت دستی در ویرایشگر سایت خود اضافه کنید.")

        except Exception as e:
            st.error(f"خطای سیستمی: {str(e)}")

# فوتر سایت
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: grey;'>Built for Professional Marketers | © {time.localtime().tm_year}</p>", unsafe_allow_html=True)
