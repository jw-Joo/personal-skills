# README Post-Install Verification Design

## Goal

README에 설치만 끝나는 안내가 아니라, 설치 후 실제로 스킬과 `playwright-cli`가 동작하는지 확인하는 검증 흐름까지 포함한다.

## Approach

설치 절차 뒤에 별도의 검증 섹션을 추가한다. 이 섹션은 먼저 `playwright-cli`로 브라우저를 열고 `example.com`에 이동한 뒤 스냅샷을 남기는 간단한 실행 테스트를 수행하게 한다. 그 다음 Codex에게 세 스킬을 각각 직접 언급하는 프롬프트 예시를 제공해서, 설치된 스킬이 실제 세션에서 호출 가능한지 확인하도록 안내한다.

## Why This Design

`playwright-cli` 스킬은 문서만 복사돼 있어도 실제 CLI가 없으면 동작하지 않을 수 있다. 반대로 스킬 디렉터리만 설치되어 있어도 Codex 세션에서 스킬 이름을 직접 불러보지 않으면 실제 인식 여부를 확신하기 어렵다. 그래서 CLI 실행 확인과 스킬 호출 확인을 둘 다 README에 넣는 것이 가장 실용적이다.
