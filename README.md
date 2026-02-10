# PyIntruder

A lightweight, open-source HTTP request mutation engine inspired by Burp Suite Intruder, built for penetration testers who want fine-grained control without proprietary tooling.

PyIntruder is **not a scanner**. It is a **request templating and execution engine** designed to surface response differentials through controlled payload injection.

---

## Philosophy

Commercial tools abstract too much too early.  
PyIntruder is built to expose *how* request mutation, payload injection, and concurrency actually work.

Design goals:
- Raw HTTP fidelity
- Deterministic request mutation
- Bounded, controllable concurrency
- Operator-driven testing only
- Minimal dependencies

---

## Features (v1)

- Raw HTTP request templates (from file)
- Explicit injection markers using `{name}` syntax
- Sniper-style attack mode
- Wordlist-based payloads
- Async request execution
- Response metrics:
  - Status code
  - Response length
  - Response time
- CLI-only (no proxy, no GUI)

---

## Non-Goals (v1)

- ❌ Automatic vulnerability detection
- ❌ Crawling or discovery
- ❌ Proxy interception
- ❌ Burp extension compatibility
- ❌ Cluster-bomb style attacks

These may be explored in later versions.

---

## Injection Markers

Injection points are explicitly defined using curly braces:

```http
POST /login HTTP/1.1
Host: example.com
Content-Type: application/x-www-form-urlencoded

username={user}&password={pass}
