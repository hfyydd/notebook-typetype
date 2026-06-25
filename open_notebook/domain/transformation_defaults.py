from __future__ import annotations

from typing import Any


SUPPORTED_TRANSFORMATION_LOCALES = (
    "en-US",
    "en-SG",
    "zh-CN",
    "zh-SG",
    "zh-TW",
    "vi-VN",
    "pt-BR",
    "ja-JP",
    "ko-KR",
    "hi-IN",
    "id-ID",
    "th-TH",
    "ar-SA",
    "fa-IR",
    "he-IL",
    "ms-MY",
    "nl-NL",
    "sv-SE",
    "nb-NO",
    "da-DK",
    "fi-FI",
    "el-GR",
    "cs-CZ",
    "hu-HU",
    "ro-RO",
    "uk-UA",
    "it-IT",
    "fr-FR",
    "ru-RU",
    "bn-IN",
    "ca-ES",
    "es-ES",
    "de-DE",
    "pl-PL",
    "tr-TR",
)

LOCALE_FALLBACKS = {
    "en-SG": "en-US",
    "zh-SG": "zh-CN",
}


def _localized(
    name: str,
    title: str,
    description: str,
    prompt: str | None = None,
) -> dict[str, str]:
    payload = {
        "name": name,
        "title": title,
        "description": description,
    }
    if prompt is not None:
        payload["prompt"] = prompt
    return payload


ANALYZE_PAPER_PROMPT_EN = """# IDENTITY and PURPOSE

You are an insightful and analytical reader of academic papers, extracting the key components, significance, and broader implications. Your focus is to uncover the core contributions, practical applications, methodological strengths or weaknesses, and any surprising findings. You are especially attuned to the clarity of arguments, the relevance to existing literature, and potential impacts on both the specific field and broader contexts.

# STEPS

1. READ AND UNDERSTAND THE PAPER: Thoroughly read the paper, identifying its main focus, arguments, methods, results, and conclusions.
2. IDENTIFY CORE ELEMENTS:
   - Purpose: What is the main goal or research question?
   - Contribution: What new knowledge or innovation does this paper bring to the field?
   - Methods: What methods are used, and are they novel or particularly effective?
   - Key Findings: What are the most critical results, and why do they matter?
   - Limitations: Are there any notable limitations or areas for further research?
3. SYNTHESIZE THE MAIN POINTS:
   - Extract the key elements and organize them into insightful observations.
   - Highlight the broader impact and potential applications.
   - Note any aspects that challenge established views or introduce new questions.

# OUTPUT INSTRUCTIONS

- Output the sections PURPOSE, CONTRIBUTION, KEY FINDINGS, IMPLICATIONS, and LIMITATIONS.
- PURPOSE should be 1-2 sentences.
- CONTRIBUTION, KEY FINDINGS, and IMPLICATIONS should each contain 2-3 bullet points.
- LIMITATIONS should contain 1-2 bullet points.
- Each bullet point should be 15-20 words.
- Avoid warnings, disclaimers, or personal opinions."""

ANALYZE_PAPER_PROMPT_ZH_CN = """# 身份与目标

你是一位善于阅读学术论文的分析助手，需要提炼论文的核心组成、重要性与更广泛影响。你的重点是识别核心贡献、实际应用、方法优劣以及任何令人意外的发现，同时关注论证是否清晰、与既有研究的关系，以及对所在领域和更广泛场景的潜在影响。

# 步骤

1. 通读并理解论文，找出研究主题、论点、方法、结果与结论。
2. 识别核心要素：
   - 目的：论文的主要目标或研究问题是什么？
   - 贡献：论文为该领域带来了哪些新的知识或创新？
   - 方法：采用了哪些方法？它们是否新颖或特别有效？
   - 关键发现：最重要的结果是什么？为什么重要？
   - 局限：有哪些值得注意的局限或后续研究方向？
3. 综合主要内容：
   - 将关键信息整理为有洞察力的观察。
   - 强调更广泛的影响和潜在应用。
   - 指出任何挑战既有观点或引出新问题的部分。

# 输出要求

- 输出 PURPOSE、CONTRIBUTION、KEY FINDINGS、IMPLICATIONS、LIMITATIONS 五个部分。
- PURPOSE 用 1-2 句话概述。
- CONTRIBUTION、KEY FINDINGS、IMPLICATIONS 各写 2-3 条项目符号。
- LIMITATIONS 写 1-2 条项目符号。
- 每条项目符号控制在 15-20 个词左右。
- 不要输出警告、免责声明或个人意见。"""

ANALYZE_PAPER_PROMPT_ZH_TW = """# 身分與目標

你是一位善於閱讀學術論文的分析助手，需要提煉論文的核心組成、重要性與更廣泛影響。你的重點是辨識核心貢獻、實際應用、方法優劣以及任何令人意外的發現，同時關注論證是否清晰、與既有研究的關係，以及對所在領域和更廣泛情境的潛在影響。

# 步驟

1. 通讀並理解論文，找出研究主題、論點、方法、結果與結論。
2. 辨識核心要素：
   - 目的：論文的主要目標或研究問題是什麼？
   - 貢獻：論文為該領域帶來了哪些新的知識或創新？
   - 方法：採用了哪些方法？它們是否新穎或特別有效？
   - 關鍵發現：最重要的結果是什麼？為什麼重要？
   - 限制：有哪些值得注意的限制或後續研究方向？
3. 綜合主要內容：
   - 將關鍵資訊整理為有洞察力的觀察。
   - 強調更廣泛的影響和潛在應用。
   - 指出任何挑戰既有觀點或引出新問題的部分。

# 輸出要求

- 輸出 PURPOSE、CONTRIBUTION、KEY FINDINGS、IMPLICATIONS、LIMITATIONS 五個部分。
- PURPOSE 用 1-2 句話概述。
- CONTRIBUTION、KEY FINDINGS、IMPLICATIONS 各寫 2-3 條項目符號。
- LIMITATIONS 寫 1-2 條項目符號。
- 每條項目符號控制在 15-20 個詞左右。
- 不要輸出警告、免責聲明或個人意見。"""

ANALYZE_PAPER_PROMPT_VI = """# VAI TRO VA MUC TIEU

Ban la tro ly phan tich bai bao hoc thuat. Nhiem vu cua ban la rut ra cac thanh phan cot loi, y nghia va tac dong rong hon cua bai bao. Hay tap trung vao dong gop chinh, gia tri ung dung, diem manh va diem yeu ve phuong phap, cung nhu cac ket qua dang chu y.

# CAC BUOC

1. Doc ky bai bao va hieu muc tieu, lap luan, phuong phap, ket qua va ket luan.
2. Xac dinh cac yeu to cot loi:
   - Muc tieu: Cau hoi nghien cuu hoac muc tieu chinh la gi?
   - Dong gop: Bai bao bo sung dieu gi moi cho linh vuc?
   - Phuong phap: Da dung nhung phuong phap nao? Chung co moi hay dac biet hieu qua khong?
   - Ket qua chinh: Phat hien quan trong nhat la gi va vi sao quan trong?
   - Gioi han: Co gioi han nao dang chu y hoac huong nghien cuu tiep theo nao khong?
3. Tong hop cac diem chinh:
   - To chuc thong tin thanh cac nhan xet co chieu sau.
   - Nhan manh tac dong rong hon va kha nang ung dung.
   - Chi ra nhung diem thach thuc quan diem hien co hoac mo ra cau hoi moi.

# YEU CAU DAU RA

- Tra ve cac muc PURPOSE, CONTRIBUTION, KEY FINDINGS, IMPLICATIONS va LIMITATIONS.
- PURPOSE dai 1-2 cau.
- CONTRIBUTION, KEY FINDINGS va IMPLICATIONS moi muc co 2-3 gạch đầu dòng.
- LIMITATIONS co 1-2 gạch đầu dòng.
- Moi gạch đầu dòng nen khoang 15-20 tu.
- Khong them canh bao, mien tru trach nhiem hay y kien ca nhan."""

KEY_INSIGHTS_PROMPT_EN = """# IDENTITY and PURPOSE

You extract surprising, powerful, and interesting insights from text content. You create concise bullet points that capture the most important ideas and then elevate them into higher-level insights.

# STEPS

1. Extract 20 to 50 notable ideas from the input in a section called IDEAS. Use bullet points of about 15 words each.
2. From those ideas, extract the strongest and most insightful ones into a section called INSIGHTS.

# OUTPUT INSTRUCTIONS

- Output the INSIGHTS section only.
- Include 10 to 25 bullet points.
- Each bullet should be about 15 words.
- Use bullet lists, not numbered lists.
- Avoid warnings or notes."""

KEY_INSIGHTS_PROMPT_ZH_CN = """# 身份与目标

你需要从文本中提炼出令人惊讶、有力量且有启发性的洞见。先捕捉重要想法，再将它们提升为更高层次的洞见。

# 步骤

1. 从输入中提取 20 到 50 个值得关注的想法，放在 IDEAS 部分，每条约 15 个词。
2. 再从这些想法中提取最有力量、最有洞察力的内容，整理到 INSIGHTS 部分。

# 输出要求

- 只输出 INSIGHTS 部分。
- 包含 10 到 25 条项目符号。
- 每条项目符号约 15 个词。
- 使用项目符号，不要使用编号列表。
- 不要添加警告或备注。"""

KEY_INSIGHTS_PROMPT_ZH_TW = """# 身分與目標

你需要從文本中提煉出令人驚訝、有力量且有啟發性的洞見。先捕捉重要想法，再將它們提升為更高層次的洞見。

# 步驟

1. 從輸入中提取 20 到 50 個值得關注的想法，放在 IDEAS 部分，每條約 15 個詞。
2. 再從這些想法中提取最有力量、最有洞察力的內容，整理到 INSIGHTS 部分。

# 輸出要求

- 只輸出 INSIGHTS 部分。
- 包含 10 到 25 條項目符號。
- 每條項目符號約 15 個詞。
- 使用項目符號，不要使用編號列表。
- 不要添加警告或備註。"""

KEY_INSIGHTS_PROMPT_VI = """# VAI TRO VA MUC TIEU

Ban can rut ra nhung insight bat ngo, manh me va thu vi tu van ban. Dau tien hay thu thap y tuong quan trong, sau do nang cap chung thanh nhung insight co muc do tong quat cao hon.

# CAC BUOC

1. Trich xuat 20 den 50 y tuong dang chu y vao muc IDEAS, moi gạch đầu dòng khoảng 15 tu.
2. Tu nhung y tuong do, chon ra cac insight manh nhat va sau sac nhat dua vao muc INSIGHTS.

# YEU CAU DAU RA

- Chi tra ve muc INSIGHTS.
- Gom 10 den 25 gạch đầu dòng.
- Moi gạch đầu dòng khoảng 15 tu.
- Dung danh sach gạch đầu dòng, khong dung danh sach danh so.
- Khong them canh bao hoac ghi chu."""

DENSE_SUMMARY_PROMPT_EN = """# MISSION

You are writing a dense summary for another language model. Capture the input as a distilled list of succinct statements, concepts, associations, and metaphors while preserving key meaning.

# INSTRUCTIONS

- Compress the content aggressively without losing important ideas.
- Use complete sentences.
- Prefer conceptual density over rhetorical flourish.
- Write for machine understanding, not for presentation polish."""

DENSE_SUMMARY_PROMPT_ZH_CN = """# 任务

你要为另一个语言模型写一份高密度摘要。请把输入压缩成精炼的陈述、概念、关联和隐喻，同时保留最关键的含义。

# 要求

- 在不丢失重要信息的前提下尽可能高密度压缩内容。
- 使用完整句子。
- 优先保留概念密度，而不是修辞表达。
- 这份内容是为了机器理解，不是为了表面上的华丽呈现。"""

DENSE_SUMMARY_PROMPT_ZH_TW = """# 任務

你要為另一個語言模型寫一份高密度摘要。請把輸入壓縮成精煉的陳述、概念、關聯和隱喻，同時保留最關鍵的含義。

# 要求

- 在不遺失重要資訊的前提下盡可能高密度壓縮內容。
- 使用完整句子。
- 優先保留概念密度，而不是修辭表達。
- 這份內容是為了機器理解，不是為了表面上的華麗呈現。"""

DENSE_SUMMARY_PROMPT_VI = """# NHIEM VU

Ban can viet mot ban tom tat co mat do thong tin cao cho mot mo hinh ngon ngu khac. Hay nen noi dung thanh nhung cau ngan gon, cac khai niem, lien tuong va an du quan trong nhat, nhung van giu duoc y nghia cot loi.

# YEU CAU

- Nen chat noi dung toi da ma van giu lai cac y chinh.
- Dung cau day du.
- Uu tien mat do khai niem hon la cach dien dat hoa my.
- Viet de may co the hieu, khong phai de trinh bay dep mat."""

REFLECTIONS_PROMPT_EN = """# IDENTITY and PURPOSE

You extract deep and meaningful reflections from text content. Your reflections should surface broader implications, challenge assumptions, and invite further thinking.

# STEPS

- Extract 3 to 5 profound ideas into a section called REFLECTIONS.
- Each item should explore deeper implications, human meaning, or transformative perspective.

# OUTPUT INSTRUCTIONS

- Output the REFLECTIONS section only.
- Use bullet points of 20-25 words.
- Each bullet can be a reflective question or a profound statement.
- Avoid warnings or notes."""

REFLECTIONS_PROMPT_ZH_CN = """# 身份与目标

你需要从文本中提炼深刻而有意义的反思。你的输出应揭示更深层的含义、挑战既有假设，并引导继续思考。

# 步骤

- 提取 3 到 5 个深刻想法，整理到 REFLECTIONS 部分。
- 每一条都应探索更深层的影响、人类意义或具有转变性的视角。

# 输出要求

- 只输出 REFLECTIONS 部分。
- 使用 20-25 个词左右的项目符号。
- 每条可以是引发思考的问题，也可以是深刻的陈述。
- 不要添加警告或备注。"""

REFLECTIONS_PROMPT_ZH_TW = """# 身分與目標

你需要從文本中提煉深刻而有意義的反思。你的輸出應揭示更深層的含義、挑戰既有假設，並引導持續思考。

# 步驟

- 提取 3 到 5 個深刻想法，整理到 REFLECTIONS 部分。
- 每一條都應探索更深層的影響、人類意義或具有轉變性的視角。

# 輸出要求

- 只輸出 REFLECTIONS 部分。
- 使用 20-25 個詞左右的項目符號。
- 每條可以是引發思考的問題，也可以是深刻的陳述。
- 不要添加警告或備註。"""

REFLECTIONS_PROMPT_VI = """# VAI TRO VA MUC TIEU

Ban can rut ra nhung suy ngam sau sac va co y nghia tu van ban. Dau ra can chi ra tac dong sau hon, thach thuc cac gia dinh hien co va khuyen khich suy nghi tiep.

# CAC BUOC

- Trich xuat 3 den 5 y tuong sau sac vao muc REFLECTIONS.
- Moi muc nen kham pha y nghia sau hon, gia tri nhan van hoac mot goc nhin co tinh chuyen hoa.

# YEU CAU DAU RA

- Chi tra ve muc REFLECTIONS.
- Dung gạch đầu dòng dài khoảng 20-25 tu.
- Moi mục co the la cau hoi goi mo suy nghi hoac mot nhan dinh sau sac.
- Khong them canh bao hoac ghi chu."""

TABLE_OF_CONTENTS_PROMPT_EN = """# SYSTEM ROLE

You read documents and provide a table of contents that helps users understand what the document covers.

# TASK

Analyze the content and create a table of contents that:
- captures the main topics in order,
- notes the major transitions,
- gives a short description for each part."""

TABLE_OF_CONTENTS_PROMPT_ZH_CN = """# 系统角色

你是一名内容分析助手，需要阅读文档并生成目录，帮助用户更快理解文档包含哪些内容。

# 任务

分析内容并生成目录，要求：
- 按顺序覆盖主要主题，
- 标出关键转折，
- 为每一部分提供简短说明。"""

TABLE_OF_CONTENTS_PROMPT_ZH_TW = """# 系統角色

你是一名內容分析助手，需要閱讀文件並產生目錄，幫助使用者更快理解文件包含哪些內容。

# 任務

分析內容並產生目錄，要求：
- 依順序涵蓋主要主題，
- 標出關鍵轉折，
- 為每一部分提供簡短說明。"""

TABLE_OF_CONTENTS_PROMPT_VI = """# VAI TRO HE THONG

Ban la tro ly phan tich noi dung, doc tai lieu va tao muc luc de giup nguoi dung nhanh chóng hieu tai lieu bao gom nhung gi.

# NHIEM VU

Phan tich noi dung va tao muc luc:
- bao quat cac chu de chinh theo dung thu tu,
- chi ra cac chuyen doan quan trong,
- them mo ta ngan cho tung phan."""

SIMPLE_SUMMARY_PROMPT_EN = """# SYSTEM ROLE

You are a summarization assistant that creates compact, information-rich summaries.

# TASK

Analyze the content and produce a short summary that:
- captures the core concepts and important information,
- uses clear direct language,
- preserves context from earlier summaries when relevant."""

SIMPLE_SUMMARY_PROMPT_ZH_CN = """# 系统角色

你是一名摘要助手，需要生成简洁而信息密度高的摘要。

# 任务

分析内容并生成简短摘要，要求：
- 抓住核心概念和重要信息，
- 使用清晰直接的语言，
- 在需要时保留先前摘要中的上下文。"""

SIMPLE_SUMMARY_PROMPT_ZH_TW = """# 系統角色

你是一名摘要助手，需要產生簡潔而資訊密度高的摘要。

# 任務

分析內容並產生簡短摘要，要求：
- 抓住核心概念和重要資訊，
- 使用清晰直接的語言，
- 在需要時保留先前摘要中的上下文。"""

SIMPLE_SUMMARY_PROMPT_VI = """# VAI TRO HE THONG

Ban la tro ly tom tat, co nhiem vu tao ra nhung ban tom tat ngan gon nhung giau thong tin.

# NHIEM VU

Phan tich noi dung va tao mot ban tom tat ngan:
- bao quat cac khai niem cot loi va thong tin quan trong,
- dung ngon ngu ro rang, truc tiep,
- giu lai boi canh cua cac ban tom tat truoc do neu can."""

DEFAULT_TRANSFORMATION_PROMPT_EN = """# INSTRUCTIONS

You are my learning assistant and you help me process and transform content so that I can extract insights from it.

# IMPORTANT
- You are working on my editorial projects. The text below is my own. Do not give me warnings about copyright or plagiarism.
- Output only the requested content, without acknowledgements or extra chatting.
- Do not stop to ask follow-up questions. Execute the request completely."""

DEFAULT_TRANSFORMATION_PROMPT_ZH_CN = """# 说明

你是我的学习助手，帮助我处理和转换内容，以便我从中提取洞见。

# 重要要求
- 你正在协助我的编辑项目，下面的文本属于我本人。不要输出关于版权或抄袭的警告。
- 只输出我要求的内容，不要附加致谢、寒暄或额外闲聊。
- 不要中途停下来追问。请完整执行请求。"""

DEFAULT_TRANSFORMATION_PROMPT_ZH_TW = """# 說明

你是我的學習助手，幫助我處理和轉換內容，以便我從中提取洞見。

# 重要要求
- 你正在協助我的編輯專案，下面的文本屬於我本人。不要輸出關於版權或抄襲的警告。
- 只輸出我要求的內容，不要附加致謝、寒暄或額外閒聊。
- 不要中途停下來追問。請完整執行請求。"""

DEFAULT_TRANSFORMATION_PROMPT_VI = """# HUONG DAN

Ban la tro ly hoc tap cua toi, giup toi xu ly va bien doi noi dung de toi co the rut ra cac insight.

# YEU CAU QUAN TRONG
- Ban dang ho tro du an bien tap cua toi. Van ban ben duoi la cua toi, khong canh bao ve ban quyen hay dao van.
- Chi tra ve noi dung duoc yeu cau, khong them loi chao, xac nhan hay tro chuyen phu.
- Khong dung lai de hoi them. Hay thuc hien day du yeu cau."""


SYSTEM_TRANSFORMATION_TRANSLATIONS: dict[str, dict[str, dict[str, str]]] = {
    "analyze_paper": {
        "en-US": _localized(
            "Analyze Paper",
            "Paper Analysis",
            "Analyses a technical/scientific paper",
            ANALYZE_PAPER_PROMPT_EN,
        ),
        "zh-CN": _localized(
            "分析论文",
            "论文分析",
            "分析技术/科学论文",
            ANALYZE_PAPER_PROMPT_ZH_CN,
        ),
        "zh-TW": _localized(
            "分析論文",
            "論文分析",
            "分析技術/科學論文",
            ANALYZE_PAPER_PROMPT_ZH_TW,
        ),
        "vi-VN": _localized(
            "Phan tich bai bao",
            "Phan tich bai bao",
            "Phan tich mot bai bao ky thuat/khoa hoc",
            ANALYZE_PAPER_PROMPT_VI,
        ),
        "pt-BR": _localized("Analisar artigo", "Análise do artigo", "Analisa um artigo técnico/científico"),
        "ja-JP": _localized("論文を分析", "論文分析", "技術・科学論文を分析します"),
        "it-IT": _localized("Analizza articolo", "Analisi dell'articolo", "Analizza un articolo tecnico/scientifico"),
        "fr-FR": _localized("Analyser l'article", "Analyse de l'article", "Analyse un article technique/scientifique"),
        "ru-RU": _localized("Проанализировать статью", "Анализ статьи", "Анализирует техническую/научную статью"),
        "bn-IN": _localized("প্রবন্ধ বিশ্লেষণ", "প্রবন্ধ বিশ্লেষণ", "একটি প্রযুক্তিগত/বৈজ্ঞানিক প্রবন্ধ বিশ্লেষণ করে"),
        "ca-ES": _localized("Analitza el document", "Anàlisi del document", "Analitza un article tècnic/científic"),
        "es-ES": _localized("Analizar artículo", "Análisis del artículo", "Analiza un artículo técnico/científico"),
        "de-DE": _localized("Artikel analysieren", "Artikelanalyse", "Analysiert einen technischen/wissenschaftlichen Artikel"),
        "pl-PL": _localized("Analizuj artykuł", "Analiza artykułu", "Analizuje artykuł techniczny/naukowy"),
        "tr-TR": _localized("Makaleyi analiz et", "Makale analizi", "Teknik/bilimsel bir makaleyi analiz eder"),
        "ko-KR": _localized(
            "논문 분석",
            "논문 분석",
            "기술/과학 논문을 분석합니다",
        ),
        "hi-IN": _localized(
            "पेपर विश्लेषण",
            "पेपर विश्लेषण",
            "तकनीकी/वैज्ञानिक पेपर का विश्लेषण करता है",
        ),
        "id-ID": _localized(
            "Analisis Makalah",
            "Analisis Makalah",
            "Menganalisis makalah teknis/ilmiah",
        ),
        "th-TH": _localized(
            "วิเคราะห์งานวิจัย",
            "วิเคราะห์งานวิจัย",
            "วิเคราะห์งานวิจัยทางเทคนิค/วิทยาศาสตร์",
        ),
        "ar-SA": _localized(
            "تحليل الورقة",
            "تحليل الورقة",
            "تحلل ورقة تقنية/علمية",
        ),
        "fa-IR": _localized(
            "تحلیل مقاله",
            "تحلیل مقاله",
            "یک مقاله فنی/علمی را تحلیل می‌کند",
        ),
        "he-IL": _localized(
            "ניתוח מאמר",
            "ניתוח מאמר",
            "מנתח מאמר טכני/מדעי",
        ),
        "ms-MY": _localized(
            "Analisis Kertas",
            "Analisis Kertas",
            "Menganalisis kertas kerja teknikal/saintifik",
        ),
        "nl-NL": _localized(
            "Artikel analyseren",
            "Artikelanalyse",
            "Analyseert een technisch/wetenschappelijk artikel",
        ),
        "sv-SE": _localized(
            "Analysera uppsats",
            "Uppsatsanalys",
            "Analyserar en teknisk/vetenskaplig uppsats",
        ),
        "nb-NO": _localized(
            "Analyser artikkel",
            "Artikkelanalyse",
            "Analyserer en teknisk/vitenskapelig artikkel",
        ),
        "da-DK": _localized(
            "Analysér artikel",
            "Artikelanalyse",
            "Analyserer en teknisk/videnskabelig artikel",
        ),
        "fi-FI": _localized(
            "Analysoi artikkeli",
            "Artikkelin analyysi",
            "Analysoi teknisen/tieteellisen artikkelin",
        ),
        "el-GR": _localized(
            "Ανάλυση άρθρου",
            "Ανάλυση άρθρου",
            "Αναλύει ένα τεχνικό/επιστημονικό άρθρο",
        ),
        "cs-CZ": _localized(
            "Analyzovat článek",
            "Analýza článku",
            "Analyzuje technický/vědecký článek",
        ),
        "hu-HU": _localized(
            "Cikk elemzése",
            "Cikk elemzése",
            "Technikai/tudományos cikket elemez",
        ),
        "ro-RO": _localized(
            "Analizează articol",
            "Analiza articolului",
            "Analizează un articol tehnic/științific",
        ),
        "uk-UA": _localized(
            "Аналіз статті",
            "Аналіз статті",
            "Аналізує технічну/наукову статтю",
        ),
    },
    "key_insights": {
        "en-US": _localized(
            "Key Insights",
            "Key Insights",
            "Extracts important insights and actionable items",
            KEY_INSIGHTS_PROMPT_EN,
        ),
        "zh-CN": _localized(
            "关键洞见",
            "关键洞见",
            "提取重要洞见和可执行要点",
            KEY_INSIGHTS_PROMPT_ZH_CN,
        ),
        "zh-TW": _localized(
            "關鍵洞見",
            "關鍵洞見",
            "提取重要洞見和可執行要點",
            KEY_INSIGHTS_PROMPT_ZH_TW,
        ),
        "vi-VN": _localized(
            "Insight chinh",
            "Insight chinh",
            "Trich xuat cac insight quan trong va cac hanh dong co the thuc hien",
            KEY_INSIGHTS_PROMPT_VI,
        ),
        "pt-BR": _localized("Principais insights", "Principais insights", "Extrai insights importantes e ações úteis"),
        "ja-JP": _localized("主要な洞察", "主要な洞察", "重要な洞察と実行項目を抽出します"),
        "it-IT": _localized("Insight chiave", "Insight chiave", "Estrae insight importanti e azioni utili"),
        "fr-FR": _localized("Insights clés", "Insights clés", "Extrait des insights importants et des actions utiles"),
        "ru-RU": _localized("Ключевые инсайты", "Ключевые инсайты", "Извлекает важные инсайты и практические шаги"),
        "bn-IN": _localized("মূল অন্তর্দৃষ্টি", "মূল অন্তর্দৃষ্টি", "গুরুত্বপূর্ণ অন্তর্দৃষ্টি ও করণীয় বের করে"),
        "ca-ES": _localized("Idees clau", "Idees clau", "Extreu idees importants i accions útils"),
        "es-ES": _localized("Ideas clave", "Ideas clave", "Extrae insights importantes y acciones útiles"),
        "de-DE": _localized("Wichtige Erkenntnisse", "Wichtige Erkenntnisse", "Extrahiert wichtige Erkenntnisse und umsetzbare Punkte"),
        "pl-PL": _localized("Kluczowe wnioski", "Kluczowe wnioski", "Wyodrębnia ważne wnioski i możliwe działania"),
        "tr-TR": _localized("Temel içgörüler", "Temel içgörüler", "Önemli içgörüleri ve uygulanabilir maddeleri çıkarır"),
        "ko-KR": _localized(
            "핵심 인사이트",
            "핵심 인사이트",
            "중요한 인사이트와 실행 가능한 항목을 추출합니다",
        ),
        "hi-IN": _localized(
            "मुख्य अंतर्दृष्टि",
            "मुख्य अंतर्दृष्टि",
            "महत्वपूर्ण अंतर्दृष्टि और कार्रवाई योग्य आइटम निकालता है",
        ),
        "id-ID": _localized(
            "Wawasan Utama",
            "Wawasan Utama",
            "Mengekstrak wawasan penting dan item yang dapat ditindaklanjuti",
        ),
        "th-TH": _localized(
            "ข้อมูลเชิงลึกหลัก",
            "ข้อมูลเชิงลึกหลัก",
            "ดึงข้อมูลเชิงลึกที่สำคัญและรายการที่นำไปปฏิบัติได้",
        ),
        "ar-SA": _localized(
            "الرؤى الرئيسية",
            "الرؤى الرئيسية",
            "تستخرج رؤى مهمة وعناصر قابلة للتنفيذ",
        ),
        "fa-IR": _localized(
            "بینش‌های کلیدی",
            "بینش‌های کلیدی",
            "بینش‌های مهم و اقدامات عملی را استخراج می‌کند",
        ),
        "he-IL": _localized(
            "תובנות מרכזיות",
            "תובנות מרכזיות",
            "מחלץ תובנות חשובות ופריטים שניתנים ליישום",
        ),
        "ms-MY": _localized(
            "Wawasan Utama",
            "Wawasan Utama",
            "Mengekstrak wawasan penting dan item yang boleh dilakukan",
        ),
        "nl-NL": _localized(
            "Belangrijke inzichten",
            "Belangrijke inzichten",
            "Extraheert belangrijke inzichten en actiepunten",
        ),
        "sv-SE": _localized(
            "Nyckelinsikter",
            "Nyckelinsikter",
            "Extraherar viktiga insikter och åtgärdsbara punkter",
        ),
        "nb-NO": _localized(
            "Nøkkelinnsikter",
            "Nøkkelinnsikter",
            "Trekker ut viktige innsikter og handlingbare punkter",
        ),
        "da-DK": _localized(
            "Nøgleindsigter",
            "Nøgleindsigter",
            "Udtrækker vigtige indsigter og handlingsbare punkter",
        ),
        "fi-FI": _localized(
            "Keskeiset oivallukset",
            "Keskeiset oivallukset",
            "Poimii tärkeitä oivalluksia ja toimenpiteitä",
        ),
        "el-GR": _localized(
            "Βασικές γνώσεις",
            "Βασικές γνώσεις",
            "Εξάγει σημαντικές γνώσεις και εφαρμόσιμα στοιχεία",
        ),
        "cs-CZ": _localized(
            "Klíčové postřehy",
            "Klíčové postřehy",
            "Extrahuje důležité postřehy a akční body",
        ),
        "hu-HU": _localized(
            "Fő betekintések",
            "Fő betekintések",
            "Fontos betekintéseket és cselekvési pontokat emel ki",
        ),
        "ro-RO": _localized(
            "Informații cheie",
            "Informații cheie",
            "Extrage informații importante și elemente acționabile",
        ),
        "uk-UA": _localized(
            "Ключові інсайти",
            "Ключові інсайти",
            "Витягує важливі інсайти та практичні пункти",
        ),
    },
    "dense_summary": {
        "en-US": _localized(
            "Dense Summary",
            "Dense Summary",
            "Creates a rich, deep summary of the content",
            DENSE_SUMMARY_PROMPT_EN,
        ),
        "zh-CN": _localized(
            "高密度摘要",
            "高密度摘要",
            "生成内容丰富、层次深入的摘要",
            DENSE_SUMMARY_PROMPT_ZH_CN,
        ),
        "zh-TW": _localized(
            "高密度摘要",
            "高密度摘要",
            "產生內容豐富、層次深入的摘要",
            DENSE_SUMMARY_PROMPT_ZH_TW,
        ),
        "vi-VN": _localized(
            "Tom tat dac",
            "Tom tat dac",
            "Tao ban tom tat sau va giau thong tin",
            DENSE_SUMMARY_PROMPT_VI,
        ),
        "pt-BR": _localized("Resumo denso", "Resumo denso", "Cria um resumo rico e profundo do conteúdo"),
        "ja-JP": _localized("高密度要約", "高密度要約", "内容を豊かで深い要約にします"),
        "it-IT": _localized("Sintesi densa", "Sintesi densa", "Crea una sintesi ricca e approfondita del contenuto"),
        "fr-FR": _localized("Résumé dense", "Résumé dense", "Crée un résumé riche et approfondi du contenu"),
        "ru-RU": _localized("Плотное резюме", "Плотное резюме", "Создает насыщенное и глубокое резюме содержания"),
        "bn-IN": _localized("ঘন সারসংক্ষেপ", "ঘন সারসংক্ষেপ", "বিষয়বস্তুর সমৃদ্ধ ও গভীর সারসংক্ষেপ তৈরি করে"),
        "ca-ES": _localized("Resum dens", "Resum dens", "Crea un resum ric i profund del contingut"),
        "es-ES": _localized("Resumen denso", "Resumen denso", "Crea un resumen rico y profundo del contenido"),
        "de-DE": _localized("Dichte Zusammenfassung", "Dichte Zusammenfassung", "Erstellt eine gehaltvolle und tiefgehende Zusammenfassung"),
        "pl-PL": _localized("Gęste podsumowanie", "Gęste podsumowanie", "Tworzy bogate i pogłębione podsumowanie treści"),
        "tr-TR": _localized("Yoğun özet", "Yoğun özet", "İçeriğin zengin ve derin bir özetini oluşturur"),
        "ko-KR": _localized(
            "고밀도 요약",
            "고밀도 요약",
            "콘텐츠의 풍부하고 심층적인 요약을 만듭니다",
        ),
        "hi-IN": _localized(
            "घना सारांश",
            "घना सारांश",
            "सामग्री का समृद्ध, गहन सारांश बनाता है",
        ),
        "id-ID": _localized(
            "Ringkasan Padat",
            "Ringkasan Padat",
            "Membuat ringkasan yang kaya dan mendalam",
        ),
        "th-TH": _localized(
            "สรุปเข้มข้น",
            "สรุปเข้มข้น",
            "สร้างบทสรุปที่สมบูรณ์และลึกซึ้งของเนื้อหา",
        ),
        "ar-SA": _localized(
            "ملخص كثيف",
            "ملخص كثيف",
            "ينشئ ملخصًا غنيًا وعميقًا للمحتوى",
        ),
        "fa-IR": _localized(
            "خلاصه متراکم",
            "خلاصه متراکم",
            "خلاصه‌ای غنی و عمیق از محتوا ایجاد می‌کند",
        ),
        "he-IL": _localized(
            "תקציר צפוף",
            "תקציר צפוף",
            "יוצר תקציר עשיר ועמוק של התוכן",
        ),
        "ms-MY": _localized(
            "Ringkasan Padat",
            "Ringkasan Padat",
            "Mewujudkan ringkasan yang kaya dan mendalam",
        ),
        "nl-NL": _localized(
            "Dichte samenvatting",
            "Dichte samenvatting",
            "Maakt een rijke, diepgaande samenvatting",
        ),
        "sv-SE": _localized(
            "Tät sammanfattning",
            "Tät sammanfattning",
            "Skapar en rik, djup sammanfattning av innehållet",
        ),
        "nb-NO": _localized(
            "Tett sammendrag",
            "Tett sammendrag",
            "Lager et rikt og dypt sammendrag av innholdet",
        ),
        "da-DK": _localized(
            "Tæt resumé",
            "Tæt resumé",
            "Skaber et rigt og dybt resumé af indholdet",
        ),
        "fi-FI": _localized(
            "Tiivis yhteenveto",
            "Tiivis yhteenveto",
            "Luo rikkaan ja syvällisen yhteenvedon sisällöstä",
        ),
        "el-GR": _localized(
            "Πυκνή περίληψη",
            "Πυκνή περίληψη",
            "Δημιουργεί μια πλούσια, βαθιά περίληψη του περιεχομένου",
        ),
        "cs-CZ": _localized(
            "Husté shrnutí",
            "Husté shrnutí",
            "Vytvoří bohaté a hluboké shrnutí obsahu",
        ),
        "hu-HU": _localized(
            "Sűrű összefoglaló",
            "Sűrű összefoglaló",
            "Gazdag, mély összefoglalót készít a tartalomból",
        ),
        "ro-RO": _localized(
            "Rezumat dens",
            "Rezumat dens",
            "Creează un rezumat bogat și profund al conținutului",
        ),
        "uk-UA": _localized(
            "Щільний підсумок",
            "Щільний підсумок",
            "Створює насичений і глибокий підсумок вмісту",
        ),
    },
    "reflections": {
        "en-US": _localized(
            "Reflections",
            "Reflection Questions",
            "Generates reflection questions from the document to help explore it further",
            REFLECTIONS_PROMPT_EN,
        ),
        "zh-CN": _localized(
            "延伸反思",
            "反思问题",
            "根据文档生成反思问题，帮助进一步探索内容",
            REFLECTIONS_PROMPT_ZH_CN,
        ),
        "zh-TW": _localized(
            "延伸反思",
            "反思問題",
            "根據文件產生反思問題，幫助進一步探索內容",
            REFLECTIONS_PROMPT_ZH_TW,
        ),
        "vi-VN": _localized(
            "Suy ngam",
            "Cau hoi suy ngam",
            "Tao cac cau hoi suy ngam de giup kham pha tai lieu sau hon",
            REFLECTIONS_PROMPT_VI,
        ),
        "pt-BR": _localized("Reflexões", "Perguntas de reflexão", "Gera perguntas de reflexão para explorar melhor o documento"),
        "ja-JP": _localized("リフレクション", "内省の問い", "文書をさらに探るための内省的な問いを生成します"),
        "it-IT": _localized("Riflessioni", "Domande di riflessione", "Genera domande di riflessione per approfondire il documento"),
        "fr-FR": _localized("Réflexions", "Questions de réflexion", "Génère des questions de réflexion pour approfondir le document"),
        "ru-RU": _localized("Размышления", "Вопросы для размышления", "Создает вопросы для более глубокого осмысления документа"),
        "bn-IN": _localized("ভাবনা", "চিন্তার প্রশ্ন", "নথিটি আরও গভীরভাবে ভাবতে সহায়ক প্রশ্ন তৈরি করে"),
        "ca-ES": _localized("Reflexions", "Preguntes de reflexió", "Genera preguntes de reflexió per aprofundir en el document"),
        "es-ES": _localized("Reflexiones", "Preguntas de reflexión", "Genera preguntas de reflexión para explorar mejor el documento"),
        "de-DE": _localized("Reflexionen", "Reflexionsfragen", "Erzeugt Reflexionsfragen, um das Dokument weiter zu erkunden"),
        "pl-PL": _localized("Refleksje", "Pytania refleksyjne", "Generuje pytania refleksyjne pomagające lepiej zbadać dokument"),
        "tr-TR": _localized("Yansımalar", "Düşünme soruları", "Belgeyi daha derin keşfetmek için düşünme soruları üretir"),
        "ko-KR": _localized(
            "성찰",
            "성찰 질문",
            "문서를 더 깊이 탐구하도록 돕는 성찰 질문을 생성합니다",
        ),
        "hi-IN": _localized(
            "चिंतन",
            "चिंतन प्रश्न",
            "दस्तावेज़ को आगे तलाशने में मदद के लिए चिंतन प्रश्न बनाता है",
        ),
        "id-ID": _localized(
            "Refleksi",
            "Pertanyaan Refleksi",
            "Menghasilkan pertanyaan refleksi untuk mengeksplorasi dokumen lebih lanjut",
        ),
        "th-TH": _localized(
            "การไตร่ตรอง",
            "คำถามไตร่ตรอง",
            "สร้างคำถามไตร่ตรองเพื่อช่วยสำรวจเอกสารเพิ่มเติม",
        ),
        "ar-SA": _localized(
            "التأملات",
            "أسئلة التأمل",
            "تولد أسئلة تأمل من المستند لاستكشافه بشكل أعمق",
        ),
        "fa-IR": _localized(
            "تأملات",
            "سؤالات تأملی",
            "سؤالات تأملی از سند تولید می‌کند تا بیشتر کاوش شود",
        ),
        "he-IL": _localized(
            "הרהורים",
            "שאלות הרהור",
            "מייצר שאלות הרהור מהמסמך כדי לחקור אותו לעומק",
        ),
        "ms-MY": _localized(
            "Refleksi",
            "Soalan Refleksi",
            "Menjana soalan refleksi untuk meneroka dokumen dengan lebih lanjut",
        ),
        "nl-NL": _localized(
            "Reflecties",
            "Reflectievragen",
            "Genereert reflectievragen om het document verder te verkennen",
        ),
        "sv-SE": _localized(
            "Reflektioner",
            "Reflektionsfrågor",
            "Genererar reflektionsfrågor för att utforska dokumentet vidare",
        ),
        "nb-NO": _localized(
            "Refleksjoner",
            "Refleksjonsspørsmål",
            "Genererer refleksjonsspørsmål for å utforske dokumentet videre",
        ),
        "da-DK": _localized(
            "Refleksioner",
            "Refleksionsspørgsmål",
            "Genererer refleksionsspørgsmål til at udforske dokumentet yderligere",
        ),
        "fi-FI": _localized(
            "Heijastukset",
            "Heijastuskysymykset",
            "Tuottaa heijastuskysymyksiä asiakirjan syvempää tutkimista varten",
        ),
        "el-GR": _localized(
            "Στοχασμοί",
            "Ερωτήσεις στοχασμού",
            "Δημιουργεί ερωτήσεις στοχασμού από το έγγραφο",
        ),
        "cs-CZ": _localized(
            "Reflexe",
            "Reflexní otázky",
            "Generuje reflexní otázky pro další zkoumání dokumentu",
        ),
        "hu-HU": _localized(
            "Reflexiók",
            "Reflexiós kérdések",
            "Reflexiós kérdéseket generál a dokumentum további feltárásához",
        ),
        "ro-RO": _localized(
            "Reflecții",
            "Întrebări de reflecție",
            "Generează întrebări de reflecție pentru a explora documentul mai departe",
        ),
        "uk-UA": _localized(
            "Роздуми",
            "Питання для роздумів",
            "Генерує питання для роздумів з документа для подальшого дослідження",
        ),
    },
    "table_of_contents": {
        "en-US": _localized(
            "Table of Contents",
            "Table of Contents",
            "Describes the different topics of the document",
            TABLE_OF_CONTENTS_PROMPT_EN,
        ),
        "zh-CN": _localized(
            "目录",
            "目录",
            "概述文档中的不同主题",
            TABLE_OF_CONTENTS_PROMPT_ZH_CN,
        ),
        "zh-TW": _localized(
            "目錄",
            "目錄",
            "概述文件中的不同主題",
            TABLE_OF_CONTENTS_PROMPT_ZH_TW,
        ),
        "vi-VN": _localized(
            "Muc luc",
            "Muc luc",
            "Mo ta cac chu de khac nhau trong tai lieu",
            TABLE_OF_CONTENTS_PROMPT_VI,
        ),
        "pt-BR": _localized("Sumário", "Sumário", "Descreve os diferentes tópicos do documento"),
        "ja-JP": _localized("目次", "目次", "文書内の各トピックを整理して示します"),
        "it-IT": _localized("Indice", "Indice", "Descrive i diversi argomenti del documento"),
        "fr-FR": _localized("Table des matières", "Table des matières", "Décrit les différents sujets du document"),
        "ru-RU": _localized("Оглавление", "Оглавление", "Описывает различные темы документа"),
        "bn-IN": _localized("সূচিপত্র", "সূচিপত্র", "নথির বিভিন্ন বিষয় বর্ণনা করে"),
        "ca-ES": _localized("Taula de continguts", "Taula de continguts", "Descriu els diferents temes del document"),
        "es-ES": _localized("Tabla de contenido", "Tabla de contenido", "Describe los distintos temas del documento"),
        "de-DE": _localized("Inhaltsverzeichnis", "Inhaltsverzeichnis", "Beschreibt die verschiedenen Themen des Dokuments"),
        "pl-PL": _localized("Spis treści", "Spis treści", "Opisuje różne tematy dokumentu"),
        "tr-TR": _localized("Icindekiler", "Icindekiler", "Belgedeki farkli konulari aciklar"),
        "ko-KR": _localized(
            "목차",
            "목차",
            "문서의 다양한 주제를 설명합니다",
        ),
        "hi-IN": _localized(
            "विषय सूची",
            "विषय सूची",
            "दस्तावेज़ के विभिन्न विषयों का वर्णन करता है",
        ),
        "id-ID": _localized(
            "Daftar Isi",
            "Daftar Isi",
            "Menjelaskan berbagai topik dalam dokumen",
        ),
        "th-TH": _localized(
            "สารบัญ",
            "สารบัญ",
            "อธิบายหัวข้อต่างๆ ของเอกสาร",
        ),
        "ar-SA": _localized(
            "جدول المحتويات",
            "جدول المحتويات",
            "يصف الموضوعات المختلفة للمستند",
        ),
        "fa-IR": _localized(
            "فهرست مطالب",
            "فهرست مطالب",
            "موضوعات مختلف سند را توصیف می‌کند",
        ),
        "he-IL": _localized(
            "תוכן עניינים",
            "תוכן עניינים",
            "מתאר את הנושאים השונים של המסמך",
        ),
        "ms-MY": _localized(
            "Jadual Kandungan",
            "Jadual Kandungan",
            "Menjelaskan pelbagai topik dalam dokumen",
        ),
        "nl-NL": _localized(
            "Inhoudsopgave",
            "Inhoudsopgave",
            "Beschrijft de verschillende onderwerpen van het document",
        ),
        "sv-SE": _localized(
            "Innehållsförteckning",
            "Innehållsförteckning",
            "Beskriver dokumentets olika ämnen",
        ),
        "nb-NO": _localized(
            "Innholdsfortegnelse",
            "Innholdsfortegnelse",
            "Beskriver de ulike emnene i dokumentet",
        ),
        "da-DK": _localized(
            "Indholdsfortegnelse",
            "Indholdsfortegnelse",
            "Beskriver dokumentets forskellige emner",
        ),
        "fi-FI": _localized(
            "Sisällysluettelo",
            "Sisällysluettelo",
            "Kuvaa asiakirjan eri aiheet",
        ),
        "el-GR": _localized(
            "Πίνακας περιεχομένων",
            "Πίνακας περιεχομένων",
            "Περιγράφει τα διάφορα θέματα του εγγράφου",
        ),
        "cs-CZ": _localized(
            "Obsah",
            "Obsah",
            "Popisuje různá témata dokumentu",
        ),
        "hu-HU": _localized(
            "Tartalomjegyzék",
            "Tartalomjegyzék",
            "Leírja a dokumentum különböző témáit",
        ),
        "ro-RO": _localized(
            "Cuprins",
            "Cuprins",
            "Descrie diferitele subiecte ale documentului",
        ),
        "uk-UA": _localized(
            "Зміст",
            "Зміст",
            "Описує різні теми документа",
        ),
    },
    "simple_summary": {
        "en-US": _localized(
            "Simple Summary",
            "Simple Summary",
            "Generates a small summary of the content",
            SIMPLE_SUMMARY_PROMPT_EN,
        ),
        "zh-CN": _localized(
            "简要摘要",
            "简要摘要",
            "生成一段简短的内容摘要",
            SIMPLE_SUMMARY_PROMPT_ZH_CN,
        ),
        "zh-TW": _localized(
            "簡要摘要",
            "簡要摘要",
            "產生一段簡短的內容摘要",
            SIMPLE_SUMMARY_PROMPT_ZH_TW,
        ),
        "vi-VN": _localized(
            "Tom tat ngan",
            "Tom tat ngan",
            "Tao mot ban tom tat ngan cho noi dung",
            SIMPLE_SUMMARY_PROMPT_VI,
        ),
        "pt-BR": _localized("Resumo simples", "Resumo simples", "Gera um pequeno resumo do conteúdo"),
        "ja-JP": _localized("簡易要約", "簡易要約", "内容の短い要約を生成します"),
        "it-IT": _localized("Sintesi breve", "Sintesi breve", "Genera un breve riassunto del contenuto"),
        "fr-FR": _localized("Résumé simple", "Résumé simple", "Génère un court résumé du contenu"),
        "ru-RU": _localized("Краткое резюме", "Краткое резюме", "Создает короткое резюме содержания"),
        "bn-IN": _localized("সংক্ষিপ্ত সারাংশ", "সংক্ষিপ্ত সারাংশ", "বিষয়বস্তুর একটি ছোট সারাংশ তৈরি করে"),
        "ca-ES": _localized("Resum breu", "Resum breu", "Genera un petit resum del contingut"),
        "es-ES": _localized("Resumen breve", "Resumen breve", "Genera un pequeño resumen del contenido"),
        "de-DE": _localized("Kurze Zusammenfassung", "Kurze Zusammenfassung", "Erstellt eine kurze Zusammenfassung des Inhalts"),
        "pl-PL": _localized("Krotkie podsumowanie", "Krotkie podsumowanie", "Generuje krótkie podsumowanie treści"),
        "tr-TR": _localized("Kisa özet", "Kisa özet", "Icerigin kisa bir özetini olusturur"),
        "ko-KR": _localized(
            "간단 요약",
            "간단 요약",
            "콘텐츠의 짧은 요약을 생성합니다",
        ),
        "hi-IN": _localized(
            "सरल सारांश",
            "सरल सारांश",
            "सामग्री का संक्षिप्त सारांश बनाता है",
        ),
        "id-ID": _localized(
            "Ringkasan Sederhana",
            "Ringkasan Sederhana",
            "Menghasilkan ringkasan singkat dari konten",
        ),
        "th-TH": _localized(
            "สรุปอย่างง่าย",
            "สรุปอย่างง่าย",
            "สร้างบทสรุปสั้นๆ ของเนื้อหา",
        ),
        "ar-SA": _localized(
            "ملخص بسيط",
            "ملخص بسيط",
            "ينشئ ملخصًا قصيرًا للمحتوى",
        ),
        "fa-IR": _localized(
            "خلاصه ساده",
            "خلاصه ساده",
            "خلاصه‌ای کوتاه از محتوا تولید می‌کند",
        ),
        "he-IL": _localized(
            "תקציר פשוט",
            "תקציר פשוט",
            "יוצר תקציר קצר של התוכן",
        ),
        "ms-MY": _localized(
            "Ringkasan Mudah",
            "Ringkasan Mudah",
            "Menjana ringkasan pendek bagi kandungan",
        ),
        "nl-NL": _localized(
            "Eenvoudige samenvatting",
            "Eenvoudige samenvatting",
            "Genereert een korte samenvatting van de inhoud",
        ),
        "sv-SE": _localized(
            "Enkel sammanfattning",
            "Enkel sammanfattning",
            "Genererar en kort sammanfattning av innehållet",
        ),
        "nb-NO": _localized(
            "Enkelt sammendrag",
            "Enkelt sammendrag",
            "Genererer et kort sammendrag av innholdet",
        ),
        "da-DK": _localized(
            "Simpelt resumé",
            "Simpelt resumé",
            "Genererer et kort resumé af indholdet",
        ),
        "fi-FI": _localized(
            "Yksinkertainen yhteenveto",
            "Yksinkertainen yhteenveto",
            "Luo lyhyen yhteenvedon sisällöstä",
        ),
        "el-GR": _localized(
            "Απλή περίληψη",
            "Απλή περίληψη",
            "Δημιουργεί μια σύντομη περίληψη του περιεχομένου",
        ),
        "cs-CZ": _localized(
            "Jednoduché shrnutí",
            "Jednoduché shrnutí",
            "Generuje krátké shrnutí obsahu",
        ),
        "hu-HU": _localized(
            "Egyszerű összefoglaló",
            "Egyszerű összefoglaló",
            "Rövid összefoglalót készít a tartalomból",
        ),
        "ro-RO": _localized(
            "Rezumat simplu",
            "Rezumat simplu",
            "Generează un rezumat scurt al conținutului",
        ),
        "uk-UA": _localized(
            "Простий підсумок",
            "Простий підсумок",
            "Створює короткий підсумок вмісту",
        ),
    },
}

DEFAULT_PROMPT_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en-US": {"transformation_instructions": DEFAULT_TRANSFORMATION_PROMPT_EN},
    "zh-CN": {"transformation_instructions": DEFAULT_TRANSFORMATION_PROMPT_ZH_CN},
    "zh-TW": {"transformation_instructions": DEFAULT_TRANSFORMATION_PROMPT_ZH_TW},
    "vi-VN": {"transformation_instructions": DEFAULT_TRANSFORMATION_PROMPT_VI},
}


def _copy_locale_entries(
    payload: dict[str, dict[str, dict[str, str]]],
    from_locale: str,
    to_locale: str,
) -> None:
    for translations in payload.values():
        if from_locale in translations and to_locale not in translations:
            translations[to_locale] = dict(translations[from_locale])


def _copy_default_prompt_locale(from_locale: str, to_locale: str) -> None:
    if from_locale in DEFAULT_PROMPT_TRANSLATIONS and to_locale not in DEFAULT_PROMPT_TRANSLATIONS:
        DEFAULT_PROMPT_TRANSLATIONS[to_locale] = dict(DEFAULT_PROMPT_TRANSLATIONS[from_locale])


_copy_locale_entries(SYSTEM_TRANSFORMATION_TRANSLATIONS, "en-US", "en-SG")
_copy_locale_entries(SYSTEM_TRANSFORMATION_TRANSLATIONS, "zh-CN", "zh-SG")
_copy_default_prompt_locale("en-US", "en-SG")
_copy_default_prompt_locale("zh-CN", "zh-SG")


def get_system_transformation_translations(
    system_key: str | None,
) -> dict[str, dict[str, Any]]:
    if not system_key:
        return {}
    return {
        locale: dict(fields)
        for locale, fields in SYSTEM_TRANSFORMATION_TRANSLATIONS.get(system_key, {}).items()
    }


def get_default_prompt_translations() -> dict[str, dict[str, Any]]:
    return {
        locale: dict(fields) for locale, fields in DEFAULT_PROMPT_TRANSLATIONS.items()
    }
