# Instructions for Claude

Read `README.md` first. It has three parts:
1. **Price checking from any chat.** Run `scripts/item_report.py "<item>"` (in cloud
   sessions, prefix the command with `WOW_API_KEY=proxy-injected`). Answer with the verdict
   (vendor, or list at about X) and a small table, following the rules of thumb in that section.
   **Horde AH only:** never check the neutral house (`/v1/neutral/...`).
   The API changed on 2026-11-23; if anything looks off, compare with `/openapi.json`.
2. **Gold farming.** The plan, the character level and the docs. Read them; don't redo the
   research. Add measured runs to `docs/farm-log.md`.
3. **General.** API reference, data quirks, security and conventions.

Never commit or print the API key. Commit as `Claude <noreply@anthropic.com>`, SSH-signed, so GitHub
shows the commit as Verified. Keep personal email addresses and names out of commits and docs.
