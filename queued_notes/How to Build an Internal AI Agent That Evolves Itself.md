Source Video: https://www.youtube.com/watch?v=DGD9b8K42lk

* The speaker, Ayush, is the founder of Answer This, a company that builds AI agents for evidence-based scientific workflows.
* Ayush shares insights on how their team uses AI agents internally and provides a blueprint for replicating their setup.
* Answer This has achieved over $2 million in Annual Recurring Revenue (ARR) with primarily two full-time employees (Ayush and his co-founder).
* They employ two or three contractors for specific tasks like design and outbound marketing.
* A significant factor in their high output-to-employee ratio is an internal AI operations agent that automates work normally consuming founder time.
* This internal AI agent processes more than 100 emails per day.
* The agent has successfully closed over 400 customer support tickets.
* It automatically handles CRM (Customer Relationship Management) updates following meetings.
* It actively collects user feedback across various communication channels.
* The agent provides assistance with general customer support inquiries.
* Beyond task execution, the agent functions as a queryable interface for the business, allowing founders to ask questions at any time.
* Founders can ask the agent about the status of specific leads.
* Founders can query the agent about open issues for a particular customer.
* This capability makes business data instantly accessible, eliminating the previous need to navigate multiple different applications to find answers.
* The most critical feature of the agent is not its ability to perform a fixed set of tasks, but its capacity to be self-extending.
* When the agent encounters a repeated task it does not know how to perform yet, it prompts a coding sub-agent to construct a tool to handle that task.
* Once created, this new tool becomes a permanent part of the agent's capabilities and is available for use in all future sessions.
* The architectural setup for replicating this system begins with a Claude code CLI (Command Line Interface).
* This CLI is wrapped in Python.
* New messages originating from Slack, email, and other communication channels are routed into a task queue within this Python wrapper.
* The agent picks up these queued tasks and works through them in an iterative manner.
* A thin harness is essential for this architecture (a concept mentioned by other speakers Pete, Gary, and Tom).
* Cloud Code is highly effective in this setup because it inherently knows how to inspect files, execute commands, and utilize CLIs.
* To provide the agent with proprietary business logic, it is given a read-only copy of both the company's database and code base.
* A cron job is configured to provide the agent with an updated version of the database and code base every time a new release is deployed.
* Consequently, when a customer support query involves specific business logic, the agent can read the code base to determine the answer.
* The agent can use the code base to understand complex subscription logic.
* The agent can locate where specific features or components are located inside the application by referencing the code base.
* The agent's ability to self-evolve relies on two crucial components.
* First, all the standard tools used by the startup (e.g., Intercom, Fathom, Stripe) are provided to the main agent as CLIs.
* Second, the main agent also has access to a general coding agent, functioning as another CLI.
* This coding agent CLI has the permission and capability to edit the main agent's own code.
* As a result, when asked to perform an unfamiliar task, the agent uses the coding agent CLI to write the necessary code, thereby coding a new tool into existence to handle the request.
* The agent has evolved from a basic skeleton into a comprehensive system with over 45 custom CLIs that it authored itself.
* For example, when the team wanted to monitor landing pages to ensure they were always online for advertising purposes, they simply instructed the agent to do so.
* The agent responded by creating a cron job from scratch that continuously monitors the landing pages.
* Another vital requirement for this type of internal agent is an editable personality or memory.
* This editable memory is implemented using an `instructions.md` file.
* This `instructions.md` file is loaded into the agent's context on every single turn or interaction.
* Crucially, the agent has the ability to edit this `instructions.md` file.
* This editing capability allows the founders to provide feedback to the agent, much like giving feedback to a human employee.
* When given feedback, the agent updates its own `instructions.md` file, which is then appended to and dictates its behavior in the next run.
* A practical example of this editable memory in action occurred during customer support operations.
* When the agent was initially deployed for customer support, Ayush's non-technical co-founder, Ryan, noticed a recurring class of mistakes in the agent's responses.
* Instead of filing a bug ticket or asking for a code change, Ryan messaged the agent directly in Slack.
* Ryan explained what was wrong with the agent's support responses.
* The agent then autonomously updated its own instruction set and tool links based on that feedback.
* Following that update, that specific entire class of support mistakes ceased to happen.
* The broader lesson derived from this experience is that an internal agent requires three distinct types of memories to function effectively.
* 1. Factual Memory: This consists of the code base and database, providing the agent with knowledge of how things work operationally within the startup.
* 2. Behavioral Memory: This represents what is explicitly taught to the agent through instruction and feedback, captured within the `instructions.md` file.
* 3. Procedural Memory: This is the memory of regular tasks that are performed, which is encoded directly into the tools that the agent self-creates.
* To replicate this entire agent setup, one can use Claude code or any other coding-capable CLI as the main agent harness.
* Grant the agent read-only access to the company code base.
* Provide the agent with basic CLIs for essential startup tools.
* Provide the agent with a coding agent as an additional CLI.
* Load an instruction file (`instructions.md`) that is editable by the agent on every turn.
* Connect the agent harness to communication channels like Slack or email via SSH.
* Implementing these steps will yield a self-evolving AI agent ready for internal business use.