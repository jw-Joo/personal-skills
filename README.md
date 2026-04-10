# personal-skills

다른 PC에서도 바로 내려받아 쓸 수 있도록 개인용 Codex 스킬 전체 디렉터리를 보관하는 저장소입니다.

현재 이 저장소에는 내가 전역에서 사용 중인 아래 4개 스킬이 보조 파일까지 포함된 형태로 그대로 들어 있습니다.

## 포함된 스킬

* `gated-plan-execution`
* `qa-workflow-expert`
* `playwright-cli`
* `api-pf-release-notes`

## 이 저장소의 목적

* 다른 PC에서 이 저장소만 clone 해도 개인 스킬 4개의 원문을 바로 확보할 수 있게 하기
* `obra/superpowers`를 먼저 설치한 뒤, 필요한 개인 스킬 디렉터리를 추가로 복사해서 쓸 수 있게 하기

## 중요한 점

일부 스킬은 `SKILL.md`만으로 끝나지 않습니다.

* `gated-plan-execution`은 `agents/openai.yaml`을 포함합니다.
* `qa-workflow-expert`는 `agents/openai.yaml`과 `references/output-patterns.md`를 포함합니다.
* `playwright-cli`는 `references/*.md`를 포함합니다.
* `api-pf-release-notes`는 `agents/openai.yaml`, `assets/output_template.md`, `references/*.md`, `scripts/*.py`를 포함합니다.

따라서 `SKILL.md` 파일만 따로 복사하면 불완전할 수 있습니다. 가능하면 항상 스킬 디렉터리 전체를 clone 또는 복사하세요.

## 권장 사용 순서

### 1. 먼저 `obra/superpowers` 설치

`obra/superpowers` 저장소 README는 Codex 설치 방법으로 아래 지시를 먼저 실행하라고 안내합니다.

Source:
* https://github.com/obra/superpowers
* https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md

Codex에게 먼저 이렇게 요청하세요.

```text
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md
```

이 단계는 개인 스킬보다 먼저 끝내는 것을 권장합니다.

### 2. 그 다음 이 저장소 클론

```bash
git clone https://github.com/jw-Joo/personal-skills.git ~/.codex/personal-skills
```

혹은 GitHub에서 ZIP으로 전체 저장소를 내려받은 뒤 `skills/` 디렉터리 전체를 사용해도 됩니다.

### 3. `playwright-cli` 스킬을 쓰기 전에 CLI 먼저 설치

`playwright-cli` 개인 스킬은 `playwright-cli` 명령이 있는 환경을 전제로 합니다.

```bash
npm install -g @playwright/cli@latest
playwright-cli --version
```

### 4. 마지막으로 개인 스킬 4개를 순서대로 복사

아래 예시는 WSL/Linux 기준이며, 심볼릭 링크가 아니라 스킬 디렉터리 전체를 실제로 복사하는 방식입니다.

```bash
mkdir -p ~/.codex/skills
cp -R ~/.codex/personal-skills/skills/gated-plan-execution ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/qa-workflow-expert ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/playwright-cli ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/api-pf-release-notes ~/.codex/skills/
```

Codex에게 한 번에 맡기고 싶다면, 아래처럼 순서가 드러나는 요청문으로 안내하면 됩니다.

```text
1. Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md
2. Clone https://github.com/jw-Joo/personal-skills.git into ~/.codex/personal-skills
3. Install @playwright/cli globally and verify that playwright-cli is available
4. Copy these full skill directories into ~/.codex/skills in order:
   - ~/.codex/personal-skills/skills/gated-plan-execution
   - ~/.codex/personal-skills/skills/qa-workflow-expert
   - ~/.codex/personal-skills/skills/playwright-cli
   - ~/.codex/personal-skills/skills/api-pf-release-notes
5. Restart Codex after installation
```

## 설치 확인

```bash
ls -la ~/.codex/skills/gated-plan-execution
ls -la ~/.codex/skills/qa-workflow-expert
ls -la ~/.codex/skills/playwright-cli
ls -la ~/.codex/skills/api-pf-release-notes
playwright-cli --version
```

필요하면 Codex를 재시작한 뒤, 해당 스킬 이름을 직접 언급해서 불러오거나 관련 작업을 요청해 동작을 확인하세요.

## 설치 후 동작 검증

위 설치 절차를 모두 끝냈다면, 아래 순서로 실제 동작 여부를 확인하세요.

### 1. `playwright-cli` 간단 실행 테스트

```bash
playwright-cli open https://example.com
playwright-cli snapshot
playwright-cli close
```

정상이라면 브라우저가 열리고, `example.com` 페이지 기준의 스냅샷이 생성되어야 합니다.

### 2. Codex에서 스킬 직접 호출 확인

새 Codex 세션에서 아래처럼 각 스킬 이름을 직접 언급해보세요.

```text
Use $gated-plan-execution and show how you would execute a two-step markdown plan with approval after each step.
```

```text
Use $qa-workflow-expert and explain what checklist, evidence, report, and Japanese summary you would produce from a change-summary document.
```

```text
Use $playwright-cli to open https://example.com, take a snapshot, and describe what you observed.
```

```text
Use $api-pf-release-notes to explain how you would discover inputs, inspect commit history, and build a Japanese release note package from a provided directory.
```

정상이라면 Codex가 해당 스킬을 인식하고, 각 스킬의 역할에 맞는 방식으로 응답하거나 실행을 시작해야 합니다.

## 저장소 구조

```text
skills/
  gated-plan-execution/
    SKILL.md
    agents/
      openai.yaml
  qa-workflow-expert/
    SKILL.md
    agents/
      openai.yaml
    references/
      output-patterns.md
  playwright-cli/
    SKILL.md
    references/
      *.md
  api-pf-release-notes/
    SKILL.md
    agents/
      openai.yaml
    assets/
      output_template.md
    references/
      *.md
    scripts/
      *.py
```

## 참고

Codex가 `~/.codex/skills/**/SKILL.md` 형태의 스킬 폴더를 인식한다는 예시는 OpenAI의 공개 skills 저장소 README에도 나와 있습니다.
