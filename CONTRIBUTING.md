# Contributing / المساهمة

Thank you for improving LLM Cost Tracker. / شكرًا لمساهمتك في تطوير المشروع.

1. Create a focused branch and keep changes small and reviewable.
2. Install development dependencies with `python -m pip install -e ".[dev]"`.
3. Run `python -m pytest -q` and `python -m compileall -q src`.
4. Add tests for behavior changes and update both README language sections when user-facing behavior changes.
5. Never commit API keys, credentials, private prompts, real private ledgers, or generated build artifacts.

Bug reports should include Python/OS versions, the command used, expected behavior, and sanitized output. Security issues should follow SECURITY.md instead of a public issue.
