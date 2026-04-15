import streamlit as st
import pandas as pd
import datetime

# --- 1. إعدادات الصفحة والتنسيق ---
st.set_page_config(page_title="النظام الذكي | ربط العمليات", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label {
        font-family: 'Rubik', sans-serif !important; direction: rtl; text-align: right;
    }
    .suggestion-box { background-color: #F2F2F7; padding: 15px; border-radius: 12px; border-right: 5px solid #34C759; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك اكتشاف الأخطاء والربط ---
def analyze_business_health(sales, mkt_spend):
    issues = []
    # سيناريو: فشل الاستهداف في التسويق
    if mkt_spend > 5000 and sales < 1000:
        issues.append({
            "المشكلة": "خلل في استهداف الجمهور (Marketing Mismatch)",
            "السبب": f"صرف مرتفع ({mkt_spend}) مقابل عائد منخفض ({sales}). الإعلانات تصل لأشخاص غير مهتمين.",
            "الحل": "إيقاف الحملة فوراً، وإعادة تحليل بيانات العملاء السابقين لضبط الاستهداف."
        })
    return issues

# --- 3. نظام الأمان ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🍏 دخول النظام")
        pwd = st.text_input("باسورد", type="password")
        if st.button("دخول"):
            if pwd == "1234": st.session_state.auth = True; st.rerun()
            else: st.error("خطأ!")
    st.stop()

# --- 4. واجهة التحكم ---
st.sidebar.title(" إدارة الربط")
page = st.sidebar.radio("المنطقة", ["لوحة التحكم حياً", "سجل الأخطاء"])

if page == "لوحة التحكم حياً":
    st.header("📊 الربط بين التسويق والمبيعات")
    
    c1, c2 = st.columns(2)
    sales = c1.number_input("المبيعات الحالية", value=500)
    mkt = c2.number_input("صرف الإعلانات", value=6000)
    
    st.divider()
    
    found_issues = analyze_business_health(sales, mkt)
    
    if found_issues:
        for issue in found_issues:
            st.error(f"🚨 اكتشاف مشكلة: {issue['المشكلة']}")
            st.markdown(f"""
                <div class="suggestion-box">
                    <strong>السبب المكتشف:</strong> {issue['السبب']}<br><br>
                    <span style='color: #34C759;'><strong>✅ الحل المقترح:</strong> {issue['الحل']}</span>
                </div><br>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ البيانات متناسقة. الاستهداف التسويقي يحقق نتائج جيدة.")

elif page == "سجل الأخطاء":
    st.header("📋 أرشيف الحلول")
    # تم تصحيح علامات التنصيص هنا لمنع الـ SyntaxError
    st.info("هذا القسم يسجل كل 'الحلول' التي تم تنفيذها بناءً على اقتراحات النظام.")
