# tg-reminder-bot — RETIRED (2026-07-17)

A 2023-era prototype: a Telegram bot that sent a daily LLM-generated
"fitness coach" reminder at a user-chosen time (python-telegram-bot +
APScheduler + SQLite + OpenAI).

**Superseded by openclaw (hugocrab)**, which handles scheduled reminders,
follow-ups, and conversation natively. Nothing here is deployed anywhere.

Dependencies were fully bumped & pinned (zero known CVEs) right before
retirement, so this snapshot is healthy if it's ever resurrected:
`TELEGRAM_BOT_TOKEN` + `OPENAI_API_KEY` (+ optional `OPENAI_BASE_URL`,
`LLM_MODEL`) are the only env vars needed.
