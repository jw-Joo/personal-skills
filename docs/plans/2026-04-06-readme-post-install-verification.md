# README Post-Install Verification Implementation Plan

> **For Codex:** If explicit approval between steps is needed, use the planning workflow from the Matt Pocock skills installation instead of a vendored local `gated-plan-execution` skill.

**Goal:** README에 설치 완료 후 `playwright-cli` 실행 확인, 로컬 스킬 호출 확인, Matt Pocock skills 설정 확인 절차를 추가한다.

**Architecture:** 기존 설치 순서는 유지하되, `gated-plan-execution` 로컬 스킬 대신 Matt Pocock skills 설치 지침을 추가한다. 검증은 `playwright-cli` 명령 실행, 로컬 Codex 스킬 프롬프트 예시, Matt Pocock skills 설정 확인으로 구성한다.

**Tech Stack:** Markdown, Codex skills, playwright-cli

---

### Task 1: Add verification section to README

**Files:**
- Create: `docs/plans/2026-04-06-readme-post-install-verification-design.md`
- Create: `docs/plans/2026-04-06-readme-post-install-verification.md`
- Modify: `README.md`

- [ ] Step 1: Add a post-install verification section after the install check block
- [ ] Step 2: Include a minimal `playwright-cli` smoke test using `open`, `goto`, `snapshot`, and `close`
- [ ] Step 3: Add example Codex prompts that explicitly invoke `$qa-workflow-expert`, `$playwright-cli`, `$api-pf-release-notes`, and `$tdd-implementation`
- [ ] Step 4: Review the README for ordering and clarity
- [ ] Step 5: Commit and push the updated documentation
