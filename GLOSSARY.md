# AI Scaffolding

This context covers agent-assisted workflows for CUAHSI project work. Its reporting vocabulary distinguishes documented accomplishments, recorded assignments, and historical work states.

## Language

**Reporting root**:
The Jira Research Project, Objective, or Epic that anchors a progress report's organizational boundary.

**Reporting scope**:
The set of descendant work items within a reporting root's hierarchy, including Sub-tasks. An ordinary issue link does not establish membership in this hierarchy.

**Reporting period**:
The interval for which a progress report describes activity and accomplishments, bounded by inclusive calendar dates in a stated timezone.

**Reporting cutoff**:
The temporal boundary separating a report's historical account from later evidence. It is the end of the reporting period, or the stated retrieval time for a provisional report covering the unfinished current day.

**Period-end state**:
The state of work at the end of the reporting period, which may differ from its current state.
_Avoid_: Current status, when referring to a historical state

**Outstanding work**:
Work that remained unresolved at the reporting cutoff, whether or not it had recorded activity during the reporting period.

**Planned work**:
Work with an explicit schedule or commitment recorded by the reporting cutoff, rather than work assumed to be planned because it exists in a backlog.

**Not completed as planned**:
Work that remained unresolved at the reporting cutoff despite a recorded commitment to finish by that time. This planning assessment is distinct from lifecycle state.
_Avoid_: Outstanding work as a synonym for a missed commitment

**Completed late**:
Work delivered after an established completion commitment but completed by the reporting cutoff. This planning assessment preserves the completed lifecycle state and differs from work still not completed as planned.

**Abandoned work**:
Work explicitly canceled or declined, which is distinct from a successful accomplishment or an unresolved commitment.
_Avoid_: Failed delivery as a synonym for cancellation

**Accomplishment**:
A delivered outcome supported by Jira evidence, which may represent only part of an unfinished work item.
_Avoid_: Ticket closure as a synonym for every accomplishment

**Documented contribution**:
Work attributed to a person by an explicit statement in Jira, rather than inferred solely from assignment or workflow activity. The statement supports recorded attribution, not independent verification of the work.
_Avoid_: Assignment, comment authorship, or status transition authorship as synonyms for contribution

**Assignment-based attribution**:
An association between a person and work based on assignment at the relevant accomplishment date or reporting cutoff, without evidence establishing that person's contribution.
