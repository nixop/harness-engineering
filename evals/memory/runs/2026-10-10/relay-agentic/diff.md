# Agentic memory vs ground truth (Relay)

- Decisions: truth 30, agentic 58, matched 27 -> recall 0.90, precision 0.47
- Status agreement on matched: 21/27; owner agreement: 23/27; proposer: 23/27; objector: 23/27
- SUPERSEDES: truth 7, agentic 11, correct 2
- ADR links on matched: truth 8, agreed 8
- Open items: truth 8, agentic 40, matched 7
- Ownership spans (topics): truth 13, agentic 19, exact (who, from, to) 7

## Missed decisions

- D10 2026-05-04 database: DynamoDB single-table design, chosen on PoC-1 results (p99 read 4 ms vs 11 ms; 38% lower c
- D18 2026-08-03 compute: Keep Relay on EKS with autoscaling (rejected: p95 0.4 s but 1.7x the monthly cost and a se
- D19 2026-08-10 database: DynamoDB migration dry run on a production snapshot is owned by Sergey, due 2026-09-04

## Extra decisions (no ground-truth match)

- A02 2026-01-19 iac: The migration to CFN will start with compute, with data network handled last. (meetings/2026-01-19-weekly-sync.txt)
- A03 2026-01-19 timeouts: Relay will keep a 60 s delivery timeout for now because there is no gateway yet. (meetings/2026-01-19-weekly-sync.txt)
- A04 2026-01-26 cost: All Relay resources should have cost center tags starting this quarter. (meetings/2026-01-26-weekly-sync.txt)
- A06 2026-02-02 iac: The compute module was moved into a CloudFormation stack and imported without recreation,  (meetings/2026-02-02-weekly-sync.txt)
- A07 2026-02-02 iac: Enable drift detection immediately on the new stack. (meetings/2026-02-02-weekly-sync.txt)
- A11 2026-02-23 security: Manual changes in production are forbidden. (meetings/2026-02-23-incident-review.txt)
- A15 2026-03-30 iac: The network stack has been moved to CloudFormation and the peering was imported without re (meetings/2026-03-30-weekly-sync.txt)
- A16 2026-03-30 idempotency: Idempotency keys should be implemented in May. (meetings/2026-03-30-weekly-sync.txt)
- A19 2026-04-13 iac: The team will revisit the network migration with numbers next week before changing the pla (meetings/2026-04-13-weekly-sync.txt)
- A20 2026-04-13 idempotency: Idempotency keys are in development and are expected to be ready by May. (meetings/2026-04-13-weekly-sync.txt)
- A22 2026-05-04 database: Adopt DynamoDB single-table for Relay. (meetings/2026-05-04-poc-review.txt)
- A23 2026-05-04 database: Run a dry run of the migration on a production snapshot before backfill. (meetings/2026-05-04-poc-review.txt)
- A24 2026-05-11 database: The single-table data model was documented with partition key customer_id and sort key typ (meetings/2026-05-11-weekly-sync.txt)
- A25 2026-05-11 gateway: The gateway will keep a 10 s limit, even though slow clients may hold delivery longer and  (meetings/2026-05-11-weekly-sync.txt)
- A26 2026-05-11 idempotency: Idempotency keys will become mandatory on 2026-06-01. (meetings/2026-05-11-weekly-sync.txt)
- A27 2026-05-11 slo: The team will revisit the synchronous mode question at the next meeting. (meetings/2026-05-11-weekly-sync.txt)
- A28 2026-05-18 database: The dry run topic remains open without an owner, and the team does not yet know when to tu (meetings/2026-05-18-weekly-sync.txt)
- A31 2026-06-01 iac: The network remains in Terraform, application stacks remain in CloudFormation, and drift d (meetings/2026-06-01-weekly-sync.txt)
- A32 2026-06-01 iac: The state has been cleaned up. (meetings/2026-06-01-weekly-sync.txt)
- A34 2026-06-01 idempotency: Idempotency keys are required starting today, with a two-week grace period, and all four c (meetings/2026-06-01-weekly-sync.txt)
- A35 2026-06-01 retries: Retries are handed over from Nikita to Anna starting today. (meetings/2026-06-01-weekly-sync.txt)
- A38 2026-06-29 compute: PoC-2 on EKS with Carpenter is under load and its p95 is 0.4 s. (meetings/2026-06-29-weekly-sync.txt)
- A39 2026-06-29 compute: PoC-3 on Lambda has a working basic variant, but the hybrid and state work took a week. (meetings/2026-06-29-weekly-sync.txt)
- A40 2026-06-29 ownership: PoC-3 should be handed over to Ivan Melnik when he joins on 2026-07-06. (meetings/2026-06-29-weekly-sync.txt)
- A42 2026-07-13 compute: Ivan will rewrite the handlers to use provisioned concurrency and SQS between intake and d (meetings/2026-07-13-weekly-sync.txt)
- A43 2026-07-13 compute: The cold start issue during long delivery is the main question to verify in PoC-3. (meetings/2026-07-13-weekly-sync.txt)
- A44 2026-07-27 compute: The team decided to keep Lambda as the preferred option because the cost is 41% lower than (meetings/2026-07-27-poc-review.txt)
- A45 2026-07-27 compute: Provisioned concurrency on deliver is mandatory for Lambda to be viable. (meetings/2026-07-27-poc-review.txt)
- A46 2026-07-27 slo: The Lambda option is acceptable only if p95 stays at 1.9 seconds and there is no safety ma (meetings/2026-07-27-poc-review.txt)
- A47 2026-07-27 timeouts: The team agreed that the SLO is 2 seconds for the first delivery attempt, not for the clie (meetings/2026-07-27-poc-review.txt)
- A54 2026-09-21 cutover: The rollback runbook will be owned by Lena and written by the end of the week. (meetings/2026-09-21-weekly-sync.txt)

## Open items

- Q1 2026-01-19 timeouts open owner=None again=[]: Review timeout behavior for slow endpoints and queue growth.
- Q2 2026-01-26 cost open owner=None again=[]: Add cost center tags to all resources starting this quarter.
- Q3 2026-02-02 iac open owner=None again=[]: Enable drift detection on the new stack.
- Q4 2026-02-02 database open owner=None again=[]: The DocumentDB read p99 is 9 ms at peak and keeps growing every month.
- Q5 2026-02-02 retries open owner=None again=[]: The queue of undelivered messages is not decreasing.
- Q6 2026-02-23 security open owner=None again=[]: Set up an alert routing path into on-call because current alerts go to
- Q7 2026-03-16 retries open owner=None again=[]: Gateway retries cannot be enabled yet.
- Q8 2026-03-23 database open owner=None again=[]: The DocumentDB read p99 is 11 ms again on Friday.
- Q9 2026-03-23 database open owner=None again=[]: Start the database work in April.
- Q10 2026-03-30 retries open owner=None again=[]: Define a retry budget so enabling retries does not cause a storm.
- Q11 2026-04-06 database open owner=None again=[]: Assess DynamoDB for poc-1 by comparing single-table vs multi-table on 
- Q12 2026-04-13 iac open owner=None again=[]: Bring numbers for the network migration decision next week.
- Q13 2026-04-20 iac open owner=None again=[]: Clean up Terraform state for resources that already moved to CloudForm
- Q14 2026-04-20 iac closed owner=Pavel Grishin again=[]: Who will take cleanup of the Terraform state.
- Q15 2026-05-04 database closed owner=Sergey Belov again=[]: Prepare the migration model and script for the dry run on a production
- Q16 2026-05-04 database open owner=None again=[]: The dry run migration item remains open without an owner.
- Q17 2026-05-11 slo open owner=None again=[]: Decide the synchronous mode question at the next meeting.
- Q18 2026-05-18 database closed owner=None again=['2026-06-08']: Dry run has no owner yet.
- Q19 2026-05-18 database open owner=None again=[]: Decide when to turn off DocumentDB after migration.
- Q20 2026-06-15 compute open owner=None again=[]: Compare EKS with autoscaling versus Lambda for relay delivery workload
- Q21 2026-06-15 database closed owner=Marat Yusupov again=['2026-06-29', '2026-07-20']: Perform a dry run.
- Q22 2026-06-29 compute open owner=None again=[]: Meet next week and decide who should own PoC-3.
- Q23 2026-07-06 ownership open owner=None again=[]: оформим передачу
- Q24 2026-07-13 compute open owner=None again=[]: Verify whether provisioned concurrency and warmed instances on deliver
- Q25 2026-07-20 compute open owner=None again=['2026-07-20']: EKS PoC report is due on Friday.
- Q26 2026-07-27 compute closed owner=Lena Kim again=[]: Run a 10x load test on the current PoC volume.
- Q27 2026-08-03 compute closed owner=Ivan Melnik again=[]: Provisioned concurrency sizing remains open: how many instances to kee
- Q28 2026-08-10 database open owner=None again=[]: Date of the document DB decom remains open and is after cutover.
- Q29 2026-08-17 compute open owner=None again=['2026-09-14']: Load test at 10x has not been taken by anyone yet.
- Q30 2026-08-17 retries open owner=None again=[]: There is a retries problem on Lambda because the gateway retries into 
- Q31 2026-08-24 cutover closed owner=Lena Kim again=[]: Write a rollback runbook for the serverless cutover.
- Q32 2026-09-07 security open owner=None again=[]: Rotate DocumentDB credentials before the decommission because they hav
- Q33 2026-09-14 cutover open owner=None again=[]: The load test for 10x is still without an owner and cutover is in five
- Q34 2026-09-14 database open owner=None again=[]: The DynamoDB dual-write remains open.
- Q35 2026-09-21 cutover open owner=None again=[]: Cutover runbook was published; rollback owner is still TBD.
- Q36 2026-09-28 security open owner=None again=[]: Rotation of credentials for the document DB is still unowned.
- Q37 2026-09-28 cutover open owner=None again=[]: Cutover planning remains open.
- Q38 2026-10-05 cutover open owner=None again=[]: Rollback details are TBD in the runbook.
- Q39 2026-10-05 database open owner=None again=[]: DocumentDB decommission date.
- Q40 2026-10-05 security open owner=None again=[]: Rotate credentials before decommission.
