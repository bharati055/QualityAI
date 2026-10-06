# Gco Use Cases

How this skill connects to **Google Cloud Monitoring / GCP Console** (later addon).

## 1. SLOs and alerts

Use service SLIs (latency, availability, error rate) in GCO to define SLOs and alerts that match reliability expectations reviewed in this skill.

## 2. Performance and load requirements

Use historical GCO metrics to derive realistic performance and load requirements (RPS, p95/p99, saturation) that plans and gates can check against.

## 3. Test-failure RCA and reporting

Correlate failing tests with GCO metrics (spikes, dependency errors, resource saturation) to support root-cause analysis and RCA reports.

## v1 note

Document which metrics *would* matter. Do not require live GCO access in v1.
