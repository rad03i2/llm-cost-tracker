# LLM Cost Tracker

A small, local-first Python CLI and library for estimating LLM token costs, recording usage in an append-only JSONL ledger, summarizing spend by model, and checking a budget.

> **Pricing note:** provider prices change frequently. The built-in `example-*` models are intentionally illustrative, not claims about any provider's current pricing. For billing decisions, pass your provider's current input/output prices explicitly.

## English

### Why this exists
LLM experiments can become difficult to budget when usage is scattered across scripts. LLM Cost Tracker provides a provider-neutral calculation and ledger layer that stays on your machine and works in shell scripts and Python programs.

### Features
- Decimal-based USD calculations to avoid binary floating-point surprises.
- Input/output token prices expressed per one million tokens.
- Custom model pricing on every estimate or record operation.
- Append-only UTF-8 JSONL ledger with labels and UTC timestamps.
- Aggregate totals and per-model summaries.
- Budget status: spend, remaining amount, percentage, and exceeded flag.
- Human-readable and JSON CLI output.
- Python API and `python -m llm_cost_tracker` support.
- No network calls, API keys, telemetry, or provider SDK required.

### Preview
```console
$ llm-cost estimate --model my-model --input-tokens 1000000 --output-tokens 500000 --input-price 2 --output-price 8
my-model: 1000000 input + 500000 output = $6.000000
```

### Requirements & installation
Requires Python 3.10+.

```bash
git clone https://github.com/rad03i2/llm-cost-tracker.git
cd llm-cost-tracker
python -m pip install -e .
```

For development:
```bash
python -m pip install -e ".[dev]"
```

### Usage
Estimate with explicit current pricing:
```bash
llm-cost estimate --model my-model --input-tokens 12000 --output-tokens 3000 --input-price 1.50 --output-price 6.00
```

Record usage:
```bash
llm-cost record --model my-model --input-tokens 12000 --output-tokens 3000 --input-price 1.50 --output-price 6.00 --ledger usage.jsonl --label nightly-job
```

Summarize and evaluate a USD budget:
```bash
llm-cost summary --ledger usage.jsonl --budget 25 --json
```

List illustrative built-in models:
```bash
llm-cost models
```

### Python API
```python
from decimal import Decimal
from llm_cost_tracker import Price, estimate_cost

price = Price(Decimal("1.50"), Decimal("6.00"))
print(estimate_cost(12_000, 3_000, price))
```

### Configuration
There is no environment configuration and no `.env` file. Pass prices explicitly when accuracy matters. The default ledger is `llm-usage.jsonl`; override it with `--ledger`.

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
CI runs these checks plus CLI smoke tests on Python 3.10, 3.12 and 3.13 across Linux, Windows and macOS.

### Security & privacy
All processing is local. The tool never contacts an LLM provider and does not read API keys. Ledger labels are user-provided text, so do not put secrets or sensitive prompt contents in them. Treat ledger files as potentially sensitive operational records and protect them accordingly.

### Limitations
- The tool **does not count tokens from raw text**; supply token counts reported by your tokenizer/provider.
- It does not fetch live pricing. Built-in prices are illustrative placeholders by design.
- It tracks estimated token cost only, not taxes, discounts, cached-token pricing, batch discounts, tool fees, image/audio units, or provider-specific billing rules.
- JSONL writes are append-only but not a transactional multi-process database; coordinate concurrent writers when needed.

### Optional roadmap
Optional future work may include pluggable provider price catalogs and CSV export, provided pricing provenance remains explicit.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Please include tests for behavior changes and never commit credentials or real private usage data.

### License
MIT — see [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**LLM Cost Tracker** أداة Python محلية لحساب التكلفة التقديرية لاستهلاك نماذج اللغة اعتمادًا على عدد رموز الإدخال والإخراج، وتسجيل الاستخدام في ملف JSONL، وتلخيص الإنفاق حسب النموذج، ومقارنته بميزانية محددة.

> **ملاحظة الأسعار:** أسعار المزودين تتغير باستمرار. النماذج المدمجة المسماة `example-*` أمثلة توضيحية فقط ولا تمثل أسعار أي مزود حاليًا. استخدم أسعار مزودك الحالية صراحةً عند الحاجة إلى دقة مالية.

### لماذا المشروع؟
عند استخدام عدة سكربتات أو نماذج يصبح تتبع المصروف صعبًا. يوفر المشروع طبقة محايدة عن المزود للحساب والتسجيل، تعمل محليًا ويمكن استخدامها من الطرفية أو Python.

### الميزات
- حسابات مالية باستخدام `Decimal`.
- أسعار منفصلة للإدخال والإخراج لكل مليون رمز.
- أسعار مخصصة لأي نموذج.
- سجل JSONL محلي بترميز UTF-8 مع وقت UTC ووسم اختياري.
- إجماليات وتقارير حسب النموذج.
- فحص الميزانية والمبلغ المتبقي ونسبة الاستهلاك وحالة التجاوز.
- إخراج نصي أو JSON.
- Python API وتشغيل عبر `python -m llm_cost_tracker`.
- بلا اتصالات شبكة أو مفاتيح API أو telemetry.

### التثبيت والمتطلبات
يتطلب Python 3.10 أو أحدث:
```bash
git clone https://github.com/rad03i2/llm-cost-tracker.git
cd llm-cost-tracker
python -m pip install -e .
```
وللتطوير والاختبارات:
```bash
python -m pip install -e ".[dev]"
```

### الاستخدام
حساب تكلفة بأسعار صريحة:
```bash
llm-cost estimate --model my-model --input-tokens 12000 --output-tokens 3000 --input-price 1.50 --output-price 6.00
```
تسجيل العملية:
```bash
llm-cost record --model my-model --input-tokens 12000 --output-tokens 3000 --input-price 1.50 --output-price 6.00 --ledger usage.jsonl --label nightly-job
```
التلخيص وفحص ميزانية بالدولار:
```bash
llm-cost summary --ledger usage.jsonl --budget 25 --json
```

### Python API
```python
from decimal import Decimal
from llm_cost_tracker import Price, estimate_cost
price = Price(Decimal("1.50"), Decimal("6.00"))
print(estimate_cost(12_000, 3_000, price))
```

### الإعداد
لا يحتاج المشروع إلى متغيرات بيئة أو ملف `.env`. السجل الافتراضي هو `llm-usage.jsonl` ويمكن تغييره عبر `--ledger`. عند أهمية الدقة استخدم أسعار المزود الحالية يدويًا.

### بنية المشروع
المحرك والـCLI داخل `src/llm_cost_tracker/`، والاختبارات داخل `tests/`، وCI داخل `.github/workflows/`، وبيانات الحزمة في `pyproject.toml`.

### الاختبارات
```bash
python -m pytest -q
python -m compileall -q src
```
ويشغل CI الاختبارات وفحص CLI على Python 3.10 و3.12 و3.13 في Linux وWindows وmacOS.

### الأمان والخصوصية
كل المعالجة محلية ولا تتصل الأداة بمزودي النماذج ولا تقرأ مفاتيح API. لا تضع أسرارًا أو نصوص prompts حساسة داخل الوسوم، واحمِ ملفات السجل لأنها قد تكشف معلومات تشغيلية.

### القيود
- لا تحسب الأداة الرموز من النص الخام؛ يجب تمرير أعداد الرموز من tokenizer أو المزود.
- لا تجلب الأسعار المباشرة، والأسعار المدمجة أمثلة فقط.
- لا تحسب الضرائب والخصومات وتسعير cache أو batch أو الصور والصوت أو الرسوم الخاصة بالمزود.
- JSONL ليس قاعدة بيانات معاملات للكتابة المتزامنة من عمليات متعددة.

### خارطة طريق اختيارية
يمكن مستقبلًا إضافة كتالوجات أسعار قابلة للتركيب وتصدير CSV مع الحفاظ على وضوح مصدر الأسعار.

### المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md). أضف اختبارات لأي تغيير سلوكي ولا ترفع بيانات اعتماد أو سجلات استخدام خاصة.

### الترخيص
MIT — راجع [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
