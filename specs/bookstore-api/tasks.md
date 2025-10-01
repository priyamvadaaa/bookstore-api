# Tasks: Bookstore API

**Input**: Design documents from `/specs/bookstore-api/`
**Prerequisites**: plan.md (required)

## Phase 3.1: Setup
- [x] T001 Create project structure per implementation plan (main.py, tests/, README.md)
- [x] T002 Initialize Python project with Flask-RESTful and pytest dependencies
- [x] T003 [P] Configure linting and formatting tools (PEP8, flake8, black)

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
- [x] T004 [P] Contract test GET /books in tests/test_books.py
- [x] T005 [P] Contract test POST /books in tests/test_books.py
- [x] T006 [P] Contract test GET /books/<id> in tests/test_books.py
- [x] T007 [P] Contract test PUT /books/<id> in tests/test_books.py
- [x] T008 [P] Contract test DELETE /books/<id> in tests/test_books.py
- [x] T009 [P] Integration test for error cases (404, 400, invalid data) in tests/test_books.py
- [x] T020 [P] Implement GET /books?title=<search_term> endpoint in main.py
- [x] T021 [P] Add contract/integration tests for search by title in tests/test_books.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T010 [P] Implement in-memory Book data model in main.py
- [x] T011 [P] Implement GET /books endpoint in main.py
- [x] T012 [P] Implement POST /books endpoint in main.py
- [x] T013 [P] Implement GET /books/<id> endpoint in main.py
- [x] T014 [P] Implement PUT /books/<id> endpoint in main.py
- [x] T015 [P] Implement DELETE /books/<id> endpoint in main.py
- [x] T016 [P] Implement request data validation and error handling in main.py

## Phase 3.4: Polish & Documentation
- [ ] T017 [P] Add structured logging to main.py
- [ ] T018 [P] Document API endpoints and usage in README.md
- [ ] T019 [P] Add performance test for <200ms p95 latency in tests/test_books.py

## Dependencies
- All [P] tasks can be executed in parallel if they touch different files (e.g., tests/ and main.py).
- TDD: All test tasks (T004–T009) must be written and MUST FAIL before any implementation (T010–T016) begins.

## Validation Checklist
- [x] All contracts have corresponding tests
- [x] All entities have model tasks
- [x] All tests come before implementation
- [x] Parallel tasks truly independent
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task
