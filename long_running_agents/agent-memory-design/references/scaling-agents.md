# Scaling Long-Running Autonomous Coding

**Source:** [Scaling long-running autonomous coding (Cursor Blog)](https://cursor.com/blog/scaling-agents)

*   **Avoid Flat Hierarchies & Locks:** Giving all agents equal status and using file-locking or optimistic concurrency creates severe bottlenecks. Agents become risk-averse and avoid difficult end-to-end implementation.
*   **Role Separation (Planners vs. Workers):**
    *   **Planners:** Continuously explore the codebase, break down work, and create tasks. Planning can be recursive (spawning sub-planners).
    *   **Workers:** Focus entirely on completing assigned tasks without worrying about the big picture or coordinating with other workers.
*   **Cycles and Fresh Starts:** At the end of a work cycle, a judge agent should determine whether to continue. Starting the next iteration fresh helps combat drift, tunnel vision, and agents running for too long.
*   **Match Models to Roles:** Different foundation models excel at different tasks. Some are better at high-level planning and maintaining focus, while others excel at raw, localized coding.
*   **Simplicity in Coordination:** Avoid over-engineering organizational designs (e.g., dedicated "integrator" agents for conflict resolution). Worker agents are often capable of handling conflicts themselves. The harness and prompts matter more than complex coordination structures.
