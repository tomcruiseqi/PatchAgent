# Setup-only failed attempt

All 18 jobs stopped before model construction or API calls because infra/helper.py was executed with /usr/bin/python (Python 2.7). Every run has model_request_count=0; this directory is preserved for diagnosis and is excluded from model comparison.

Fix: the campaign bin/python shim directs OSS-Fuzz helper scripts to /usr/bin/python3 and is prepended to PATH only for this campaign.
