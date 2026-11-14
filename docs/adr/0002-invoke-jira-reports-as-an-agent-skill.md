# Invoke Jira reports as an agent skill

CAM-1619 will provide an explicitly invoked agent skill rather than a standalone reporting application. It will reuse the existing Atlassian CLI for discovery and ordinary reads, with authenticated Jira REST requests where history or pagination requires them. This choice keeps reporting within the existing agent workflow and authentication arrangements rather than introducing a separately operated service.

Scheduled execution, persistent report databases, dashboards, and external services are outside v1. The accepted trade-off is reliance on the agent and live Jira evidence rather than a durable historical reporting store, including the historical coverage qualifications recorded in ADR-0001.
