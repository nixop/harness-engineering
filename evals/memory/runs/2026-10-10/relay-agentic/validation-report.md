# Validation report (agentic memory, Relay)

Sources: 70; without parseable JSON: 0 []
- dropped open item taken without a prior raise (iac, 2026-01-12) in meetings/2026-01-12-weekly-sync.txt: 'Write the ADR for the Terraform to CloudFormation migration.'
- dropped open item taken without a prior raise (slo, 2026-01-19) in meetings/2026-01-19-weekly-sync.txt: 'Lena will cover SLOs at the next meeting.'
- dropped open item taken without a prior raise (cost, 2026-01-26) in meetings/2026-01-26-weekly-sync.txt: 'Discuss Relay cost visibility separately at the next meeting'
- dropped open item taken without a prior raise (database, 2026-02-02) in meetings/2026-02-02-weekly-sync.txt: 'The database work is planned for the second half of the year'
- dropped open item taken without a prior raise (gateway, 2026-03-02) in meetings/2026-03-02-weekly-sync.txt: 'Finish the network stack so the gateway can use VPC Link.'
- dropped open item taken without a prior raise (retries, 2026-03-16) in meetings/2026-03-16-weekly-sync.txt: 'Discuss gateway retries separately in two weeks.'
- dropped open item taken without a prior raise (idempotency, 2026-03-30) in meetings/2026-03-30-weekly-sync.txt: 'Implement idempotency keys by May.'
- dropped open item taken without a prior raise (idempotency, 2026-04-13) in meetings/2026-04-13-weekly-sync.txt: 'Finish idempotency keys development by May.'
- dropped open item closed without a prior raise (ownership, 2026-04-27) in meetings/2026-04-27-weekly-sync.txt: 'Marat said he is closing it'
- dropped open item closed without a prior raise (security, 2026-04-27) in meetings/2026-04-27-weekly-sync.txt: 'Old API key has been revoked and all four services are on IA'
- dropped open item taken without a prior raise (idempotency, 2026-04-27) in meetings/2026-04-27-weekly-sync.txt: 'Idempotency is being tested in staging'
- dropped open item taken without a prior raise (database, 2026-05-04) in meetings/2026-05-04-poc-review.txt: 'Own the state and hybrid parts needed for the migration dry '
- dropped open item taken without a prior raise (gateway, 2026-05-04) in meetings/2026-05-04-poc-review.txt: 'Take ownership of gateway work for the migration context.'
- dropped open item taken without a prior raise (idempotency, 2026-05-11) in meetings/2026-05-11-weekly-sync.txt: 'Make idempotency keys mandatory starting on 2026-06-01.'
- decision dated 2026-06-01 in a meeting of 2026-05-18 (meetings/2026-05-18-weekly-sync.txt): date set to the meeting date
- dropped open item raised_again without a prior raise (database, 2026-05-18) in meetings/2026-05-18-weekly-sync.txt: 'The team does not know the decommissioning date.'
- dropped open item taken without a prior raise (idempotency, 2026-06-01) in meetings/2026-06-01-weekly-sync.txt: 'All four callers must send idempotency keys; grace period is'
- open item raised twice (database, 2026-06-08) in meetings/2026-06-08-weekly-sync.txt, treated as raised again
- open item raised twice (database, 2026-06-29) in meetings/2026-06-29-weekly-sync.txt, treated as raised again
- open item raised twice (compute, 2026-07-20) in meetings/2026-07-20-weekly-sync.txt, treated as raised again
- dropped open item taken without a prior raise (compute, 2026-08-10) in meetings/2026-08-10-weekly-sync.txt: 'Sizing for provisioned compute will be decided after the loa'
- dropped open item taken without a prior raise (compute, 2026-08-17) in meetings/2026-08-17-weekly-sync.txt: 'The load test at 10x remains open.'
- dropped open item taken without a prior raise (retries, 2026-08-24) in meetings/2026-08-24-weekly-sync.txt: 'Check the queue under load before finalizing the retry chang'
- open item raised twice (compute, 2026-09-14) in meetings/2026-09-14-weekly-sync.txt, treated as raised again
- A01 says it replaces 'Keep Relay on old Terraform 0.12 and update the ve' but no earlier decision on iac exists
- A12 says it replaces 'Relay was planned behind API Gateway with gateway ' but no earlier decision on gateway exists
- A03 depends_on 'The current timeout is inside the service and ther' not matched
- A12 depends_on 'The network stack must be finished first so VPC Li' not matched
- A12 closes 'The open item of deciding the gateway placement an' not matched
- A30 depends_on 'After the incident on the 14th, the team wanted to' not matched
- A48 depends_on 'A load test is needed to validate that Lambda meet' not matched
- stale note not linked: document 'document db' / decision database 2026-04-06
- stale note not linked: document 'ADR-004' / decision iac 2026-04-20
- stale note not linked: document 'ADR-007' / decision compute 2026-08-03

Decisions kept: 58 (rejected 0, superseded 11); open items: 40; ownership events: 33; ADRs: 10; documents: 26; PoCs: 3; stale notes: 3; graph lines: 872

## Register issues (not written)

- unresolved person 'null' in meetings/2026-07-06-weekly-sync.txt
