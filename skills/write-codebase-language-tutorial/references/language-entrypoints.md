# Language entrypoint routing

## Contents

- Generic discovery
- Go
- Rust
- TypeScript and React
- Other languages

## Generic discovery

First classify the artifact:

- HTTP/RPC server
- CLI
- worker or queue consumer
- scheduled job
- frontend SPA/SSR app
- reusable library
- multi-process workspace

Trace the launch command to the actual entrypoint. Do not assume `main` is the only process when a repository has multiple binaries or packages.

Search manifests and run configuration before broad source reading. Exclude dependency, generated, and build-output directories from the first pass.

## Go

### Discover

Inspect:

- `go.work`, then each `go.mod`;
- `cmd/*/main.go`, other `package main` files, and build tags;
- Makefile, Taskfile, container entrypoint, deployment command, or process manager;
- router/server registration, worker startup, or CLI command registration;
- generated files, `vendor/`, and mocks before treating code as authored logic.

Useful searches:

```bash
rg -n '^package main$|^func main\(' --glob '*.go'
rg -n 'http\.Handle|HandleFunc|grpc\.NewServer|cobra\.Command|Run\(' --glob '*.go'
```

### Teach in likely order

1. `package`, imports, `func`, parameters, and return values.
2. `:=` versus `var`, zero values, structs, and field access.
3. Multiple return values and explicit `if err != nil` flow.
4. Methods, pointer receivers, interfaces, and concrete implementations.
5. `defer` and `context.Context` when the traced path reaches them.
6. Goroutines, channels, reflection, generics, and advanced concurrency only when required.

### Representative server flow

Prefer one real path:

```text
process command
→ package main / func main
→ config and dependencies
→ router registration
→ handler
→ service/use case
→ repository or external client
→ encoded response/log/state change
```

Explain interface wiring by showing both the interface-typed field/parameter and the concrete constructor assignment.

## Rust

### Discover

Inspect:

- root `Cargo.toml`, workspace members, package targets, and features;
- `src/main.rs`, `src/bin/*.rs`, explicit `[[bin]]`, and `src/lib.rs`;
- run commands in task files, containers, and deployment configuration;
- runtime setup (`tokio`, `async-std`), router/CLI framework, application state, and module declarations;
- `target/`, generated bindings, and vendored crates before treating code as authored logic.

Useful searches:

```bash
rg -n '^fn main\(|^async fn main\(' --glob '*.rs'
rg -n '#\[tokio::main\]|Router::new|route\(|Command::new|clap' --glob '*.rs'
```

### Teach in likely order

1. `let`, `mut`, functions, structs, enums, and module paths.
2. `Option` and `Result`, then `match` and `?` on the first real error path.
3. Ownership versus borrowing only with the actual value that moves or is borrowed.
4. `&T`, `&mut T`, `String`, and `&str` through service inputs and state.
5. Traits and generics through one actual bound and implementation.
6. Macros (`!`) and attributes (`#[...]`) by separating generated/setup behavior from runtime flow.
7. `async`/`await`, `Arc`, locks, channels, and lifetimes when the representative path needs them.

### Representative server flow

Prefer one real path:

```text
cargo run target
→ main / async runtime
→ config and shared state
→ route registration
→ extractor and handler
→ service/domain function
→ database or external client
→ Result conversion and response
```

Never explain ownership as a complete theory before showing the exact move or borrow that matters in this flow.

## TypeScript and React

### Discover

Inspect:

- `package.json` scripts and actual dependencies;
- bundler/framework config and `index.html` or server entrypoint;
- `main.tsx`/`index.tsx`, root component, router registration, route files, and generated route tree;
- providers/contexts and one verified consumer;
- API client and one actual screen-to-server flow;
- `node_modules`, generated files, and build output before treating code as authored logic.

### Keep layers separate

- JavaScript syntax and runtime behavior
- TypeScript annotations and declarations that disappear at runtime
- React component/context/state behavior
- router/framework conventions
- bundler code generation and browser DOM

When teaching a Provider, verify the context object, provider value, consumer hook, and actual consuming component. When teaching routing, distinguish route configuration trees, React component trees, and browser DOM trees.

## Other languages

Apply generic discovery, then identify:

1. manifest/toolchain;
2. actual process entrypoint;
3. registration or dispatch boundary;
4. one representative input/output path;
5. language constructs first encountered on that path.

Use primary official documentation for semantics that cannot be established from code. Add a new language section only after the workflow recurs and the guidance is reusable.
