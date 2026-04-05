# personal-skills

다른 PC에서도 바로 내려받아 쓸 수 있도록 개인용 Codex 스킬 원문을 보관하는 저장소입니다.

현재 이 저장소에는 내가 전역에서 사용 중인 아래 3개 스킬의 원문이 그대로 들어 있습니다.

## 포함된 스킬

* `gated-plan-execution`
* `qa-workflow-expert`
* `playwright-cli`

## 이 저장소의 목적

* 다른 PC에서 이 저장소만 clone 해도 개인 스킬 3개의 원문을 바로 확보할 수 있게 하기
* `obra/superpowers`를 먼저 설치한 뒤, 필요한 개인 스킬을 추가로 복사해서 쓸 수 있게 하기

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

혹은 GitHub에서 필요한 `SKILL.md` 파일만 직접 내려받아도 됩니다.

Raw URLs:
* `gated-plan-execution`: `https://raw.githubusercontent.com/jw-Joo/personal-skills/main/skills/gated-plan-execution/SKILL.md`
* `qa-workflow-expert`: `https://raw.githubusercontent.com/jw-Joo/personal-skills/main/skills/qa-workflow-expert/SKILL.md`
* `playwright-cli`: `https://raw.githubusercontent.com/jw-Joo/personal-skills/main/skills/playwright-cli/SKILL.md`

### 3. 마지막으로 개인 스킬 3개를 순서대로 복사

아래 예시는 macOS/Linux 기준이며, 심볼릭 링크가 아니라 실제 파일 복사 방식입니다.

```bash
mkdir -p ~/.codex/skills
cp -R ~/.codex/personal-skills/skills/gated-plan-execution ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/qa-workflow-expert ~/.codex/skills/
cp -R ~/.codex/personal-skills/skills/playwright-cli ~/.codex/skills/
```

Codex에게 한 번에 맡기고 싶다면, 아래처럼 순서가 드러나는 요청문으로 안내하면 됩니다.

```text
1. Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.codex/INSTALL.md
2. Clone https://github.com/jw-Joo/personal-skills.git into ~/.codex/personal-skills
3. Copy these folders into ~/.codex/skills in order:
   - ~/.codex/personal-skills/skills/gated-plan-execution
   - ~/.codex/personal-skills/skills/qa-workflow-expert
   - ~/.codex/personal-skills/skills/playwright-cli
4. Restart Codex after installation
```

## 설치 확인

```bash
ls -la ~/.codex/skills/gated-plan-execution
ls -la ~/.codex/skills/qa-workflow-expert
ls -la ~/.codex/skills/playwright-cli
```

필요하면 Codex를 재시작한 뒤, 해당 스킬 이름을 직접 언급해서 불러오거나 관련 작업을 요청해 동작을 확인하세요.

## 저장소 구조

```text
skills/
  gated-plan-execution/
    SKILL.md
  qa-workflow-expert/
    SKILL.md
  playwright-cli/
    SKILL.md
```

## 참고

Codex가 `~/.codex/skills/**/SKILL.md` 형태의 스킬 폴더를 인식한다는 예시는 OpenAI의 공개 skills 저장소 README에도 나와 있습니다.
