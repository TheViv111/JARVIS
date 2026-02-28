# Risk Policy v1

## 1. Risk Tiers
- `low`: read-only or reversible local actions.
- `medium`: state-changing but non-destructive local actions.
- `high`: destructive, external communication, payment, system-critical operations.

## 2. Approval Rules
1. Low: auto-run and log.
2. Medium: auto-run with user notification and optional cancel window.
3. High: explicit user approval required.

## 3. Always-High Actions
1. `send_email`
2. `send_message`
3. `delete_file_permanent`
4. `payment_action`
5. `system_critical_change`
6. `driver_or_install_change`

## 4. Biometric Policy
1. High-risk requires trust check.
2. Primary check: voice + face confidence.
3. If threshold unmet: require PIN/passphrase fallback.
4. Liveness checks required for face trust on high-risk action.

## 5. Learn-From-Me Policy
1. First three workflow runs require approval.
2. Sensitive fields are redacted at capture and replay.
3. Unsafe step patterns are blocked unless explicitly re-authorized.

## 6. Clarification Policy
If planner confidence < configured threshold, assistant must ask a clarifying question before execution.

## 7. Retention Policy
1. Raw timeline: 72 hours.
2. Summaries: 90 days.
3. Graph facts/workflows: indefinite with confidence decay.
4. Secrets and sensitive auth values: never persisted.

## 8. Emergency Controls
1. `jarvis emergency stop` halts active task.
2. `jarvis privacy mode` disables mic/cam/screen capture.
3. Emergency commands preempt all normal tasks.

## 9. Audit and Explainability
1. Every action logs: intent, plan step, tool, result, confidence, and policy decision.
2. Every high-risk action logs approval artifact and user decision.
3. Logs must support post-run replay and incident review.
