# Tasks: Search Books by Author

**Input**: Design documents from `/specs/002-add-a-new/`
**Prerequisites**: plan.md (required)

## Execution Flow (main)
- Loaded plan.md for technical context and requirements.
- No contracts/ or data-model.md found; using plan and spec only.

## Task List

[X] T001 Setup project environment and dependencies (requirements.txt, Flask-RESTful, logging)
[X] T002 [P] Write contract/integration test for GET /books/author/<string:author> endpoint in tests/test_books.py
[X] T003 Implement BookAuthorSearch Resource in main.py with validation, logging, and error handling
[X] T004 Integrate endpoint registration in main.py
[X] T005 [P] Add/update persistent storage logic for author search in book.json
[X] T007 Polish: Update documentation (README.md) to include new endpoint and usage examples

## Parallel Execution Guidance
- T002, T005, T006 can be run in parallel (different files: tests/test_books.py, book.json)
- T003 and T004 must be sequential (same file: main.py)
- T007 can be run after implementation and tests

## Dependency Notes
- Setup (T001) must be completed before all other tasks
- Tests (T002, T006) should be written before implementation (T003, T004) for TDD compliance
- Documentation (T007) is last, after feature and tests are complete

---
