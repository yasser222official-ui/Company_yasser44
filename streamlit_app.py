import streamlit as st
import pandas as pd
import datetime
import time

# --- 1. إعدادات التصميم (Apple Style) ---
st.set_page_config(page_title="نظام التشخيص الذكي", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3 {
        font-family: 'Rubik', sans-serif !important; direction: rtl; text-align: right;
    }
    .diagnostic-card {
        padding: 20px; border-radius: 15px; margin-bottom: 20px;
        border-right: 10px solid; background-color: #F8F9FA;
    }
    .source-tag { background-color: #E1E1E6; padding: 5px 10px; border-radius: 8px; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك التشخيص الذكي (The Intelligence Engine) ---
def run_diagnostic(sales, mkt_spend, gps_status):
    diagnostics = []
    
    # السيناريو 1: الربط بين التسويق والمبيعات
    if mkt_spend > 5000 and sales < 1000:
        diagnostics.append({
            "المشكلة": "هدر في ميزانية التسويق",
            "المصدر": "إعلانات فيسبوك / استهداف الجمهور",
            "التفاصيل": "الميزانية تُصرف بالكامل لكن العائد لا يتجاوز 20% من المتوقع.",
            "الحل المقترح": "إيقاف حملة 'الجمهور العام' وتفعيل حملة 'إعادة الاستهداف' للعملاء المهتمين فقط.",
            "النوع": "خطير"
        })
        
    # السيناريو 2: الربط بين المبيعات والتشغيل (الـ GPS)
    if sales < 500 and gps_status == "متوقف":
        diagnostics.append({
            "المشكلة": "توقف حركة المندوبين",
            "المصدر": "أسطول التوزيع / نظام التتبع",
            "التفاصيل": "المبيعات متوقفة بسبب عدم تحرك السيارات من المركز الرئيسي.",
            "الحل المقترح": "التواصل مع مشرف الحركة للتأكد من خروج خطوط السير في موعدها.",
            "النوع": "تحذير"
        })
        
    return diagnostics

# --- 3. واجهة التحكم والتحديث اللحظي ---
st.title("🍏 نظام التشخيص اللحظي (Nerve Center)")

# محاكاة البيانات القادمة من البرامج الأخرى
st.sidebar.header("🔌 مصادر البيانات الحية")
live_sales = st.sidebar.slider("المبيعات الحالية (ERP)", 0, 10000, 500)
live_mkt = st.sidebar.slider("صرف التسويق (Ads)", 0, 10000, 6000)
live_gps = st.sidebar.selectbox("حالة أسطول الشحن (GPS)", ["يعمل", "متوقف"])

# التحديث اللحظي (Real-time Simulation)
st.write(f"⏱️ آخر تحديث للنظام: {datetime.datetime.now().strftime('%H:%M:%S')}")

# تنفيذ التشخيص
results = run_diagnostic(live_sales, live_mkt, live_gps)

if results:
    for res in results:
        color = "#FF3B30" if res["النوع"] == "خطير" else "#FF9500"
        st.markdown(f"""
            <div class="diagnostic-card" style="border-right-color: {color};">
                <h3 style="color: {color};">🚨 المشكلة: {res['المشكلة']}</h3>
                <p>📍 <strong>مصدر المشكلة:</strong> <span class="source-tag">{res['المصدر']}</span></p>
                <p>📝 <strong>التوصيف:</strong> {res['التفاصيل']}</p>
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px;">
                    <strong style="color: #2E7D32;">✅ الحل المقترح:</strong> {res['الحل']}
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.success("✨ جميع الأنظمة مرتبطة ببعضها وتعمل بشكل مثالي. لا توجد انحرافات مكتشفة.")

# --- 4. سجل الحلول التاريخي ---
st.divider()
st.subheader("📋 سجل الإجراءات المتخذة")
if 'history' not in st.session_state:
    st.session_state.history = []

if results and st.button("تأكيد تنفيذ الحلول المقترحة"):
    for r in results:
        st.session_state.history.append({
            "التاريخ": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "المشكلة": r["المشكلة"],
            "الإجراء": "تم تطبيق الحل المقترح"
        })
    st.success("تم تحديث السجل!")

if st.session_state.history:
    st.table(pd.DataFrame(st.session_state.history))
