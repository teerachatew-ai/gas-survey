# -*- coding: utf-8 -*-
"""UI translations for the customer survey page (th = matches official form)."""

LANGS = ("th", "en", "zh")

TEXTS = {
    # ---------- header / general ----------
    "brand": {
        "th": "PTT NGD — บริษัท ปตท. จำหน่ายก๊าซธรรมชาติ จำกัด",
        "en": "PTT NGD — PTT Natural Gas Distribution Co., Ltd.",
        "zh": "PTT NGD — PTT天然气配送有限公司",
    },
    "title": {
        "th": "แบบสอบถามความต้องการใช้พลังงานของโรงงาน",
        "en": "Factories’ Energy Consumption Questionnaire",
        "zh": "工厂能源需求调查问卷",
    },
    "subtitle": {
        "th": "Factories’ Energy Consumption Questionnaire",
        "en": "แบบสอบถามความต้องการใช้พลังงานของโรงงาน",
        "zh": "Factories’ Energy Consumption Questionnaire",
    },
    "flash_company": {
        "th": "กรุณากรอกชื่อบริษัท / Please enter your company name",
        "en": "Please enter your company name",
        "zh": "请填写公司名称",
    },
    "flash_consent": {
        "th": "กรุณากดยอมรับนโยบาย Compliance & Sanctions ก่อนส่งแบบสอบถาม",
        "en": "Please accept the Compliance & Sanctions policy before submitting",
        "zh": "提交前请先同意合规与制裁政策",
    },
    # ---------- section 1 ----------
    "s1_title": {
        "th": "1. ข้อมูลทั่วไป / General Information",
        "en": "1. General Information",
        "zh": "1. 基本信息 / General Information",
    },
    "part13": {"th": "(ส่วนที่ Part 1/3)", "en": "(Part 1/3)", "zh": "（第 1/3 部分）"},
    "channel": {"th": "ช่องทาง:", "en": "Channel:", "zh": "渠道："},
    "ch_inquire": {"th": "สอบถาม / Inquire", "en": "Inquire", "zh": "咨询 / Inquire"},
    "ch_fax": {"th": "ทางโทรสาร / Fax", "en": "By Fax", "zh": "传真 / Fax"},
    "ch_email": {"th": "ทางอีเมล์ / By E-mail", "en": "By E-mail", "zh": "电子邮件 / E-mail"},
    "ch_other": {"th": "อื่นๆ / Other", "en": "Other", "zh": "其他 / Other"},
    "specify_ph": {"th": "ระบุ...", "en": "Please specify...", "zh": "请注明..."},
    "f_company": {"th": "ชื่อบริษัท / Company Name *", "en": "Company Name *", "zh": "公司名称 / Company Name *"},
    "f_address": {"th": "ที่ตั้ง / Address", "en": "Address", "zh": "地址 / Address"},
    "f_contact": {"th": "ชื่อผู้ติดต่อ / Contact Person", "en": "Contact Person", "zh": "联系人 / Contact Person"},
    "f_email": {"th": "อีเมล์ / E-mail", "en": "E-mail", "zh": "电子邮箱 / E-mail"},
    "f_nationality": {"th": "สัญชาติของบริษัท / Nationality", "en": "Company Nationality", "zh": "公司国籍 / Nationality"},
    "f_bustype": {"th": "ประเภทธุรกิจ / Business Type", "en": "Business Type", "zh": "业务类型 / Business Type"},
    "f_mobile": {"th": "มือถือ / Mobile Phone", "en": "Mobile Phone", "zh": "手机 / Mobile Phone"},
    "f_tel": {"th": "โทรศัพท์ / Tel.", "en": "Tel.", "zh": "电话 / Tel."},
    "f_fax": {"th": "โทรสาร / Fax.", "en": "Fax.", "zh": "传真 / Fax."},
    # ---------- section 2 ----------
    "s2_title": {
        "th": "2. ปริมาณการใช้เชื้อเพลิงในการผลิต",
        "en": "2. Fuel Consumption in Production",
        "zh": "2. 生产燃料使用量",
    },
    "s21_head": {
        "th": "2.1 ปริมาณการใช้เชื้อเพลิงเดิมต่อเดือนย้อนหลัง 12 เดือนล่าสุด หรือความต้องการใช้เชื้อเพลิงที่คาดว่าจะใช้สำหรับ 12 เดือน",
        "en": "2.1 Monthly existing fuel consumption of the last 12 months, or expected fuel consumption for the next 12 months",
        "zh": "2.1 过去12个月的每月燃料使用量，或预计未来12个月的燃料需求量",
    },
    "s21_hint": {
        "th": "/ Monthly existing fuel consumption of last 12 months or Expected fuel consumption for 12 months in each fuel. <em>(For example; Jan-09)</em><br>(ในกรณีมีเชื้อเพลิงมากกว่า 1 ชนิด สามารถระบุในเชื้อเพลิงที่ 2, 3 ตามลำดับ / If fuel type is more than 1 type, please specify in Fuel type 2, 3.)",
        "en": "Specify the consumption per month for each fuel. <em>(Month format example: Jan-25)</em><br>(If more than one fuel type is used, please specify them under Fuel type 2 and 3.)",
        "zh": "请填写每种燃料的每月使用量。<em>（月份格式例如：Jan-25）</em><br>（如使用多于一种燃料，请分别填写在燃料2、燃料3。）",
    },
    "fuel_type_n": {"th": "เชื้อเพลิงชนิดที่ {n} / Fuel Type {n}", "en": "Fuel Type {n}", "zh": "燃料 {n} / Fuel Type {n}"},
    "opt_fuel_oil": {"th": "น้ำมันเตา / Fuel Oil", "en": "Fuel Oil", "zh": "重油 / Fuel Oil"},
    "opt_grade": {"th": "เกรด / Grade:", "en": "Grade:", "zh": "等级 / Grade："},
    "opt_lpg": {"th": "ก๊าซหุงต้ม / LPG", "en": "LPG", "zh": "液化石油气 / LPG"},
    "opt_diesel": {"th": "ดีเซล / Diesel", "en": "Diesel", "zh": "柴油 / Diesel"},
    "opt_ng": {"th": "ก๊าซธรรมชาติ / Natural Gas", "en": "Natural Gas", "zh": "天然气 / Natural Gas"},
    "opt_other": {"th": "อื่น ๆ / Other", "en": "Other", "zh": "其他 / Other"},
    "unit_head": {"th": "หน่วยปริมาณ / Consumption unit", "en": "Consumption unit", "zh": "用量单位 / Unit"},
    "opt_liter": {"th": "ลิตร / Liter", "en": "Liter", "zh": "升 / Liter"},
    "opt_kg": {"th": "กิโลกรัม / kilogram", "en": "Kilogram", "zh": "公斤 / Kilogram"},
    "opt_mmbtu": {"th": "ล้านบีทียู / MMBtu", "en": "MMBtu", "zh": "百万英热单位 / MMBtu"},
    "tbl_month": {"th": "เดือน-ปี /<br>Month-Yr", "en": "Month-Yr", "zh": "月份-年份<br>Month-Yr"},
    "tbl_cons": {"th": "ปริมาณ / Consumption", "en": "Consumption", "zh": "用量 / Consumption"},
    "tbl_price": {"th": "ราคา / Price", "en": "Price", "zh": "价格 / Price"},
    "tbl_price_unit": {"th": "(บาทต่อหน่วย / Baht per unit)", "en": "(Baht per unit)", "zh": "（泰铢/单位）"},
    "month_ph": {"th": "เช่น Jan-25", "en": "e.g. Jan-25", "zh": "例如 Jan-25"},
    "s22_head": {
        "th": "2.2 แนวโน้มปริมาณการใช้ก๊าซธรรมชาติต่อปีในอนาคต / Yearly expected your Natural gas consumption in the future <em>(For example; Year 2010)</em>",
        "en": "2.2 Expected yearly natural gas consumption in the future <em>(Year example: 2027)</em>",
        "zh": "2.2 未来每年天然气需求趋势 <em>（年份例如：2027）</em>",
    },
    "year_n": {"th": "ปีที่ {n} / {sfx} Year", "en": "Year {n}", "zh": "第 {n} 年"},
    "tbl_expected": {"th": "Expected", "en": "Expected", "zh": "预计 / Expected"},
    "tbl_year": {"th": "(Year)", "en": "(Year)", "zh": "（年份 / Year）"},
    "tbl_cons_yr": {"th": "Consumption (MMBtu/yr)", "en": "Consumption (MMBtu/yr)", "zh": "用量 Consumption (MMBtu/yr)"},
    "tbl_cap_yr": {"th": "Capacity (Sm3/hr)", "en": "Capacity (Sm3/hr)", "zh": "产能 Capacity (Sm3/hr)"},
    "year_ph": {"th": "เช่น 2027", "en": "e.g. 2027", "zh": "例如 2027"},
    # ---------- section 3 ----------
    "s3_title": {
        "th": "3. ความต้องการใช้พลังงาน / Energy Usage",
        "en": "3. Energy Usage",
        "zh": "3. 能源需求 / Energy Usage",
    },
    "part23": {"th": "(ส่วนที่ Part 2/3)", "en": "(Part 2/3)", "zh": "（第 2/3 部分）"},
    "s31_head": {"th": "3.1 โครงการและแผนงาน / Project and Plan", "en": "3.1 Project and Plan", "zh": "3.1 项目与计划 / Project and Plan"},
    "col_current": {"th": "โครงการปัจจุบัน /<br>Current Project", "en": "Current Project", "zh": "当前项目<br>Current Project"},
    "col_expansion": {"th": "โครงการกำลังก่อสร้าง – แผนงาน /<br>Expansion Plan", "en": "Expansion Plan", "zh": "在建项目－扩建计划<br>Expansion Plan"},
    "row_product": {"th": "ประเภทสินค้าที่ผลิต / Product", "en": "Product", "zh": "生产产品类型 / Product"},
    "row_startup": {"th": "วัน / เดือน / ปี ที่เริ่มผลิต (Start-up: Date / Month / Year)", "en": "Start-up date (Date / Month / Year)", "zh": "开始生产日期（日/月/年）"},
    "row_ophour": {"th": "ระยะเวลาปฏิบัติงาน / Operating cycle (ชั่วโมงต่อวัน / hour per day)", "en": "Operating cycle (hours per day)", "zh": "运行时间（小时/天）"},
    "row_opday": {"th": "(วันต่อปี / day per year)", "en": "(days per year)", "zh": "（天/年）"},
    "s32_head": {"th": "3.2 ความต้องการใช้ก๊าซธรรมชาติ / To use Natural Gas", "en": "3.2 Natural Gas Requirement", "zh": "3.2 天然气需求 / Natural Gas"},
    "f_location": {
        "th": "(1) ตำแหน่งที่ตั้งโรงงาน / Plant Location [นิคมอุตสาหกรรม, สวนอุตสาหกรรม, เขตอุตสาหกรรม / Industrial Estate]",
        "en": "(1) Plant Location [Industrial Estate / Industrial Park / Industrial Zone]",
        "zh": "(1) 工厂位置 / Plant Location（工业园区）",
    },
    "f_landplot": {"th": "ที่ดินแปลงที่ / Land plot number", "en": "Land plot number", "zh": "地块编号 / Land plot number"},
    "f_purpose": {
        "th": "(2) วัตถุประสงค์ของการใช้เชื้อเพลิง / Using Purpose (เลือกได้มากกว่า 1 ข้อ)",
        "en": "(2) Using Purpose (select all that apply)",
        "zh": "(2) 燃料用途（可多选）/ Using Purpose",
    },
    "p_steam": {"th": "ผลิตไอน้ำ / Steam Production", "en": "Steam Production", "zh": "蒸汽生产 / Steam Production"},
    "p_pressure": {"th": "ความดัน/Steam Pressure", "en": "Steam Pressure", "zh": "蒸汽压力 / Steam Pressure"},
    "p_drying": {"th": "อบแห้ง / Drying", "en": "Drying", "zh": "烘干 / Drying"},
    "p_melting": {"th": "หลอม / Melting", "en": "Melting", "zh": "熔炼 / Melting"},
    "p_other": {"th": "อื่นๆ ระบุ / Others", "en": "Others (specify)", "zh": "其他（请注明）/ Others"},
    "f_supplydate": {
        "th": "(3) ช่วงเวลาที่ต้องการใช้ก๊าซธรรมชาติ / Natural Gas supplying date required (DD/MM/YY)",
        "en": "(3) Natural Gas supplying date required (DD/MM/YY)",
        "zh": "(3) 需要供气的日期（日/月/年 DD/MM/YY）",
    },
    "supply_ph": {"th": "เช่น 01/01/27", "en": "e.g. 01/01/27", "zh": "例如 01/01/27"},
    "f_pressure": {
        "th": "(4) แรงดันที่ต้องการ / Natural Gas pressure supply required [For example: Standard pressure supply are 1, or 1.5 Bar (gauge)]",
        "en": "(4) Natural Gas pressure supply required [e.g. standard supply: 1 or 1.5 Bar (gauge)]",
        "zh": "(4) 所需供气压力 [标准供气压力例如 1 或 1.5 Bar (gauge)]",
    },
    "pressure_ph": {"th": "เช่น 1.5 Bar (g)", "en": "e.g. 1.5 Bar (g)", "zh": "例如 1.5 Bar (g)"},
    "s33_head": {
        "th": "3.3 รายละเอียดเครื่องจักรที่ใช้พลังงาน / Type of Heating Machines and Heating Capacity",
        "en": "3.3 Type of Heating Machines and Heating Capacity",
        "zh": "3.3 用能设备详情 / Heating Machines and Capacity",
    },
    "s33_hint": {
        "th": "<em>For example;</em> Machine type: Water Steam boiler, Air-Heat, Furnace &nbsp; Capacity: 200,000 Kcal/hr, 400,000 Btu/hr, 11 MW, 50,000 MJ, 100m3/hr<br>Operating hours/day: 15 hours/day &nbsp; Working day/year: 340 days/year &nbsp; Operating Character: Low-Fire / High-Fire, On-OFF, Steady, Fluctuate &nbsp; Quantity: 2 machines",
        "en": "<em>Example:</em> Machine type: Water Steam boiler, Air-Heat, Furnace &nbsp; Capacity: 200,000 Kcal/hr, 400,000 Btu/hr, 11 MW, 50,000 MJ, 100m3/hr<br>Operating hours/day: 15 hours/day &nbsp; Working days/year: 340 days/year &nbsp; Operating Character: Low-Fire / High-Fire, On-OFF, Steady, Fluctuate &nbsp; Quantity: 2 machines",
        "zh": "<em>例如：</em>设备类型：蒸汽锅炉、热风机、熔炉 &nbsp; 功率：200,000 Kcal/hr、400,000 Btu/hr、11 MW、50,000 MJ、100m3/hr<br>运行时间：15小时/天 &nbsp; 工作天数：340天/年 &nbsp; 运行特性：Low-Fire / High-Fire、On-OFF、Steady、Fluctuate &nbsp; 数量：2台",
    },
    "machine_no": {"th": "ประเภทของเครื่องจักรที่ / No {n}", "en": "Machine No. {n}", "zh": "设备 {n} / Machine No. {n}"},
    "m_type": {"th": "ประเภทเครื่องจักร / Machine type", "en": "Machine type", "zh": "设备类型 / Machine type"},
    "m_capacity": {"th": "อัตราการใช้พลังงาน / Capacity", "en": "Capacity", "zh": "能耗功率 / Capacity"},
    "m_ophour": {"th": "ระยะเวลาการทำงานของเครื่องจักร / Operating (hours/day)", "en": "Operating (hours/day)", "zh": "运行时间（小时/天）"},
    "m_days": {"th": "Working days /year", "en": "Working days /year", "zh": "工作天数（天/年）"},
    "m_char": {"th": "ลักษณะการทำงาน / Operating Character", "en": "Operating Character", "zh": "运行特性 / Operating Character"},
    "m_qty": {"th": "จำนวน / Quantity", "en": "Quantity", "zh": "数量 / Quantity"},
    "s33_note": {
        "th": "<u>หมายเหตุ</u>: กรณีเครื่องจักรมากกว่า 4 เครื่อง กรุณาระบุรายละเอียดเพิ่มเติมโดยติดต่อเจ้าหน้าที่ / if there are more than 5 machines, please duplicate part 2/2 and can write more details.",
        "en": "<u>Note</u>: if there are more than 4 machines, please contact our staff to provide further details.",
        "zh": "<u>注</u>：如设备超过4台，请联系工作人员补充详细信息。",
    },
    # ---------- section 4 ----------
    "s4_title": {
        "th": "4. ความต้องการใช้ไฟฟ้า และ ความเย็น / Type of Heating Machines and Heating Capacity",
        "en": "4. Electricity and Chiller Demand",
        "zh": "4. 电力与制冷需求",
    },
    "part33": {"th": "(ส่วนที่ Part 3/3)", "en": "(Part 3/3)", "zh": "（第 3/3 部分）"},
    "s41_head": {"th": "4.1 ปริมาณการใช้ไฟฟ้าในโรงงาน / Electricity Demand", "en": "4.1 Electricity Demand", "zh": "4.1 工厂用电量 / Electricity Demand"},
    "e_bill": {"th": "แนบบิลค่าไฟฟ้า/Electricity bill (ถ้ามี)", "en": "Electricity bill attached (if any)", "zh": "附电费单（如有）"},
    "e_profile": {"th": "Weekly/Monthly Electricty Load Profile", "en": "Weekly/Monthly Electricity Load Profile", "zh": "每周/每月用电负荷曲线"},
    "e_base": {"th": "Base Load (Mwh)", "en": "Base Load (Mwh)", "zh": "基础负荷 Base Load (Mwh)"},
    "e_peak": {"th": "Peak (Mwh)", "en": "Peak (Mwh)", "zh": "峰值 Peak (Mwh)"},
    "e_offpeak": {"th": "Off Peak (Mwh)", "en": "Off Peak (Mwh)", "zh": "非峰值 Off Peak (Mwh)"},
    "e_source": {"th": "ปัจจุบันซื้อไฟฟ้าจาก / Electricity Source", "en": "Current Electricity Source", "zh": "当前电力来源 / Electricity Source"},
    "voltage": {"th": "ระดับแรงดัน", "en": "Voltage level", "zh": "电压等级"},
    "src_spp": {"th": "SPP ในนิคมอุตสาหกรรม", "en": "SPP in industrial estate", "zh": "工业园区内 SPP"},
    "src_self": {"th": "ผลิตได้เอง", "en": "Self-generated", "zh": "自发电"},
    "self_mw": {"th": "ปริมาณที่ผลิตได้เอง", "en": "Self-generated capacity", "zh": "自发电量"},
    "self_method": {"th": "วิธีที่ใช้ผลิต (Example Solar Rooftop, etc)", "en": "Generation method (e.g. Solar Rooftop)", "zh": "发电方式（如屋顶光伏）"},
    "src_other": {"th": "อื่นๆ (โปรดระบุ)", "en": "Others (please specify)", "zh": "其他（请注明）"},
    "s42_head": {"th": "4.2 ปริมาณการใช้ความเย็น / Chiller demand", "en": "4.2 Chiller Demand", "zh": "4.2 制冷需求 / Chiller demand"},
    "c_profile": {"th": "Weekly/Monthly Load Profile", "en": "Weekly/Monthly Load Profile", "zh": "每周/每月负荷曲线"},
    "c_avg": {"th": "Average (RT/hr)", "en": "Average (RT/hr)", "zh": "平均 Average (RT/hr)"},
    "c_base": {"th": "Base Load (RT/hr)", "en": "Base Load (RT/hr)", "zh": "基础负荷 Base Load (RT/hr)"},
    "c_no": {"th": "Chiller No.{n} (RT/hr)", "en": "Chiller No.{n} (RT/hr)", "zh": "制冷机 {n} Chiller No.{n} (RT/hr)"},
    "c_type": {"th": "Type", "en": "Type", "zh": "类型 / Type"},
    "c_cop": {"th": "COP", "en": "COP", "zh": "COP"},
    # ---------- section 5 : policy ----------
    "s5_title": {
        "th": "5. นโยบาย Compliance & Sanctions ของบริษัทฯ",
        "en": "5. Company Compliance & Sanctions Policy",
        "zh": "5. 公司合规与制裁政策（Compliance & Sanctions）",
    },
    "policy_html": {
        "th": """<p>บริษัท ปตท. จำหน่ายก๊าซธรรมชาติ จำกัด (&ldquo;บริษัทฯ&rdquo;) ขอแจ้งให้ท่านทราบว่า บริษัทฯ ดำเนินธุรกิจภายใต้กรอบกฎหมายและมาตรฐานสากลด้าน Compliance อย่างเคร่งครัด รายละเอียดดังนี้</p>
<p><strong>&bull; มาตรการคว่ำบาตรระหว่างประเทศ (International Sanctions)</strong><br>บริษัทฯ ปฏิบัติตามมาตรการคว่ำบาตรระหว่างประเทศอย่างเคร่งครัด และไม่ดำเนินธุรกิจกับบุคคล นิติบุคคล หรือประเทศที่อยู่ภายใต้มาตรการของ:</p>
<ul><li>United Nations (UN)</li><li>United States OFAC</li><li>European Union (EU)</li><li>United Kingdom (UK)</li></ul>
<p><strong>&bull; การป้องกันการฟอกเงินและการสนับสนุนทางการเงินแก่การก่อการร้าย (AML/CFT)</strong><br>บริษัทฯ มีนโยบายไม่รับ ไม่สนับสนุน และไม่มีส่วนเกี่ยวข้องกับ:</p>
<ul><li>การฟอกเงิน (Money Laundering)</li><li>การสนับสนุนทางการเงินแก่การก่อการร้าย (Terrorism Financing)</li><li>ธุรกรรมหรือกิจกรรมทางการค้าที่ผิดกฎหมาย</li></ul>
<p><strong>&bull; การตรวจสอบข้อมูลลูกค้า (KYC / Sanctions Screening)</strong><br>เพื่อให้เป็นไปตามกฎหมายและมาตรฐานสากล บริษัทฯ ขอสงวนสิทธิ์ในการดำเนินการตรวจสอบ KYC, Compliance และ Sanctions Screening สำหรับลูกค้าทุกรายตามความเหมาะสม</p>
<p><strong>&bull; การแจ้งเปลี่ยนแปลงข้อมูล</strong><br>หากมีการเปลี่ยนแปลงข้อมูลที่มีนัยสำคัญ บริษัทฯ ขอความร่วมมือให้ท่านแจ้งให้ทราบโดยเร็ว ได้แก่:</p>
<ul><li>โครงสร้างผู้ถือหุ้น</li><li>ผู้มีอำนาจลงนาม</li><li>สถานะทางกฎหมาย</li><li>สถานะด้านมาตรการคว่ำบาตร</li></ul>
<p><strong>&bull; สิทธิ์ของบริษัทฯ</strong><br>บริษัทฯ ขอสงวนสิทธิ์ในการระงับการดำเนินการหรือการให้บริการ หากตรวจพบประเด็นที่เกี่ยวข้องกับ Compliance หรือ Sanctions โดยไม่ถือเป็นการผิดสัญญา</p>""",
        "en": """<p>PTT Natural Gas Distribution Co., Ltd. (&ldquo;the Company&rdquo;) would like to inform you that the Company strictly conducts its business under applicable laws and international Compliance standards, as detailed below:</p>
<p><strong>&bull; International Sanctions</strong><br>The Company strictly complies with international sanctions and does not conduct business with individuals, juristic persons, or countries subject to the measures of:</p>
<ul><li>United Nations (UN)</li><li>United States OFAC</li><li>European Union (EU)</li><li>United Kingdom (UK)</li></ul>
<p><strong>&bull; Anti-Money Laundering / Counter-Terrorism Financing (AML/CFT)</strong><br>The Company's policy is not to accept, support, or be involved in:</p>
<ul><li>Money Laundering</li><li>Terrorism Financing</li><li>Illegal transactions or trading activities</li></ul>
<p><strong>&bull; KYC / Sanctions Screening</strong><br>To comply with laws and international standards, the Company reserves the right to conduct KYC, Compliance and Sanctions Screening on all customers as appropriate.</p>
<p><strong>&bull; Notification of Changes</strong><br>If there is any significant change in your information, please notify the Company promptly, including:</p>
<ul><li>Shareholder structure</li><li>Authorized signatories</li><li>Legal status</li><li>Sanctions status</li></ul>
<p><strong>&bull; The Company's Rights</strong><br>The Company reserves the right to suspend operations or services if any issue related to Compliance or Sanctions is found, without this being deemed a breach of contract.</p>""",
        "zh": """<p>PTT天然气配送有限公司（&ldquo;本公司&rdquo;）谨此告知，本公司严格遵守相关法律法规及国际合规（Compliance）标准开展业务，详情如下：</p>
<p><strong>&bull; 国际制裁（International Sanctions）</strong><br>本公司严格遵守国际制裁措施，不与受以下机构制裁的个人、法人或国家开展业务：</p>
<ul><li>联合国 (UN)</li><li>美国 OFAC</li><li>欧盟 (EU)</li><li>英国 (UK)</li></ul>
<p><strong>&bull; 反洗钱及反恐怖融资（AML/CFT）</strong><br>本公司的政策为不接受、不支持且不参与：</p>
<ul><li>洗钱 (Money Laundering)</li><li>恐怖主义融资 (Terrorism Financing)</li><li>非法交易或商业活动</li></ul>
<p><strong>&bull; 客户尽职调查（KYC / Sanctions Screening）</strong><br>为遵守法律及国际标准，本公司保留对所有客户酌情进行 KYC、合规及制裁筛查的权利。</p>
<p><strong>&bull; 信息变更通知</strong><br>如有重大信息变更，请及时告知本公司，包括：</p>
<ul><li>股东结构</li><li>授权签字人</li><li>法律地位</li><li>制裁状态</li></ul>
<p><strong>&bull; 本公司的权利</strong><br>如发现涉及合规或制裁的问题，本公司保留暂停相关操作或服务的权利，且不视为违约。</p>""",
    },
    "consent_text": {
        "th": "ข้าพเจ้าในนามของบริษัทได้รับทราบและเข้าใจนโยบาย Compliance & Sanctions ของบริษัท ปตท. จำหน่ายก๊าซธรรมชาติ จำกัด และยินยอมให้บริษัทฯ ดำเนินการตามที่ระบุข้างต้นทุกประการ",
        "en": "I, on behalf of the company, acknowledge and understand the Compliance & Sanctions policy of PTT Natural Gas Distribution Co., Ltd., and consent to the Company proceeding as stated above.",
        "zh": "本人谨代表公司确认已知悉并理解PTT天然气配送有限公司的合规与制裁政策，并同意本公司按上述内容执行。",
    },
    "pdpa_name": {"th": "ชื่อผู้ยืนยัน / Name", "en": "Name of confirmer", "zh": "确认人姓名 / Name"},
    "pdpa_name_ph": {"th": "หากเว้นว่างจะใช้ชื่อผู้ติดต่อ", "en": "If blank, the contact person's name is used", "zh": "留空则使用联系人姓名"},
    "pdpa_title": {"th": "ตำแหน่ง / Title", "en": "Title / Position", "zh": "职位 / Title"},
    "submit": {"th": "ส่งแบบสอบถาม / Submit", "en": "Submit", "zh": "提交问卷 / Submit"},
    "pdpa_footer": {
        "th": "&ldquo;บริษัทฯ จะเก็บรวบรวม ใช้ หรือเปิดเผยข้อมูลของท่านเพื่อการประสานงานที่เกี่ยวข้องกับการดำเนินธุรกิจของบริษัท และ/หรือเพื่อดำเนินการเรื่องการอนุมัติคำขอซื้อสินค้าและหรือใช้บริการ และ/หรือเพื่อดำเนินการตามกระบวนการภายในต่าง ๆ ของบริษัทเท่านั้น โดยท่านสามารถศึกษารายละเอียดเพิ่มเติมที่เกี่ยวข้องกับการประมวลผลข้อมูลส่วนบุคคลและการคุ้มครองข้อมูลส่วนบุคคลของบริษัทได้ที่ &ldquo;แบบแจ้งเกี่ยวกับข้อมูลส่วนบุคคล (Privacy Notice)&rdquo; ในเว็บไซต์ของบริษัท www.pttngd.co.th&rdquo;",
        "en": "&ldquo;The Company will collect, use, or disclose your information solely for coordination related to the Company's business operations, and/or for processing product/service requests, and/or for the Company's internal processes. For more details on personal data processing and protection, please see the &ldquo;Privacy Notice&rdquo; on the Company's website www.pttngd.co.th&rdquo;",
        "zh": "&ldquo;本公司收集、使用或披露您的信息，仅用于与本公司业务运营相关的协调工作、处理产品购买和/或服务申请，以及本公司内部流程。有关个人数据处理与保护的详情，请参阅本公司网站 www.pttngd.co.th 上的《隐私声明》（Privacy Notice）。&rdquo;",
    },
    # ---------- thanks page ----------
    "th_title": {"th": "ขอบคุณสำหรับข้อมูลของท่าน", "en": "Thank you for your information", "zh": "感谢您提供的信息"},
    "th_sub": {"th": "Thank you — your questionnaire has been submitted.", "en": "Your questionnaire has been submitted.", "zh": "您的问卷已成功提交。"},
    "th_msg": {
        "th": "บริษัทฯ ได้รับแบบสอบถามความต้องการใช้พลังงานของท่านเรียบร้อยแล้ว",
        "en": "The Company has received your energy consumption questionnaire.",
        "zh": "本公司已收到您的能源需求调查问卷。",
    },
    "th_ref": {"th": "หมายเลขอ้างอิง / Reference No.", "en": "Reference No.", "zh": "参考编号 / Reference No."},
    "th_contact": {
        "th": "เจ้าหน้าที่จะติดต่อกลับโดยเร็วที่สุด / Our staff will contact you shortly.",
        "en": "Our staff will contact you shortly.",
        "zh": "我们的工作人员将尽快与您联系。",
    },
    "th_again": {"th": "กรอกแบบสอบถามใหม่อีกครั้ง", "en": "Fill in a new questionnaire", "zh": "再次填写问卷"},
    "th_eta": {
        "th": "วิศวกร PNGD จะติดต่อกลับภายใน 3 วันทำการ",
        "en": "A PNGD engineer will contact you within 3 business days",
        "zh": "PNGD工程师将在3个工作日内与您联系",
    },

    # ---------- wizard chrome ----------
    "brand_short": {"th": "PTT NGD", "en": "PTT NGD", "zh": "PTT NGD"},
    "brand_tagline": {
        "th": "NATURAL GAS DISTRIBUTION",
        "en": "NATURAL GAS DISTRIBUTION",
        "zh": "天然气配送",
    },
    "welcome_kicker": {
        "th": "แบบสอบถามความต้องการใช้พลังงานของโรงงาน",
        "en": "Factories' Energy Consumption Questionnaire",
        "zh": "工厂能源需求调查问卷",
    },
    "welcome_time_chip": {
        "th": "ใช้เวลาเพียง ~5 นาที · 6 ขั้นตอน",
        "en": "Takes about ~5 minutes · 6 steps",
        "zh": "仅需约5分钟 · 共6个步骤",
    },
    "welcome_b1_title": {"th": "ออกแบบให้ตรงโรงงานของท่าน", "en": "Tailored to your plant", "zh": "为您的工厂量身定制"},
    "welcome_b1_desc": {
        "th": "วิศวกร PNGD ใช้คำตอบนี้ประเมินระบบก๊าซและต้นทุนที่เหมาะสมที่สุด",
        "en": "PNGD engineers use your answers to design the right gas system and cost estimate.",
        "zh": "PNGD工程师将根据您的回答评估最合适的供气系统与成本。",
    },
    "welcome_b2_title": {"th": "กรอกค้างไว้ได้ ไม่หาย", "en": "Save your progress", "zh": "可保存草稿，不会丢失"},
    "welcome_b2_desc": {
        "th": "ระบบบันทึกอัตโนมัติในเครื่องของท่าน กลับมากรอกต่อจากเดิมได้ทุกเมื่อ",
        "en": "Your answers are auto-saved on this device — come back anytime to continue.",
        "zh": "系统会自动在本设备保存草稿，您可以随时回来继续填写。",
    },
    "welcome_b3_title": {"th": "ข้อมูลปลอดภัย", "en": "Your data is protected", "zh": "信息安全有保障"},
    "welcome_b3_desc": {
        "th": "คุ้มครองตามนโยบาย PDPA และใช้เพื่อการเสนอบริการเท่านั้น",
        "en": "Protected under our PDPA policy and used only to prepare your service proposal.",
        "zh": "依据PDPA政策予以保护，仅用于为您准备服务方案。",
    },
    "start_btn": {"th": "เริ่มกรอกแบบสอบถาม", "en": "Start the questionnaire", "zh": "开始填写问卷"},

    "step_name_1": {"th": "ข้อมูลบริษัท", "en": "Company info", "zh": "公司信息"},
    "step_name_2": {"th": "เชื้อเพลิงปัจจุบัน", "en": "Current fuel", "zh": "当前燃料"},
    "step_name_3": {"th": "แผนใช้ก๊าซ", "en": "Gas plan", "zh": "用气计划"},
    "step_name_4": {"th": "ไฟฟ้า & ความเย็น", "en": "Electricity & chiller", "zh": "电力与制冷"},
    "step_name_5": {"th": "การยินยอม", "en": "Consent", "zh": "同意条款"},
    "step_name_6": {"th": "ตรวจทาน & ส่ง", "en": "Review & submit", "zh": "核对并提交"},

    "cheer_1": {"th": "เริ่มกันเลย!", "en": "Let's get started!", "zh": "开始吧！"},
    "cheer_2": {"th": "", "en": "", "zh": ""},
    "cheer_3": {"th": "ครึ่งทางแล้ว!", "en": "Halfway there!", "zh": "已完成一半！"},
    "cheer_4": {"th": "อีกนิดเดียว!", "en": "Almost done!", "zh": "快好了！"},
    "cheer_5": {"th": "ขั้นสุดท้ายก่อนสรุป", "en": "Last step before review", "zh": "最后一步，即将完成"},
    "cheer_6": {"th": "เสร็จแล้ว!", "en": "All set!", "zh": "全部完成！"},

    "step_of": {"th": "ขั้นที่ {n}/6", "en": "Step {n}/6", "zh": "第{n}/6步"},
    "btn_back": {"th": "ย้อนกลับ", "en": "Back", "zh": "上一步"},
    "btn_next": {"th": "ถัดไป", "en": "Next", "zh": "下一步"},
    "btn_confirm_send": {"th": "ยืนยันและส่ง", "en": "Confirm & Submit", "zh": "确认并提交"},
    "autosave_text": {"th": "บันทึกอัตโนมัติแล้ว", "en": "Auto-saved", "zh": "已自动保存"},

    "copy_all_months": {"th": "⤓ ใช้ค่านี้กับทั้ง 12 เดือน", "en": "⤓ Copy to all 12 months", "zh": "⤓ 应用到全部12个月"},
    "copy_all_hint": {"th": "แล้วค่อยแก้เดือนที่ต่าง", "en": "You can still edit any month after", "zh": "之后仍可单独修改各月份"},

    "add_machine_btn": {"th": "＋ เพิ่มเครื่องจักร", "en": "＋ Add another machine", "zh": "＋ 添加设备"},

    "err_company_required": {
        "th": "กรุณากรอกชื่อบริษัทก่อนไปต่อ",
        "en": "Please enter your company name to continue",
        "zh": "请先填写公司名称再继续",
    },
    "err_consent_required": {
        "th": "กรุณาติ๊กยอมรับนโยบายก่อนไปต่อ",
        "en": "Please accept the policy to continue",
        "zh": "请先勾选同意政策再继续",
    },

    "review_title": {"th": "ตรวจทานคำตอบของท่าน", "en": "Review your answers", "zh": "核对您的答案"},
    "review_hint": {
        "th": "กด \"แก้ไข\" เพื่อกลับไปแก้ขั้นนั้นได้ทันที",
        "en": "Tap \"Edit\" to jump back and change any step",
        "zh": "点击“编辑”即可返回修改对应步骤",
    },
    "review_edit": {"th": "แก้ไข", "en": "Edit", "zh": "编辑"},
    "review_empty": {"th": "ยังไม่ได้กรอก", "en": "Not filled in", "zh": "尚未填写"},
    "review_card_company": {"th": "บริษัท", "en": "Company", "zh": "公司"},
    "review_card_fuel": {"th": "เชื้อเพลิงปัจจุบัน", "en": "Current fuel", "zh": "当前燃料"},
    "review_card_gasplan": {"th": "แผนใช้ก๊าซ", "en": "Gas plan", "zh": "用气计划"},
    "review_card_elec": {"th": "ไฟฟ้า", "en": "Electricity", "zh": "电力"},
    "review_card_compliance": {"th": "Compliance & Sanctions", "en": "Compliance & Sanctions", "zh": "合规与制裁"},
    "review_consent_yes": {"th": "ยินยอมแล้ว", "en": "Consent given", "zh": "已同意"},
    "review_consent_no": {"th": "ยังไม่ได้ยินยอม", "en": "Not yet accepted", "zh": "尚未同意"},
}


def make_t(lang):
    def t(key):
        entry = TEXTS.get(key)
        if not entry:
            return key
        return entry.get(lang) or entry["th"]
    return t


# label maps the wizard's JS review step needs to translate raw field values
# (e.g. "fuel_oil") into on-screen text, keyed by the same value the form posts.
REVIEW_KEY_MAP = {
    "fuel_type": {"fuel_oil": "opt_fuel_oil", "lpg": "opt_lpg", "diesel": "opt_diesel",
                  "natural_gas": "opt_ng", "other": "opt_other"},
    "unit": {"liter": "opt_liter", "kg": "opt_kg", "mmbtu": "opt_mmbtu", "other": "opt_other"},
    "purpose": {"steam": "p_steam", "drying": "p_drying", "melting": "p_melting", "other": "p_other"},
}


def review_i18n(lang):
    t = make_t(lang)
    out = {}
    for group, mapping in REVIEW_KEY_MAP.items():
        out[group] = {k: t(v) for k, v in mapping.items()}
    out["elec_source"] = {"pea": "PEA", "mea": "MEA", "spp": t("src_spp"),
                           "self": t("src_self"), "other": t("src_other")}
    return out
