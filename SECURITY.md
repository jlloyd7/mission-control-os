# Security Policy

## Safe-by-default posture

Mission Control OS is an experimental agentic workflow platform. It ships with
**mock / read-only defaults**. Do not enable write tools, deploy tools, shell
tools, customer-data access, or external communication tools without first
reviewing and configuring approval gates, audit logging, RBAC, and secret
management.

## Core safety principles

1. Default to read-only.
2. Default to mock tools in development.
3. Every side effect must be auditable.
4. High-risk actions require human approval.
5. Agents never receive secrets directly.
6. Tool access is allowlisted per agent.
7. Memory writes can be reviewed.
8. Prompt-injection warnings are surfaced in the run timeline.
9. Dangerous tools are disabled by default.
10. The open-source build must be safe out of the box.

## Secret handling

- Never log API keys, and never render secrets in traces.
- Use environment variables locally; use a secret manager in production.
- Redact provider request headers and tool credentials.

## Reporting a vulnerability

This is an early-stage project. Please open a private security advisory or
contact the maintainers rather than filing a public issue for anything that
could expose users to risk.
