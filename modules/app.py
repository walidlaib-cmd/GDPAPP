import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from modules.calculations import compute_macro_indicators
from modules.explanations import INDICATOR_EXPLANATIONS

# إعداد الصفحة وتفضيلات العرض
st.set_page_config(
    page_title="منصة قياس النشاط الاقتصادي | جامعة برج بوعريريج",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص واجهة المستخدم لدعم الاتجاه العربي RTL والتصميم الأكاديمي
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .academic-header {
        background: linear-gradient(135deg, #1B365D 0%, #0F2342 100%);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(27, 54, 93, 0.15);
        margin-bottom: 2rem;
        border-right: 6px solid #D97706;
    }
    
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1B365D;
    }
    
    .metric-title {
        font-size: 0.95rem;
        color: #64748B;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 1. الترويسة الأكاديمية الرسمية
st.markdown("""
<div class="academic-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h3 style="margin: 0; font-weight: 800; color: #FCD34D;">جامعة محمد البشير الإبراهيمي - برج بوعريريج</h3>
            <h4 style="margin: 4px 0; font-weight: 600; color: #E2E8F0;">كلية العلوم الاقتصادية والتجارية وعلوم التسيير</h4>
            <div style="margin-top: 10px; display: flex; gap: 15px; flex-wrap: wrap;">
                <span style="background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">📚 السنة الثانية: اقتصاد كلي</span>
                <span style="background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">👨‍🏫 الأستاذ: لعايب وليد</span>
                <span style="background: #D97706; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">مخبر المحاكاة الاقتصادية</span>
            </div>
        </div>
        <div style="text-align: left; margin-top: 10px;">
            <span style="font-size: 2.4rem;">📈</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. الشريط الجانبي للمدخلات الاقتصادية (Sidebar Inputs)
with st.sidebar:
    st.header("⚙️ معطيات التدفقات والأنشطة")
    
    # خيار تعبئة بيانات نموذجية
    preset = st.selectbox(
        "اختر سيناريو تعليمي جاهز:",
        ["سيناريو افتراضي متوازن", "حالة عجز موازنة وتجاري", "مخصص يدوي"]
    )
    
    default_vals = {
        "VPT": 2500.0, "CI": 1000.0, "TVA": 120.0, "DD": 80.0, "Sub_Imp": 30.0,
        "C": 1100.0, "I": 400.0, "G": 320.0, "X": 250.0, "M": 400.0,
        "RNFE": 40.0, "Am": 150.0, "Imp_I": 110.0, "Sub_Exp": 50.0,
        "PND": 60.0, "TA_pr": 70.0, "CS": 80.0, "TR": 90.0, "TA_Y": 100.0,
        "PIB_real": 1600.0
    }
    
    if preset == "حالة عجز موازنة وتجاري":
        default_vals["G"] = 500.0
        default_vals["M"] = 550.0
        default_vals["X"] = 200.0

    st.subheader("1. تدفقات الإنتاج والقيمة المضافة")
    vpt = st.number_input("قيمة الإنتاج الكلي (VPT)", value=default_vals["VPT"], step=50.0)
    ci = st.number_input("الاستهلاك الوسيط (CI)", value=default_vals["CI"], step=50.0)
    tva = st.number_input("الرسوم على القيمة المضافة (TVA)", value=default_vals["TVA"], step=10.0)
    dd = st.number_input("الحقوق والرسوم الجمركية (DD)", value=default_vals["DD"], step=10.0)
    sub_imp = st.number_input("إعانات الاستيراد (Sub d'Imp)", value=default_vals["Sub_Imp"], step=5.0)

    st.subheader("2. بنود الإنفاق النهائي")
    c = st.number_input("الاستهلاك العائلي النهائي (C)", value=default_vals["C"], step=50.0)
    i = st.number_input("الاستثمار الإجمالي (I)", value=default_vals["I"], step=20.0)
    g = st.number_input("الإنفاق الحكومي (G)", value=default_vals["G"], step=20.0)
    x = st.number_input("الصادرات من السلع والخدمات (X)", value=default_vals["X"], step=20.0)
    m = st.number_input("الواردات من السلع والخدمات (M)", value=default_vals["M"], step=20.0)

    st.subheader("3. التوزيع والتحويلات والضرائب")
    rnfe = st.number_input("صافي عوائد عناصر الإنتاج الخارجية (RNFE)", value=default_vals["RNFE"], step=10.0)
    am = st.number_input("اهتلاك الأصول الرأسمالية (Am)", value=default_vals["Am"], step=10.0)
    imp_i = st.number_input("الضرائب غير المباشرة (Imp I)", value=default_vals["Imp_I"], step=10.0)
    sub_exp = st.number_input("إعانات الاستغلال (Sub d'Exp)", value=default_vals["Sub_Exp"], step=5.0)
    pnd = st.number_input("الأرباح غير الموزعة (PND)", value=default_vals["PND"], step=5.0)
    ta_pr = st.number_input("الضرائب على أرباح الشركات (TA_pr)", value=default_vals["TA_pr"], step=5.0)
    cs = st.number_input("الاشتراكات الاجتماعية (CS)", value=default_vals["CS"], step=5.0)
    tr = st.number_input("التحويلات الحكومية الاجتماعية (TR)", value=default_vals["TR"], step=10.0)
    ta_y = st.number_input("الضرائب المباشرة على دخل العائلات (TA_Y)", value=default_vals["TA_Y"], step=10.0)
    
    st.subheader("4. معطيات إضافية للمقارنة الحقيقية")
    pib_real = st.number_input("الناتج المحلي الحقيقي بالأسعار الثابتة", value=default_vals["PIB_real"], step=50.0)

# تجميع المدخلات
raw_inputs = {
    "VPT": vpt, "CI": ci, "TVA": tva, "DD": dd, "Sub_Imp": sub_imp,
    "C": c, "I": i, "G": g, "X": x, "M": m,
    "RNFE": rnfe, "Am": am, "Imp_I": imp_i, "Sub_Exp": sub_exp,
    "PND": pnd, "TA_pr": ta_pr, "CS": cs, "TR": tr, "TA_Y": ta_y,
    "PIB_real": pib_real
}

# تشغيل المعالجة
results = compute_macro_indicators(raw_inputs)

# 3. عرض علامات التبويب الرئيسية (Tabs)
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 لوحة المؤشرات الكلية (Dashboard)",
    "⚖️ مقارنة طرق قياس الناتج الثلاث",
    "🔄 شجرة التدفق التراكمي للمؤشرات",
    "📖 الدليل العلمي والمفاهيمي المفصل"
])

# ----------------- التبويب 1: لوحة المؤشرات -----------------
with tab1:
    st.subheader("المؤشرات الاقتصادية السيادية الكبرى")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-title">الناتج الداخلي بسعر السوق (PIB)</div>
            <div class="metric-value">{results['PIB_pm']:,.1f}</div>
            <small style="color: #059669;">طريقة الإنفاق: C+I+G+(X-M)</small>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-title">الناتج القومي الخام (PNB)</div>
            <div class="metric-value">{results['PNB_pm']:,.1f}</div>
            <small style="color: #2563EB;">PIB + RNFE ({raw_inputs['RNFE']:+,.0f})</small>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-title">الدخل الوطني الصافي (RN)</div>
            <div class="metric-value">{results['RN']:,.1f}</div>
            <small style="color: #D97706;">بسعر تكلفة عوامل الإنتاج</small>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-title">الدخل التصرفي المتاح (Yd)</div>
            <div class="metric-value">{results['Yd']:,.1f}</div>
            <small style="color: #7C3AED;">الدخل القابل للتصرف العائلي</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # رسوم بيانية: مكونات الإنفاق والادخار
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.write("##### 📊 هيكل الإنفاق الكلي النهائي على الناتج")
        exp_df = pd.DataFrame({
            "المكون": ["الاستهلاك العائلي (C)", "الاستثمار الإجمالي (I)", "الإنفاق الحكومي (G)", "صافي الصادرات (X-M)"],
            "القيمة": [raw_inputs['C'], raw_inputs['I'], raw_inputs['G'], results['Net_Exports']]
        })
        fig_exp = px.pie(exp_df, values='القيمة', names='المكون', hole=0.45, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_exp.update_layout(margin=dict(t=20, b=20, l=20, r=20), font=dict(family="Cairo"))
        st.plotly_chart(fig_exp, use_container_width=True)
        
    with g_col2:
        st.write("##### 🏦 مصادر الادخار الكلي الوطني (ST)")
        sav_df = pd.DataFrame({
            "القطاع": ["القطاع العائلي (SM)", "قطاع المؤسسات (SE)", "القطاع الحكومي (SAP)"],
            "الادخار": [results['SM'], results['SE'], results['SAP']]
        })
        fig_sav = px.bar(sav_df, x='القطاع', y='الادخار', color='القطاع', 
                         text_auto='.1f', color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B'])
        fig_sav.update_layout(margin=dict(t=20, b=20, l=20, r=20), font=dict(family="Cairo"), showlegend=False)
        st.plotly_chart(fig_sav, use_container_width=True)

# ----------------- التبويب 2: مقارنة الطرق الثلاث -----------------
with tab2:
    st.subheader("تحليل ومطابقة طرق قياس الناتج الداخلي الخام الثلاث")
    st.info("تثبت النظرية الاقتصادية أن الناتج المقاس بطريقة القيمة المضافة يجب أن يطابق الناتج بطريقة الإنفاق والدخل عند اتساق البيانات المحاسبية.")
    
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.write("#### 1. طريقة الإنتاج والقيمة المضافة (VAB)")
        st.write(f"- قيمة الإنتاج الكلي (VPT): **{raw_inputs['VPT']:,.1f}**")
        st.write(f"- ناقص الاستهلاك الوسيط (CI): **{raw_inputs['CI']:,.1f}**")
        st.write(f"- = القيمة المضافة الكلية (VAB): **{results['VAB']:,.1f}**")
        st.write(f"- زائد الرسوم على القيمة المضافة (TVA): **{raw_inputs['TVA']:,.1f}**")
        st.write(f"- زائد الرسوم الجمركية (DD): **{raw_inputs['DD']:,.1f}**")
        st.write(f"- ناقص إعانات الاستيراد (Sub d'Imp): **{raw_inputs['Sub_Imp']:,.1f}**")
        st.success(f"**الناتج بطريقة الإنتاج (PIB_prod): {results['PIB_prod']:,.1f}**")

    with t_col2:
        st.write("#### 2. طريقة الإنفاق النهائي")
        st.write(f"- الاستهلاك النهائي العائلي (C): **{raw_inputs['C']:,.1f}**")
        st.write(f"- الاستثمار الإجمالي (I): **{raw_inputs['I']:,.1f}**")
        st.write(f"- الإنفاق العام الحكومي (G): **{raw_inputs['G']:,.1f}**")
        st.write(f"- الصادرات (X): **{raw_inputs['X']:,.1f}** | الواردات (M): **{raw_inputs['M']:,.1f}**")
        st.write(f"- صافي التجارة الخارجية (X - M): **{results['Net_Exports']:,.1f}**")
        st.success(f"**الناتج بطريقة الإنفاق (PIB_exp): {results['PIB_exp']:,.1f}**")

    st.markdown("---")
    st.write("#### 3. فحص التوازن الكلي: الحقن والتسربات (Equilibrium Check)")
    eq1, eq2, eq3 = st.columns(3)
    eq1.metric("إجمالي التسربات (S + T + M)", f"{results['Leakages']:,.1f}")
    eq2.metric("إجمالي الحقن (I + G + X)", f"{results['Injections']:,.1f}")
    diff = results['Injections'] - results['Leakages']
    eq3.metric("صافي الفجوة التوازنية", f"{diff:,.1f}", delta=f"{diff:,.1f}", delta_color="normal")

# ----------------- التبويب 3: شجرة التدفق التراكمي -----------------
with tab3:
    st.subheader("التسلسل الانتقالي التراكمي للمؤشرات (من الإنتاج إلى الادخار)")
    
    waterfall_data = [
        {"المرحلة": "قيمة الإنتاج الكلي (VPT)", "التغير": raw_inputs['VPT']},
        {"المرحلة": "استبعاد الاستهلاك الوسيط (-CI)", "التغير": -raw_inputs['CI']},
        {"المرحلة": "صافي الضرائب الجمركية و TVA", "التغير": raw_inputs['TVA'] + raw_inputs['DD'] - raw_inputs['Sub_Imp']},
        {"المرحلة": "الناتج الداخلي الخام (PIB)", "التغير": 0}, # نقطة ارتكاز
        {"المرحلة": "صافي عوائد العوامل الخارجية (RNFE)", "التغير": raw_inputs['RNFE']},
        {"المرحلة": "استبعاد الاهتلاك (-Am)", "التغير": -raw_inputs['Am']},
        {"المرحلة": "صافي الضرائب غير المباشرة", "التغير": -raw_inputs['Imp_I'] + raw_inputs['Sub_Exp']},
        {"المرحلة": "الدخل الوطني (RN)", "التغير": 0},
        {"المرحلة": "اقتطاعات الشركات والتأمينات", "التغير": -(raw_inputs['PND'] + raw_inputs['TA_pr'] + raw_inputs['CS'])},
        {"المرحلة": "التحويلات الحكومية (+TR)", "التغير": raw_inputs['TR']},
        {"المرحلة": "الدخل الشخصي (RP)", "التغير": 0},
        {"المرحلة": "الضرائب المباشرة (-TA_Y)", "التغير": -raw_inputs['TA_Y']},
        {"المرحلة": "الدخل المتاح (Yd)", "التغير": 0}
    ]
    
    st.table(pd.DataFrame(waterfall_data))
    st.caption("الجدول يوضح مراحل انتقال القيمة المالية عبر مختلف مستويات النشاط الاقتصادي وفقاً للملخص النظري للمقرر.")

# ----------------- التبويب 4: الدليل العلمي والمفاهيمي -----------------
with tab4:
    st.subheader("المعجم الاقتصادي التفاعلي لمؤشرات النشاط الكلي")
    
    for key, info in INDICATOR_EXPLANATIONS.items():
        with st.expander(f"📌 {info['name']} — [{key}]"):
            st.markdown(f"**الصيغة الرياضية:** `{info['formula']}`")
            st.write(info['description'])
            
    st.markdown("---")
    st.subheader("📚 مراجع نظرية موثوقة لمزيد من التوسع")
    st.markdown("""
    1. **نظام الحسابات القومية (SNA 2008):** الصادر عن الأمم المتحدة وصندوق النقد الدولي والبنك الدولي.
    2. **الاقتصاد الكلي (Macroeconomics):** N. Gregory Mankiw, 10th Edition.
    3. **محاضرات وتطبيقات مقياس الاقتصاد الكلي:** الأستاذ لعايب وليد، جامعة برج بوعريريج.
    """)

# تذييل الصفحة
st.markdown("---")
st.markdown(
    "<center><small style='color: #64748B;'>تم تطوير هذه المنصة التعليمية لصالح طلبة كلية العلوم الاقتصادية والتجارية وعلوم التسيير - جامعة برج بوعريريج</small></center>", 
    unsafe_allow_html=True
)
