# Evolving Agents: Internal AI Agent Setup

*   **Introduction and Context**
    *   Presentation by Ayush, founder of "Answer This" (a company building AI agents for evidence-based scientific workflows).
    *   The focus of the talk is on how they utilize AI agents internally and how other companies can replicate their setup.

*   **Company Scale and Agent Impact**
    *   The company reached over $2 million in Annual Recurring Revenue (ARR) operating primarily with only two full-time employees (the founders), supplemented by a few contractors for design and outbound tasks.
    *   A massive driver for this efficiency is an internal "AI ops agent" that handles work typically consuming founder time.
    *   The AI agent processes over 100 emails daily and has successfully closed more than 400 customer support tickets.
    *   It automatically handles Customer Relationship Management (CRM) updates following meetings.
    *   It aggregates user feedback across multiple communication channels.
    *   The agent serves as a query interface for the founders, allowing them to instantly ask questions about the business (e.g., lead statuses, open customer issues) without navigating multiple different applications.

*   **Core Feature: Self-Extension**
    *   The most crucial capability of the agent is that it is not limited to a hardcoded, fixed set of tasks.
    *   When the agent encounters a repeated task it lacks the capability to perform, it requests a coding sub-agent to construct a new tool for it.
    *   Once built, this new tool becomes permanent and remains available for all future sessions and tasks.

*   **Architecture for Replication**
    *   The foundational setup involves wrapping a Claude Code Command Line Interface (CLI) in Python.
    *   Incoming messages from platforms like Slack, email, and other channels are routed into a task queue.
    *   The agent picks up tasks from this queue and processes them iteratively.
    *   A thin harness is recommended; Claude Code is highlighted as exceptionally effective because it inherently knows how to inspect files, run terminal commands, and use CLIs.

*   **Teaching Proprietary Business Logic**
    *   To give the agent context about proprietary business logic, it is provided with a read-only copy of both the company's database and its codebase.
    *   A cron job is set up to provide the agent with an updated version of the database and codebase every time a new software release is deployed.
    *   This enables the agent to independently read the codebase to answer complex customer support queries, such as understanding internal subscription logic or locating specific elements within the app.

*   **Mechanics of Self-Evolution**
    *   **Access to Startup Tools:** The agent is given CLI access to standard everyday startup tools (e.g., Intercom, Fathom, Stripe).
    *   **Access to a Coding Agent:** The primary agent is given CLI access to a general coding agent, effectively allowing it to edit its own agent code.
    *   These two components mean the agent can literally code a new tool into existence to handle unprecedented tasks.
    *   The internal agent evolved from a basic skeleton to a comprehensive system featuring over 45 custom CLIs it built itself.
    *   Example: When tasked with monitoring landing pages to ensure they stayed up for ads, the agent autonomously created a cron job to handle the monitoring.

*   **Editable Personality and Memory**
    *   The agent requires an editable "personality" or memory system to adapt to feedback.
    *   This is implemented using an `instructions.md` file that is loaded on every single agent turn, and crucially, the agent is granted permission to edit this file.
    *   Founders can give the agent feedback just like an employee. The agent updates its `instructions.md` file based on this feedback, appending the learned behavior to all future runs.
    *   Example: A non-technical co-founder noticed a recurring class of customer support mistakes. By directly messaging the agent in Slack with feedback, the agent updated its instruction set and tool logic, completely eliminating that category of errors going forward.

*   **The Three Types of Memory Needed**
    *   **Factual Memory:** The read-only codebase and database, which represent how operations mechanically function within the startup.
    *   **Behavioral Memory:** The rules and feedback taught to the agent by humans, stored and managed via the editable `instructions.md` file.
    *   **Procedural Memory:** The regular, repeated tasks that are permanently encoded into the tools the agent autonomously creates.

*   **Summary Checklist for Building the Agent**
    *   Use a coding-capable CLI (like Claude Code) as the main agent harness.
    *   Provide the agent with read-only access to the codebase.
    *   Supply basic CLIs for interfacing with external tools.
    *   Provide a coding agent as an accessible CLI tool.
    *   Implement an instruction file that is loaded and can be edited on every turn.
    *   Connect the system to communication channels (e.g., Slack, email) through SSH to operationalize it for the business.