# README Post-Install Verification Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** README에 설치 완료 후 `playwright-cli` 실행 확인과 스킬 호출 확인 절차를 추가한다.

**Architecture:** 기존 설치 순서는 유지하고, 설치 확인 이후에 별도 검증 섹션을 추가한다. 검증은 `playwright-cli` 명령 실행과 Codex 프롬프트 예시 두 축으로 구성한다.

**Tech Stack:** Markdown, Codex skills, playwright-cli

---

### Task 1: Add verification section to README

**Files:**
- Create: `docs/plans/2026-04-06-readme-post-install-verification-design.md`
- Create: `docs/plans/2026-04-06-readme-post-install-verification.md`
- Modify: `README.md`

- [ ] Step 1: Add a post-install verification section after the install check block
- [ ] Step 2: Include a minimal `playwright-cli` smoke test using `open`, `goto`, `snapshot`, and `close`
- [ ] Step 3: Add example Codex prompts that explicitly invoke `$gated-plan-execution`, `$qa-workflow-expert`, and `$playwright-cli`
- [ ] Step 4: Review the README for ordering and clarity
- [ ] Step 5: Commit and push the updated documentation
