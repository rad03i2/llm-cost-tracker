# LLM Cost Tracker

Local-first Python CLI and library for estimating LLM token costs, recording usage in an append-only JSONL ledger, filtering historical usage, exporting CSV reports, summarizing spend by model, and checking budgets.

> **Pricing note:** provider prices change frequently. Built-in `example-*` models are illustrative only. For billing decisions, supply current provider prices explicitly.

## English

### Overview / why it exists
LLM usage is often scattered across scripts and experiments. This project provides a small provider-neutral accounting layer that stays on your machine, uses decimal arithmetic, and works from both shell scripts and Python.

### Key features
- Decimal-based USD calculations with separate input/output prices per million tokens.
- Custom pricing for any model; no provider SDK or API key required.
- Append-only UTF-8 JSONL ledger with labels and ISO-8601 timestamps.
- Strict validation when reading ledger rows, including token counts and timestamps.
- Summaries for requests, input/output tokens, total cost, and per-model cost.
- Exact filtering by model/label and inclusive `--since` / `--until` ISO-8601 ranges.
- UTF-8 CSV export of all or filtered usage.
- Budget status with spend, remaining amount, percentage, and exceeded flag.
- Human-readable or JSON CLI output; reusable Python API.
- No network calls or telemetry.

### Preview
```console
$ llm-cost estimate --model my-model --input-tokens 1000000 --output-tokens 500000 --input-price 2 --output-price 8
my-model: 1000000 input + 500000 output = $6.000000

$ llm-cost summary --ledger usage.jsonl --label production
requests=4 input=52000 output=9000 cost=$0.132000
```

For screenshots, capture the terminal with `estimate`, filtered `summary`, and `export` output; the project is intentionally CLI-first and has no GUI.

### Requirements & installation
Python 3.10+.

```bash
git clone https://github.com/rad03i2/llm-cost-tracker.git
cd llm-cost-tracker
python -m pip install -e .
```

Development install:
```bash
python -m pip install -e ".[dev]"
```

### Usage
Estimate with explicit pricing:
```bash
llm-cost estimate --model my-model --input-tokens 12000 --output-tokens 3000 --input-price 1.50 --output-price 6.00
```

Record usage:
```bash
llm-cost record --model my-model --input-tokens 12000 --output-tokens 3000 --input-price 1.50 --output-price 6.00 --ledger usage.jsonl --label production
```

Summarize a filtered period and check a USD budget:
```bash
llm-cost summary --ledger usage.jsonl --model my-model --label production --since 2026-09-01T00:00:00Z --until 2026-09-30T23:59:59Z --budget 25 --json
```

Export the same kind of filtered selection to CSV:
```bash
llm-cost export --ledger usage.jsonl --label production --since 2026-09-01T00:00:00Z --output september.csv
```

List illustrative built-in models:
```bash
llm-cost models
```

### Python API
```python
from decimal import Decimal
from llm_cost_tracker import Price, estimate_cost, filter_usage, load_usage, summarize

price = Price(Decimal("1.50"), Decimal("6.00"))
print(estimate_cost(12_000, 3_000, price))
rows = filter_usage(load_usage("usage.jsonl"), label="production")
print(summarize(rows))
```

### Configuration
No environment variables or `.env` file are required. The default ledger is `llm-usage.jsonl`; override it with `--ledger`. Filters use exact model/label matching. Time bounds are inclusive and accept ISO-8601 timestamps; timestamps without an offset are interpreted as UTC.

### Project structure
```text
src/llm_cost_tracker/   core engine, public API and CLI
tests/                  unit and CLI tests
.github/workflows/      cross-platform CI
pyproject.toml           package/build metadata
```

### Testing
```bash
python -m pytest -q
python -m compileall -q src
```
CI runs automated checks on supported Python versions and operating systems as configured in `.github/workflows/ci.yml`.

### Security & privacy
All processing is local. The tool never contacts an LLM provider and never reads API keys. Ledger labels and exported CSV files can reveal operational information, so avoid secrets in labels and protect ledger/report files appropriately. CSV export writes data fields through Python's CSV writer, but spreadsheet software may still interpret cells beginning with formula characters; do not use untrusted labels/models as spreadsheet formulas without reviewing the exported file.

### Limitations
- It does **not** tokenize raw text; provide token counts from your tokenizer/provider.
- It does not fetch live pricing; built-in prices are illustrative placeholders.
- It tracks token cost only, not taxes, discounts, cached/batch pricing, tool fees, image/audio units, or provider-specific billing rules.
- JSONL is not a transactional multi-process database; coordinate concurrent writers.
- Filtering scans the ledger in memory and is intended for small-to-medium local ledgers, not warehouse-scale analytics.

### Optional roadmap
Optional future work may include pluggable price catalogs with explicit provenance and a SQLite backend for very large ledgers.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Include tests for behavior changes and never commit credentials or private usage data.

### License
MIT — see [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة ولماذا المشروع؟
**LLM Cost Tracker** أداة Python محلية لحساب التكلفة التقديرية لاستهلاك نماذج اللغة، وتسجيل الاستخدام في سجل JSONL، وتصفية السجل حسب النموذج والوسم والفترة الزمنية، وتصدير CSV، وتلخيص الإنفاق ومقارنته بميزانية. تفيد عندما يكون الاستخدام موزعًا بين سكربتات وتجارب متعددة وتحتاج طبقة حساب محلية ومحايدة عن المزود.

> **ملاحظة الأسعار:** النماذج `example-*` أمثلة توضيحية وليست أسعارًا حالية لأي مزود. مرر أسعار مزودك الحالية صراحةً عند الحاجة إلى دقة مالية.

### الميزات
- حساب مالي باستخدام `Decimal` مع أسعار مستقلة للإدخال والإخراج لكل مليون رمز.
- أسعار مخصصة لأي نموذج دون SDK أو مفتاح API.
- سجل JSONL محلي UTF-8 مع وسوم وأوقات ISO-8601.
- تحقق صارم من صفوف السجل وأعداد الرموز والطوابع الزمنية.
- إجماليات للطلبات والرموز والتكلفة وتقارير حسب النموذج.
- تصفية حسب النموذج والوسم والفترة الزمنية عبر `--since` و`--until`.
- تصدير CSV بترميز UTF-8 لكل السجل أو للنتائج المفلترة.
- فحص الميزانية والمبلغ المتبقي ونسبة الاستهلاك وحالة التجاوز.
- إخراج نصي أو JSON وواجهة Python قابلة لإعادة الاستخدام.
- لا اتصالات شبكة ولا telemetry.

### المعاينة
المشروع مخصص للطرفية ولا يملك واجهة رسومية. يمكن تصوير أوامر `estimate` و`summary` و`export` عند إعداد صور للمستودع.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث:
```bash
git clone https://github.com/rad03i2/llm-cost-tracker.git
cd llm-cost-tracker
python -m pip install -e .
```
وللتطوير:
```bash
python -m pip install -e ".[dev]"
```

### الاستخدام
حساب تكلفة:
```bash
llm-cost estimate --model my-model --input-tokens 12000 --output-tokens 3000 --input-price 1.50 --output-price 6.00
```
تسجيل الاستخدام:
```bash
llm-cost record --model my-model --input-tokens 12000 --output-tokens 3000 --input-price 1.50 --output-price 6.00 --ledger usage.jsonl --label production
```
تلخيص فترة محددة وفحص الميزانية:
```bash
llm-cost summary --ledger usage.jsonl --label production --since 2026-09-01T00:00:00Z --until 2026-09-30T23:59:59Z --budget 25 --json
```
تصدير النتائج المفلترة:
```bash
llm-cost export --ledger usage.jsonl --label production --output report.csv
```

### Python API
```python
from llm_cost_tracker import filter_usage, load_usage, summarize
rows = filter_usage(load_usage("usage.jsonl"), label="production")
print(summarize(rows))
```

### الإعداد
لا يحتاج المشروع إلى متغيرات بيئة أو `.env`. السجل الافتراضي `llm-usage.jsonl` ويمكن تغييره بـ`--ledger`. مطابقة النموذج والوسم تامة، والحدود الزمنية شاملة، والطابع بلا timezone يعامل كـUTC.

### بنية المشروع
المحرك والـCLI داخل `src/llm_cost_tracker/`، والاختبارات داخل `tests/`، وCI داخل `.github/workflows/`، وبيانات الحزمة في `pyproject.toml`.

### الاختبارات
```bash
python -m pytest -q
python -m compileall -q src
```
ويشغل GitHub Actions الفحوص الآلية وفق مصفوفة الإصدارات والأنظمة المحددة في ملف CI.

### الأمان والخصوصية
كل المعالجة محلية ولا تقرأ الأداة مفاتيح API. قد تكشف الوسوم وملفات JSONL وCSV معلومات تشغيلية، لذلك لا تضع أسرارًا فيها واحمِ الملفات الناتجة. كما قد تفسر برامج الجداول بعض الخلايا التي تبدأ بعلامات الصيغ كصيغة؛ راجع البيانات غير الموثوقة قبل فتحها في برنامج جداول.

### القيود
- لا تحسب الرموز من النص الخام؛ يجب تمرير العدد من tokenizer أو المزود.
- لا تجلب أسعارًا مباشرة، والأسعار المدمجة أمثلة فقط.
- لا تحسب الضرائب والخصومات وتسعير cache/batch أو الصور والصوت والرسوم الخاصة بالمزود.
- JSONL ليس قاعدة معاملات للكتابة المتزامنة من عدة عمليات.
- التصفية تقرأ السجل في الذاكرة، لذا هي موجهة للسجلات المحلية الصغيرة والمتوسطة.

### خارطة طريق اختيارية
يمكن مستقبلًا إضافة كتالوجات أسعار ذات مصدر واضح وSQLite للسجلات الكبيرة جدًا.

### المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md)، وأضف اختبارات للتغييرات السلوكية ولا ترفع بيانات اعتماد أو سجلات خاصة.

### الترخيص
MIT — راجع [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
