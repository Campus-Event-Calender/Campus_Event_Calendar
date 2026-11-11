# Software Test Plan

## 1. Introduction

This document defines the software testing approach for the Campus Event Calendar with RSVP project. The plan is based on a review of the implemented repository structure and source code, including the backend Flask API, SQLite database layer, frontend HTML/JavaScript pages, and the existing Pytest-based unit tests.

The objective of this test plan is to verify that the implemented features behave as expected, that integration between the frontend, backend, and database is reliable, and that the system remains stable across revisions. This plan does not claim that the application has already passed all tests; it describes the planned testing process and acceptance conditions for the current implementation.

The project under test includes the following verified implementation areas:
- Event CRUD functionality exposed through `/api/events`
- RSVP creation and cancellation endpoints under `/api/events/<id>/rsvp`
- Attendance-related reporting and CSV export under `/api/reports`
- Calendar view and event browsing in the frontend pages
- SQLite-based persistence with sample seed data
- Pytest-based automated tests in the `tests/` directory

The project also includes an explicit warning in the repository documentation that administrator authentication and authorization are not implemented. This is treated as a scope exclusion for this test plan unless such functionality is added in a future release.

## 2. Test Items

The following product items are in scope for testing:

1. Backend application entry point: `backend/app.py`
2. SQLite database schema and initialization: `backend/database.py`
3. Event retrieval and validation logic: `backend/routes/events.py`
4. RSVP logic: `backend/routes/rsvp.py`
5. Reporting and CSV export logic: `backend/routes/reports.py`
6. Data access helpers and event aggregation: `backend/models.py`
7. Frontend pages and JavaScript integration:
   - `frontend/index.html`
   - `frontend/calendar.html`
   - `frontend/events.html`
   - `frontend/reports.html`
   - `frontend/js/events.js`
   - `frontend/js/calendar.js`
   - `frontend/js/reports.js`
8. Automated unit tests:
   - `tests/test_events.py`
   - `tests/test_rsvp.py`
   - `tests/test_reports.py`
   - `tests/conftest.py`

## 3. Features to be Tested

The following feature list reflects the functionalities that are implemented and verifiable in the current source code.

| Requirement ID | Feature | Implementation Status | Verification Source |
|---|---|---|---|
| EVT-001 | Event list and event detail retrieval | Implemented | `backend/routes/events.py`, `backend/models.py` |
| EVT-002 | Event creation with required field validation | Implemented | `backend/routes/events.py`, `tests/test_events.py` |
| EVT-003 | Event update with time and capacity validation | Implemented | `backend/routes/events.py`, `tests/test_events.py` |
| EVT-004 | Event deletion and cascading removal of related records | Implemented | `backend/routes/events.py`, `tests/test_events.py` |
| CAL-001 | Calendar page rendering and event display | Implemented | `frontend/calendar.html`, `frontend/js/calendar.js` |
| RSVP-001 | RSVP registration for an event | Implemented | `backend/routes/rsvp.py`, `tests/test_rsvp.py` |
| RSVP-002 | Duplicate RSVP prevention by email | Implemented | `backend/routes/rsvp.py`, `tests/test_rsvp.py` |
| RSVP-003 | RSVP cancellation by student email | Implemented | `backend/routes/rsvp.py` |
| RSVP-004 | Event capacity enforcement | Implemented | `backend/routes/rsvp.py`, `backend/routes/events.py` |
| ATT-001 | Event attendee listing and attendance data aggregation | Implemented | `backend/routes/reports.py` |
| REP-001 | Attendance summary report | Implemented | `backend/routes/reports.py`, `tests/test_reports.py` |
| REP-002 | CSV export for attendance and RSVP summaries | Implemented | `backend/routes/reports.py`, `tests/test_reports.py` |
| UI-001 | Event management UI and modal interactions | Implemented | `frontend/events.html`, `frontend/js/events.js` |
| UI-002 | Reports page summary cards and charts | Implemented | `frontend/reports.html`, `frontend/js/reports.js` |

Notes:
- The `attendance` table exists in the schema and seed data, but the backend does not expose a matching `/api/events/<id>/attendance` POST endpoint in the current codebase. This means attendance recording is not considered a verified implementation feature for this test plan unless the API is added and then tested in a future revision.
- Administrator authentication and authorization are not implemented, as noted in the repository documentation and verified by code inspection. They are therefore excluded from this test plan.

## 4. Features Not to be Tested

The following items are not included in scope because they are either not implemented or outside the current project boundary:

1. Administrator authentication and authorization
   - No login, user management, or role-based access control was found in the backend or frontend source.
   - The project README explicitly notes this as a future enhancement and warns against treating UI hiding as security.

2. POST attendance recording endpoint `/api/events/<id>/attendance`
   - This route is documented in the README but is not implemented in the backend route files inspected in this project.
   - Since the actual code does not expose this endpoint, it cannot be treated as a verified feature for testing at this time.

3. Production deployment configuration and security hardening
   - This project is currently a local Flask application intended for demonstration and academic use.
   - Containerization, reverse proxy configuration, TLS, and enterprise security controls are outside the current scope.

4. Advanced non-functional testing outside the repository tooling
   - Performance benchmarks, load testing, and penetration testing are excluded unless the project requirements are expanded in a later phase.

## 5. Test Approach / Strategy

The project will use a mixed testing strategy combining automated and manual validation aligned to the implemented architecture.

### 5.1 Test Types

- Unit testing
  - Use the existing Pytest framework and the provided test fixtures to validate backend logic in isolation.
  - Focus: validation functions, event creation/update rules, RSVP logic, and reporting logic.

- Integration testing
  - Validate communication among Flask routes, SQLite database, and JSON responses.
  - Focus: event CRUD, duplicate RSVP handling, capacity enforcement, and CSV/report generation.

- System testing
  - Validate the complete web application behavior through the browser and API endpoints.
  - Focus: page rendering, navigation, modal interactions, and user flows such as creating events, reserving seats, and viewing reports.

- Regression testing
  - Re-run critical API and UI tests after changes to validation logic, route definitions, or database schema.
  - Focus on the core flows previously identified in the requirement matrix.

- Usability testing
  - Assess readability, navigation clarity, validation feedback, and ease of use for campus users interacting with the event, calendar, and report pages.

### 5.2 Entry Criteria

A test cycle may begin when all of the following conditions are met:
- The code is available in the repository and builds or starts the application successfully.
- Required dependencies are installed according to `requirements.txt`.
- The SQLite database can be initialized without critical errors.
- The application can be run locally using a valid Flask entry point.
- Critical test cases for event CRUD and RSVP flows are available in the automated suite.

### 5.3 Exit Criteria

A test cycle may be considered complete when:
- All planned test cases have been executed or formally marked as blocked/not applicable.
- All critical defects are resolved, deferred, or accepted with documented rationale.
- No open critical or high-severity defects remain without approval.
- Test evidence is recorded and traceability to the requirement IDs is updated.
- The project team reviews the final test summary before formal release or academic submission.

## 6. Test Environment

The testing environment will reflect the real project stack and tools used in the repository.

### 6.1 Hardware and Software
- Operating system: Windows environment used during project development
- Python version: as installed in the local development environment, consistent with the project runtime
- Backend framework: Flask 3.1.2
- Backend CORS support: flask-cors 6.0.1
- Database: SQLite via native Python `sqlite3`
- Frontend: HTML, CSS, and JavaScript
- UI libraries: FullCalendar 6.1.19 and Chart.js
- Automated test framework: Pytest 8.4.2

### 6.2 Execution Environment
- Local development execution using `python -m backend.app`
- Browser-based system testing using local web pages served by Flask
- API validation via Flask test client and browser `fetch` requests
- Database validation using temporary SQLite databases created in the existing test fixture setup

## 7. Test Schedule

The schedule below is a working template to be adjusted by the project team as necessary. Dates are placeholders and can be edited for the actual academic delivery timeline.

| Phase | Activity | Planned Window | Owner |
|---|---|---|---|
| Phase 1 | Requirements review and test planning | Week 1 | [Project Manager / QA Lead] |
| Phase 2 | Unit test execution (Pytest) | Week 2 | [QA Engineer / Backend Developer] |
| Phase 3 | API integration testing | Week 3 | [Backend Developer / QA Engineer] |
| Phase 4 | System and usability testing | Week 4 | [Frontend Developer / QA Engineer] |
| Phase 5 | Regression testing | Week 5 | [QA Engineer] |
| Phase 6 | Final defect review and sign-off | Week 6 | [Project Manager / Review Board] |

The above schedule should be updated with the actual academic milestone dates before execution.

## 8. Test Deliverables

The following items will be produced as part of the test process:

1. Test plan document
2. Requirement-to-test traceability matrix
3. Unit test scripts in the repository (`tests/`)
4. Defect log and status summary
5. Test execution report with pass/fail/blocked status
6. Final sign-off form for academic submission

## 9. Roles and Responsibilities

The following role placeholders are recommended for the project team and should be replaced with actual names when the team is assigned.

| Role | Responsibility |
|---|---|
| Project Manager | Oversees schedule, scope, and overall test readiness |
| QA Engineer | Defines test cases, executes tests, manages defects, and maintains traceability |
| Backend Developer | Maintains Flask API and database logic; resolves backend defects |
| Frontend Developer | Maintains HTML/JavaScript views and user interaction flows |
| Database Administrator | Reviews schema integrity, data constraints, and reporting consistency |
| Reviewer / Academic Supervisor | Confirms test coverage, quality expectations, and final acceptance |

## 10. Risks and Mitigation

| Risk | Description | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| Invalid event time range | `end_time` may be earlier than or equal to `start_time` | Medium | High | Validate timestamps before persistence; test edge cases |
| Duplicate registration | Same email may be used to RSVP multiple times | Medium | High | Enforce unique constraint and verify duplicate rejection |
| Capacity overflow | RSVPs exceed event capacity | Medium | High | Check `rsvp_count` against `capacity` before confirming |
| Data inconsistency | Event deletion may remove related RSVP/attendance records | Medium | Medium | Validate cascade behavior through integration tests |
| Frontend validation mismatch | Client-side validation may differ from backend validation | Medium | Medium | Validate both client and server logic |
| Missing admin security | Public access to event management routes is a known concern | High | High | Document as out of scope for now; restrict in future secure release |
| CSV/report errors | Incorrect calculation or formatting may affect reporting | Medium | Medium | Validate report calculations and CSV headers |

## 11. Assumptions and Dependencies

The following assumptions apply to this test plan:
- The project will continue to use Flask, SQLite, and the existing Pytest infrastructure.
- The project is executed locally in a development environment rather than a production deployment.
- The repository remains the authoritative source of system behavior.
- Existing test fixtures create temporary SQLite databases for isolated validation.
- Browser and local environment dependencies remain available throughout testing.

Dependencies include:
- Python and package dependencies from `requirements.txt`
- SQLite database initialization during startup
- Frontend resources served by Flask static routing
- Network access for CDN-based libraries such as FullCalendar and Chart.js when loaded in a browser

## 12. Suspension and Resumption Criteria

### Suspension Criteria

Testing should be suspended if any of the following occurs:
- The application cannot be started or the database cannot be initialized.
- An environment issue prevents the execution of the required test suite.
- A defect blocks the completion of a critical path such as event creation or RSVP registration.
- The code under test is not stable enough to validate the required functionality.

### Resumption Criteria

Testing may resume only after:
- The blocking issue has been resolved or documented as an accepted risk.
- The environment has been restored to a valid state.
- The relevant test cases have been updated or re-evaluated if the defect changed the expected behavior.
- The project team confirms that the defect does not invalidate the planned scope.

## 13. Test Case Management and Traceability

Test case management will follow a requirement-based traceability approach. Each major requirement is mapped to a test identifier and source artifact.

| Requirement ID | Related Test IDs | Test Type | Source / Area |
|---|---|---|---|
| EVT-001 | TC-EVT-01, TC-EVT-02 | Functional, Integration | `tests/test_events.py`, `backend/models.py` |
| EVT-002 | TC-EVT-03, TC-EVT-04 | Functional, Unit | `tests/test_events.py` |
| EVT-003 | TC-EVT-05, TC-EVT-06, TC-EVT-07 | Functional, Unit | `tests/test_events.py` |
| EVT-004 | TC-EVT-08, TC-EVT-09 | Functional, Integration | `tests/test_events.py` |
| RSVP-001 | TC-RSVP-01 | Functional, Integration | `tests/test_rsvp.py` |
| RSVP-002 | TC-RSVP-02 | Functional, Regression | `tests/test_rsvp.py` |
| RSVP-003 | TC-RSVP-03 | Functional, Integration | `backend/routes/rsvp.py` |
| RSVP-004 | TC-RSVP-04, TC-RSVP-05 | Functional, Integration | `backend/routes/rsvp.py`, `backend/routes/events.py` |
| ATT-001 | TC-ATT-01 | Integration | `backend/routes/reports.py` |
| REP-001 | TC-REP-01 | Functional, Integration | `tests/test_reports.py` |
| REP-002 | TC-REP-02 | Functional, Integration | `tests/test_reports.py` |
| CAL-001 | TC-CAL-01, TC-CAL-02 | System, Usability | `frontend/calendar.html`, `frontend/js/calendar.js` |
| UI-001 | TC-UI-01, TC-UI-02 | System, Usability | `frontend/events.html`, `frontend/js/events.js` |
| UI-002 | TC-UI-03 | System, Usability | `frontend/reports.html`, `frontend/js/reports.js` |

The team should maintain a separate defect log and update this matrix as new test cases and requirements are added.

## 14. Test Metrics and Reporting

The project team will monitor the following quality indicators during testing:
- Number of planned, executed, passed, failed, blocked, and deferred test cases
- Number of open defects by severity
- Requirement coverage percentage against the implemented scope
- Critical path test pass rate for event CRUD and RSVP flows
- Regression test stability across iterations

Test reporting output should include:
- Summary status for each test cycle
- Defect severity and priority tracking
- Risk/issue escalation notes
- Updated traceability status

No test results will be reported as passed without execution evidence. This plan is intended to define the testing process, not to assert the outcome of the current test execution.

## 15. Approvals

This Software Test Plan will be approved by the relevant project stakeholders before formal execution or final academic review.

| Role | Name / Placeholder | Signature | Date |
|---|---|---|---|
| Project Manager | [Project Manager Name] |  |  |
| QA Lead | [QA Lead Name] |  |  |
| Backend Developer | [Backend Developer Name] |  |  |
| Frontend Developer | [Frontend Developer Name] |  |  |
| Academic Reviewer | [Reviewer Name] |  |  |

This document should be revised whenever the scope, team assignments, or delivery schedule change.
