## What & why

Briefly describe the change and the motivation.

## Checklist

- [ ] Mock mode still works with no API keys (the vertical slice runs end-to-end)
- [ ] No secrets committed (`.env` stays local; `env.example` has empty values)
- [ ] Real tool execution remains disabled / approval-gated by default
- [ ] Backend: `pytest` passes; new behavior has tests
- [ ] Frontend: `tsc --noEmit` and `next build` pass
- [ ] Migrations added if models changed (`alembic revision --autogenerate`)

## Notes for reviewers

Anything the Sentinel (Fable/Cipher) should scrutinize — risk, blast radius, edge cases.
