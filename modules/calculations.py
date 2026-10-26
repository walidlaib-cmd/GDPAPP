"""
الوحدة الحسابية للمؤشرات الاقتصادية الكلية
مبنية على المنهجية الواردة في مقررات جامعة محمد البشير الإبراهيمي
"""

from typing import Dict, Any

def compute_macro_indicators(inputs: Dict[str, float]) -> Dict[str, Any]:
    # 1. طريقة الإنتاج والقيمة المضافة
    vab = inputs['VPT'] - inputs['CI']
    pib_pm_prod = vab + inputs['TVA'] + inputs['DD'] - inputs['Sub_Imp']
    
    # 2. طريقة الإنفاق
    net_exports = inputs['X'] - inputs['M']
    pib_pm_exp = inputs['C'] + inputs['I'] + inputs['G'] + net_exports
    
    # 3. مؤشرات السلسلة الدورية حتى الادخار الكلي
    # اعتماد الناتج الداخلي الخام بسعر السوق
    pib_pm = pib_pm_exp if inputs.get('use_exp_as_base', True) else pib_pm_prod
    
    pnb_pm = pib_pm + inputs['RNFE']
    pnn_pm = pnb_pm - inputs['Am']
    
    # الدخل الوطني (بسعر تكلفة عوامل الإنتاج)
    rn = pnn_pm - inputs['Imp_I'] + inputs['Sub_Exp']
    
    # الدخل الشخصي
    rp = rn - inputs['PND'] - inputs['TA_pr'] - inputs['CS'] + inputs['TR']
    
    # الدخل التصرفي (المتاح)
    yd = rp - inputs['TA_Y']
    
    # الادخارات
    sm = yd - inputs['C']                    # الادخار العائلي
    se = inputs['PND'] + inputs['Am']        # ادخار المؤسسات
    
    # الضرائب الكلية لاحتساب الادخار الحكومي
    # TA = الضرائب غير المباشرة + ضرائب الشركات + ضرائب العائلات + الرسوم الجمركية و TVA
    total_tax = (inputs['TA_Y'] + inputs['TA_pr'] + inputs['Imp_I'] + 
                 inputs['TVA'] + inputs['DD'])
    sap = total_tax - (inputs['G'] + inputs['TR']) # الادخار الحكومي
    st = sm + se + sap                             # الادخار الكلي
    
    # التحقق من توازن الحقن والتسرب
    leakages = sm + (total_tax - inputs['TR']) + inputs['M']
    injections = inputs['I'] + inputs['G'] + inputs['X']
    
    # مؤشرات إضافية (أرقام قياسية ومعدلات مشتقة)
    gdp_deflator = (pib_pm / inputs['PIB_real'] * 100) if inputs.get('PIB_real', 0) > 0 else 100.0
    apc = (inputs['C'] / yd) if yd > 0 else 0.0
    aps = (sm / yd) if yd > 0 else 0.0
    
    return {
        "VAB": vab,
        "PIB_prod": pib_pm_prod,
        "PIB_exp": pib_pm_exp,
        "Net_Exports": net_exports,
        "PIB_pm": pib_pm,
        "PNB_pm": pnb_pm,
        "PNN_pm": pnn_pm,
        "RN": rn,
        "RP": rp,
        "Yd": yd,
        "SM": sm,
        "SE": se,
        "SAP": sap,
        "ST": st,
        "Total_Tax": total_tax,
        "Leakages": leakages,
        "Injections": injections,
        "GDP_Deflator": gdp_deflator,
        "APC": apc,
        "APS": aps
    }
