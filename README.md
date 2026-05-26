# personal-skills

다른 PC에서도 바로 내려받아 쓸 수 있도록 개인용 Codex 스킬 디렉터리와 설치 지침을 보관하는 저장소입니다.

현재 이 저장소에는 내가 전역에서 사용 중인 아래 7개 로컬 스킬이 보조 파일까지 포함된 형태로 들어 있습니다.

## 포함된 로컬 스킬

* `qa-workflow-expert`
* `playwright-cli`
* `api-pf-release-notes`
* `kc-manual-release-update`
* `kc-manual-change-summary`
* `tdd-implementation`
* `write-readable-html-docs`

## 외부에서 적용할 스킬

`gated-plan-execution`은 이 저장소에 더 이상 보관하지 않습니다.

계획, 이슈, PRD, TDD, 진단, 아키텍처 개선 같은 일반 엔지니어링 워크플로는 Matt Pocock의 skills 저장소를 설치해서 사용합니다.

* Upstream: <https://github.com/mattpocock/skills>
* Quickstart command:

```bash
npx skills@latest add mattpocock/skills
```

설치 선택 과정에서 `/setup-matt-pocock-skills`를 포함하고, 설치 후 새 에이전트 세션에서 `/setup-matt-pocock-skills`를 실행해 프로젝트별 설정을 먼저 잡습니다.

## 이 저장소의 목적

* 다른 PC에서 이 저장소만 clone 해도 개인 로컬 스킬 7개의 원문을 바로 확보할 수 있게 하기
* 필요한 개인 스킬 디렉터리를 선택해서 `~/.codex/skills`에 복사해 쓸 수 있게 하기
* 이 저장소에 vendoring하지 않는 Matt Pocock skills는 upstream 설치 절차로 적용하게 안내하기

## 중요한 점

일부 스킬은 `SKILL.md`만으로 끝나지 않습니다.

* `qa-workflow-expert`는 `agents/openai.yaml`과 `references/output-patterns.md`를 포함합니다.
* `playwright-cli`는 `references/*.md`를 포함합니다.
* `api-pf-release-notes`는 `agents/openai.yaml`, `assets/output_template.md`, `references/*.md`, `scripts/*.py`를 포함합니다.
* `kc-manual-release-update`는 `agents/openai.yaml`, `references/*.md`, `scripts/*.py`를 포함합니다.
* `kc-manual-change-summary`는 `agents/openai.yaml`을 포함합니다.
* `tdd-implementation`은 `agents/openai.yaml`을 포함합니다.
* `write-readable-html-docs`는 `agents/openai.yaml`, `references/html-patterns.md`, `scripts/validate_html_doc.py`를 포함합니다.

따라서 `SKILL.md` 파일만 따로 복사하면 불완전할 수 있습니다. 가능하면 항상 스킬 디렉터리 전체를 clone 또는 복사하세요.

## 권장 사용 순서

### 1. 이 저장소 클론

```bash
git clone https://github.com/jw-Joo/personal-skills.git ~/.codex/personal-skills
```

혹은 GitHub에서 ZIP으로 전체 저장소를 내려받은 뒤 `skills/` 디렉터리 전체를 사용해도 됩니다.

### 2. Matt Pocock skills 설치

이 저장소는 `gated-plan-execution`을 직접 제공하지 않습니다. 일반 엔지니어링 워크플로 스킬은 upstream에서 설치합니다.

```bash
npx skills@latest add mattpocock/skills
```

설치 중 사용할 코딩 에이전트와 필요한 스킬을 선택하세요. 특히 `/setup-matt-pocock-skills`를 포함해야 이후 프로젝트별 설정을 잡을 수 있습니다.

설치 후 새 에이전트 세션에서 다음을 실행합니다.

```text
/setup-matt-pocock-skills
```

### 3. `playwright-cli` 스킬을 쓰기 전에 CLI 먼저 설치

`playwright-cli` 개인 스킬은 `playwright-cli` 명령이 있는 환경을 전제로 합니다.

```bash
npm install -g @playwright/cli@latest
playwright-cli --version
```

### 4. 개인 로컬 스킬 7개를 복사

아래 예시는 WSL/Linux 기준이며, 심볼릭 링크가 아니라 스킬 디렉터리 전체를 실제로 복사하는 방식입니다.

```bash
mkdir -p ~/.codex/skills
cp -R ~/.codex/personal-skills/skills/qa-workflow-expert ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/playwright-cli ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/api-pf-release-notes ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/kc-manual-release-update ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/kc-manual-change-summary ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/tdd-implementation ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/write-readable-html-docs ~/.codex/skills/
```

Codex에게 한 번에 맡기고 싶다면, 아래처럼 순서가 드러나는 요청문으로 안내하면 됩니다.

```text
1. Clone https://github.com/jw-Joo/personal-skills.git into ~/.codex/personal-skills
2. Install Matt Pocock skills with: npx skills@latest add mattpocock/skills
3. Include /setup-matt-pocock-skills during that installation and run it in a new agent session
4. Install @playwright/cli globally and verify that playwright-cli is available
5. Copy these full local skill directories into ~/.codex/skills:
   - ~/.codex/personal-skills/skills/qa-workflow-expert
   - ~/.codex/personal-skills/skills/playwright-cli
   - ~/.codex/personal-skills/skills/api-pf-release-notes
   - ~/.codex/personal-skills/skills/kc-manual-release-update
   - ~/.codex/personal-skills/skills/kc-manual-change-summary
   - ~/.codex/personal-skills/skills/tdd-implementation
   - ~/.codex/personal-skills/skills/write-readable-html-docs
6. Restart Codex after installation
```

## 설치 확인

```bash
ls -la ~/.codex/skills/qa-workflow-expert
ls -la ~/.codex/skills/playwright-cli
ls -la ~/.codex/skills/api-pf-release-notes
ls -la ~/.codex/skills/kc-manual-release-update
ls -la ~/.codex/skills/kc-manual-change-summary
ls -la ~/.codex/skills/tdd-implementation
ls -la ~/.codex/skills/write-readable-html-docs
playwright-cli --version
```

Matt Pocock skills는 설치한 에이전트 환경에서 `/setup-matt-pocock-skills` 또는 설치한 개별 스킬 이름이 인식되는지 확인하세요.

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

### 2. Codex에서 로컬 스킬 직접 호출 확인

새 Codex 세션에서 아래처럼 각 로컬 스킬 이름을 직접 언급해보세요.

```text
Use $qa-workflow-expert and explain what checklist, evidence, report, and Japanese summary you would produce from a change-summary document.
```

```text
Use $playwright-cli to open https://example.com, take a snapshot, and describe what you observed.
```

```text
Use $api-pf-release-notes to explain how you would discover inputs, inspect commit history, and build a Japanese release note package from a provided directory.
```

```text
Use $kc-manual-release-update to explain how you would update kc-manual RST documentation from a full release-note package and create a before/after HTML report.
```

```text
Use $kc-manual-change-summary to explain how you would create a concise Japanese マニュアル変更箇所 Markdown file from a manual_update_report.
```

```text
Use $tdd-implementation and explain how you would classify a code change, add a failing test first when appropriate, implement the smallest fix, and report the red/green results.
```

```text
Use $write-readable-html-docs and explain how you would turn a Markdown design document into a standalone review-friendly HTML file, including source-sync validation.
```

### 3. Matt Pocock skills 설정 확인

Matt Pocock skills를 설치한 뒤 새 에이전트 세션에서 아래 명령을 실행해 프로젝트별 설정을 확인합니다.

```text
/setup-matt-pocock-skills
```

정상이라면 Codex가 로컬 스킬과 외부에서 설치한 Matt Pocock skills를 각각 인식하고, 각 스킬의 역할에 맞는 방식으로 응답하거나 실행을 시작해야 합니다.

## 저장소 구조

```text
skills/
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
  kc-manual-release-update/
    SKILL.md
    agents/
      openai.yaml
    references/
      *.md
    scripts/
      *.py
  kc-manual-change-summary/
    SKILL.md
    agents/
      openai.yaml
  tdd-implementation/
    SKILL.md
    agents/
      openai.yaml
  write-readable-html-docs/
    SKILL.md
    agents/
      openai.yaml
    references/
      html-patterns.md
    scripts/
      validate_html_doc.py
```

## 참고

Codex가 `~/.codex/skills/**/SKILL.md` 형태의 스킬 폴더를 인식한다는 예시는 OpenAI의 공개 skills 저장소 README에도 나와 있습니다.
