import streamlit as st
import pandas as pd
import datetime

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="نظام التشخيص الذكي", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label {
        font-family: 'Rubik', sans-serif !important; direction: rtl; text-align: right;
    }
    .diagnostic-card {
        padding: 20px; border-radius: 15px; margin-bottom: 20px;
        border-right: 10px solid #FF3B30; background-color: #F8F9FA;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .source-tag { background-color: #E1E1E6; padding: 5px 10px; border-radius: 8px; font-size: 0.85em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك اكتشاف المشكلة والمصدر والحل ---
def run_diagnostic(sales, mkt_spend):
    diagnostics = []
    
    # ربط التسويق بالمبيعات (تحليل الاستهداف)
    if mkt_spend > 5000 and sales < 1000:
        diagnostics.append({
            "المشكلة": "فشل استهداف الحملة الإعلانية",
            "المصدر": "إعلانات التسويق (Targeting Settings)",
            "التوصيف": "الميزانية تُستنزف دون تحقيق مبيعات تناسب الصرف، مما يعني أن الإعلان يظهر للجمهور الخطأ.",
            "الحل": "إيقاف الحملة فوراً، وإعادة ضبط الـ Pixel لتركيز الاستهداف على 'العملاء المهتمين' فقط."
        })
    
    # مثال لمشكلة تشغيلية أخرى
    if sales == 0:
        diagnostics.append({
            "المشكلة": "توقف تدفق المبيعات الرقمية",
            "المصدر": "بوابة الدفع / نظام الـ ERP",
            "التوصيف": "لا توجد عمليات مسجلة رغم وجود زيارات، قد يكون هناك عطل في الربط التقني.",
            "الحل": "فحص اتصال الـ API بين الموقع ونظام المحاسبة فوراً."
        })
        
    return diagnostics

# --- 3. نظام الأمان ---
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align:center;'>🍏 دخول النظام</h2>", unsafe_allow_html=True)
        pwd = st.text_input("باسورد", type="password")
        if st.button("دخول"):
            if pwd == "1234":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- 4. لوحة التحكم الحية ---
st.title("🍏 نظام التشخيص اللحظي (Nerve Center)")

# محاكاة البيانات الحية (تحديث لحظي)
with st.sidebar:
    st.header("🔌 ربط البيانات")
    live_sales = st.number_input("المبيعات (Live ERP)", value=500)
    live_mkt = st.number_input("صرف الإعلانات (Live Ads)", value=6000)

# تنفيذ التشخيص
results = run_diagnostic(live_sales, live_mkt)

if results:
    st.subheader("🚨 المشكلات المكتشفة الآن")
    for res in results:
        st.markdown(f"""
            <div class="diagnostic-card">
                <h3 style="color: #FF3B30;">⚠️ المشكلة: {res['المشكلة']}</h3>
                <p>📍 <strong>المصدر:</strong> <span class="source-tag">{res['المصدر']}</span></p>
                <p>📝 <strong>التوصيف:</strong> {res['التوصيف']}</p>
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; border-right: 5px solid #34C759;">
                    <strong style="color: #2E7D32;">✅ الحل المقترح:</strong> {res['الحل']}
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.success("✨ جميع الأنظمة مرتبطة وتعمل بكفاءة. لا توجد انحرافات في البيانات.")

# سجل الحلول التاريخي
st.divider()
st.subheader("📋 سجل الإجراءات")
if 'history' not in st.session_state: st.session_state.history = []

if results and st.button("تأكيد تنفيذ الحلول المقترحة"):
    for r in results:
        st.session_state.history.append({
            "التاريخ": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "المصدر": r["المصدر"],
            "المشكلة": r["المشكلة"],
            "الحالة": "تم الحل"
        })
    st.rerun()

if st.session_state.history:
    st.table(pd.DataFrame(st.session_state.history))
