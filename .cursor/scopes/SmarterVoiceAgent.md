# Spec: Smarter Voice Agent with LLM-based Intent Detection and CrewAI Delegation

## Purpose & User Problem
- Make the voice agent more flexible and accurate in detecting coloring sheet requests by leveraging LLM reasoning instead of static keyword matching.
- Enable the voice agent to delegate tasks (e.g., content filtering, subject extraction, prompt structuring) to specialized agents (summarizer, designer) using CrewAI's delegation features.

## Success Criteria
- The voice agent uses an LLM (OpenAI, with future support for local models) to determine if a user is requesting a coloring sheet.
- If the LLM is uncertain, the agent asks the user for clarification.
- The agent can delegate tasks to the summarizer and designer agents as needed, based on the nature of the request.
- Delegation logic and LLM provider are configurable (e.g., via YAML or environment variables).
- The system remains responsive (async calls are acceptable).

## Scope & Constraints
- Only the coloring sheet request detection and delegation logic are affected in this update.
- The agent should determine when to delegate to the summarizer and designer.
- Use OpenAI as the LLM provider initially, but design for easy switching to a local model later.
- Delegation and LLM provider should be configurable.
- No hardcoded agent configurations.

## Technical Considerations
- Use CrewAI's delegation features for agent orchestration.
- Document agent roles and communication protocols in code comments.
- Avoid hardcoding; use config files or environment variables for agent setup.
- Ensure async LLM calls are handled properly.

## Out of Scope
- No changes to unrelated parts of the system.
- No UI changes unless required for agent communication.

---

**Review this Spec and let me know if it captures your intent or if any changes are needed. Type 'GO!' when ready to proceed with implementation.** 