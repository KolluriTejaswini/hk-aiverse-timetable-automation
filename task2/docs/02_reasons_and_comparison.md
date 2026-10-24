# Reasons for the changes (12) and comparison with job descriptions

Evidence labels: **JD** = from the job descriptions in `sources/job_descriptions.md`; **HB** = observed in the 2023-24 handbook (credit structure only); **A** = my assumption. Course content was **not** checked against detailed syllabi (see limitations), so "current course" statements are based on titles.

| # | Reason | Evidence | Change |
|---|---|---|---|
| R1 | Employers ask for production-grade Python, version control, tests and APIs; the AI table has a Python/R coding course (DS202) and a web course (CS205) that can carry this | JD-A, JD-B | C02, C03 UPDATE |
| R2 | Testing, documentation and repository discipline appear in the JDs, but the AI table has **no software-engineering or testing course**; the CSE table (4.7.6) lists Software Engineering (CS304) and the IT table lists Software Testing | JD-A, JD-B, JD-C; HB | N03 ADD (3 cr) |
| R3 | Deploying, monitoring and versioning models (CI/CD, drift, rollback) is explicit in two JDs; no AI-table course covers deployment | JD-A, JD-B, JD-D; HB | N04 ADD (3 cr) |
| R4 | Spark / Hadoop / cloud data platforms are named; DS307 Big Data systems is the natural place | JD-A, JD-C | C05 UPDATE |
| R5 | SQL pipelines and pandas/NumPy are asked for; DS305 sits right after DBMS (CS206) | JD-B, JD-C | C04 UPDATE |
| R6 | LLM tooling and NLP appear in two JDs; DS311 NLP is in Sem VI | JD-A, JD-D | C06 UPDATE |
| R7 | Blockchain does not appear in any of the four JDs (small sample, n=4, so this is a weak signal) | JD | C10 REDUCE: core -> elective pool |
| R8 | Embedded systems does not appear; edge deployment is kept by refreshing the IoT course | JD; A | C11 REDUCE, C01 UPDATE |
| R9 | Version control is needed from the first coding course on; a 1-credit lab in Sem I is a prerequisite for DS202 and the new Sem V course | JD-A, JD-B; A | N01 ADD (1 cr) |
| R10 | Governance, legal and model-risk controls are named in a JD; a short seminar introduces them early | JD-B | N02 ADD (1 cr) |
| R11 | Sem I and II repeat the same common courses in every B.Tech table of the handbook; trimming 1 credit each from Digital Fabrication and Engineering Graphics funds the two 1-credit additions without changing semester load | HB; A | C08, C09 REDUCE |
| R12 | Only one project course (SP301, 3 cr) sits before the Sem VII internship; making it a structured capstone around a real workflow (Task 1) uses existing credits | HB | C07 UPDATE |

## Skill-to-curriculum comparison (course titles only)

| Skill from JDs | Where the 2023 AI curriculum touches it (title-level) | Gap? | Proposed |
|---|---|---|---|
| Python, Git, tests | CS101, DS202 | Git/testing not visible in titles | NEW-01, C02 |
| SQL, pipelines | CS206, DS305 | Partly | C04 |
| ML / DL / NLP | DS304, DS306, DS311, DS310 | No | C06 only |
| Big data | DS307 | Partly (tools unknown) | C05 |
| Deployment / MLOps / cloud | none by title | **Yes** | N04 |
| Software engineering, testing | none in AI table | **Yes** | N03 |
| Governance | none | Yes | N02 |

## Prerequisite chain proposed
NEW-01 Git lab (Sem I) -> DS202 (Sem IV) -> NEW-03 Software Engineering & Testing (Sem V) -> NEW-04 MLOps & Deployment (Sem VI, also needs DS304 Machine Learning) -> SP301 capstone (Sem VI). CS205 needs CS201 and CS206 (Sem III), already earlier.

## Regulatory and approval conditions (to verify)
- Sem I-II courses are common to all B.Tech branches in the handbook, so C08/C09 would need cross-branch agreement.
- I have not seen the regulations: check minimum total credits, elective-pool rules and how Blockchain/Embedded would be offered as electives.
- Programme total stays 165 and each semester load is unchanged, so no regulation on total or semester credit load should be affected (A).
- This is **student work, not an official syllabus revision.**
