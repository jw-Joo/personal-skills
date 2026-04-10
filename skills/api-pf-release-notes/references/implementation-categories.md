# Implementation Categories

Use only the following category labels in `### 実装内容`:

- `インフラ`
- `フロントエンド`
- `バックエンド`
- `その他(API-PF 自体ではない)`

## Path Heuristics

Apply these heuristics after reading commit messages, changed paths, and diff context:

- `client/` changes or visible UI behavior: `フロントエンド`
- `server/`, `functions/`, `iotsafe/api/`, service logic, or API schema changes: `バックエンド`
- `cdk/`, `docker/`, deployment, infrastructure, or environment plumbing: `インフラ`
- Non-API-PF deliverables or assets that are not an API-PF code change: `その他(API-PF 自体ではない)`

## Decision Rules

- Use multiple categories when one release note spans multiple layers.
- Group bullets by category in the final document.
- Ask the user when the diff does not support a confident category decision.
- Ask about missing screenshots when `フロントエンド` is present and no image candidates were found.
