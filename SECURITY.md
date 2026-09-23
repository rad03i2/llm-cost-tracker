# Security Policy / سياسة الأمان

## Supported version
Security fixes target the latest version on `main`.

## Reporting
Please report suspected vulnerabilities privately through GitHub's available private security-reporting mechanism when enabled. Do not publish credentials, private prompts, or usage ledgers in an issue. If private reporting is unavailable, open a minimal issue asking for a private contact path without disclosing exploit details.

## Security model
LLM Cost Tracker performs local arithmetic and local file I/O only. It does not contact model providers, execute ledger content, load `.env`, or require credentials. Ledger files may still contain operational metadata; protect them with normal filesystem access controls and avoid sensitive labels.

## سياسة الأمان
الأداة تعمل محليًا ولا تحتاج مفاتيح API ولا تنفذ محتوى السجل. تعامل مع ملفات السجل كبيانات تشغيلية قد تكون حساسة، ولا تنشر أسرارًا أو prompts خاصة في البلاغات العامة.
