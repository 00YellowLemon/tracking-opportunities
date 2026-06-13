[ ](/)

Products

[LangSmith Platform ](/langsmith-platform)

[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6a1c6031b3db015796401c5b_LangSmith%20Engine_Icon_light%201.svg)EngineImprove
agents autonomously](/langsmith/engine)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c024180a65887312dd40_Frame%202147254707.svg)ObservabilitySee
exactly what your agents are
doing](/langsmith/observability)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c0247f235ca5583fa63b_Frame%202147255166.svg)EvaluationScore
and improve agent
performance](/langsmith/evaluation)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c024926f877c1de6e728_updated.svg)DeploymentShip
and scale agents in
production](/langsmith/deployment)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69baea024a5f7c2d229815b0_LangSmith%20Fleet_icon_light%20mode%203.svg)FleetAgents
for the whole company](/langsmith/fleet)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6a020888f9b2346912c07f41_sandboxes_light_mode%202.svg)SandboxesRun
agent-generated code safely](/langsmith/sandboxes)

Open Source Frameworks

[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c02453d869396317aaa3_updated-1.svg)deepagentsBuild
long-running agents for complex tasks](/deep-
agents)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c024409fcfc7e5b8f78f_Frame%202147254707-1.svg)langchainQuick
start agents with any model
provider](/langchain)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c024c2d98286a8fb058f_Frame%202147255166-1.svg)langgraphBuild
reliable agents with low-level control](/langgraph)

Learn

Resources

[Blog](/blog)[Customer Stories](/customers)[Guides](/resources)[Max
Agency](https://www.youtube.com/playlist?list=PLfaIDFEXuae3UwB1QGEjsRAr8BzCQss7s)

How-To

[LangChain
Academy](https://academy.langchain.com/)[YouTube](https://www.youtube.com/@LangChain)[Documentation](https://docs.langchain.com/)

Community

[LangSmith for
Startups](/startups)[Meetups](https://luma.com/langchain?k=c)[Community](/community)

[Docs](https://docs.langchain.com/)

Company

[About](/about)[Careers](/careers)[Partners](/langchain-partner-
network)[Events](/events)

[Pricing](/pricing)

[Try LangSmith ](https://smith.langchain.com/)[Get a demo ](/contact-sales)

[Try LangSmith ](https://smith.langchain.com/)

[Get a demo ](/contact-sales)

Open Source

LangChain

Agent Architecture

Deep Agents

# How to Build a Custom Agent Harness

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/69dcee60745f0e15b18ad4d5_sydney-runkle.png)

Sydney Runkle

June 3, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69ce2c533137196179bae949_Icon-7.svg)

6

min

[ Go back to blog](/blog)

Create agents

Share

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a2035adfcf624bfe1b4fd22_94%20\(1\).png)

## Key Takeaways

  * A harness is the scaffolding around the model that connects it to the real world.
  * How well a harness fits the task at hand determines how useful an agent is.
  * LangChain's `create_agent` is the easiest way to build a custom harness tailored to a given task.

‍

Building useful agents is largely about _customization:_ connecting your agent
to the right context, data, and environment(s) for the task at hand.

At its core, an agent is a model calling tools in a loop until it completes a
task and returns a result:

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a2030b364751b0b7b69bd2d_Screenshot%202026-05-26%20at%203.38.24%E2%80%AFPM.png)

You can also define an agent as:

> agent = model + harness

The harness is the scaffolding around the model that connects it to the real
world.

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a2030d9edf4c6cf5969df53_Screenshot%202026-06-01%20at%2010.22.02%E2%80%AFAM.png)

The remainder of this post assumes the following:

  1. An agent is only as good as the context provided to the model
  2. The job of a harness is to provide context to the model at every step

So, to build a useful agent, you need a harness that’s great at delivering the
right context for the given task to the model.

## The base harness

`create_agent` is LangChain's primitive for building a harness. Pass in a
model, tools, and a system prompt, and you have a working agent:



    from langchain.agents import create_agent

    agent = create_agent(
        model="anthropic:claude-sonnet-4-6",
        tools=tools,
        system_prompt="you are a helpful assistant..."
    )

Harnesses like [Deep
Agents](https://docs.langchain.com/oss/python/deepagents/overview) and the
[Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) come
pre-assembled with an opinionated middleware (explained below) stack: memory,
context management, sandboxing, and more. They're designed to get you to a
production-ready agent fast, and they work well for most cases. But many
agents need finer grained customization than these harnesses support: custom
prompting, business logic, guardrails, etc.

`create_agent` takes a different approach: it’s _purposefully minimalistic_.
Our philosophy is similar to that of [Pi](https://pi.dev/), a highly
configurable coding agent harness. `create_agent` just implements the core
agent loop, and it exposes **middleware** as a primitive for customization.

## Middleware: how you customize the harness

Middleware hooks into the agent loop at each step: before and after model
calls, before and after tool calls, at agent startup and teardown. Each piece
handles one concern and composes freely with any other:

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a203176250a89bbc45c8bf0_Screenshot%202026-05-26%20at%208.24.17%E2%80%AFAM.png)

Middleware allows you to add **capabilities** to your agent via a few levers
that often work together:

**Deterministic Logic.** Business logic, policy enforcement, dynamic agent
control — anything that needs to fire at a specific point in the loop. This
includes runtime control over the agent itself: swapping the model based on
task complexity, adjusting the prompt, and updating the agent’s message
history (during compaction, for example). The right place for anything that
can't (or shouldn't) live in a prompt.

**Tools.** Rather than registering tools directly on the agent, middleware can
handle the full lifecycle — setup, teardown, registration — and hand the agent
a clean set of tools to work with. This matters when tools have dependencies,
require initialization, or need to be torn down cleanly at the end of a run.
It also keeps tool configuration close to the logic that governs it, rather
than scattered across the agent definition.

**Custom state.** If your middleware needs to track state across hooks,
middleware can extend the agent’s state with custom properties. This enables
middleware to track state throughout execution (maintain counters, flags, or
other values that persist throughout agent runs) and share data between hooks.

**Stream handlers.** Middleware can intercept and transform the agent's output
stream — filtering events, injecting metadata, routing different event types
to different consumers. Useful when different parts of your stack need to
react to different things the agent does: a UI consuming token deltas, an
audit log capturing tool calls, a monitoring system tracking latency.

The beauty of middleware is that it:

  1. Enables customization at any point in the agent loop
  2. Bundles related logic in composable, sharable units of code

LangChain ships [prebuilt
middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-
in) for the most common patterns. Anything bespoke to your use case is one
[custom
middleware](https://docs.langchain.com/oss/python/langchain/middleware/custom)
away. Because each piece is isolated, the same middleware can be reused across
every agent in an organization so that new agents inherit battle-tested
behavior without rebuilding it.

## Harness capabilities

The job of a harness is to get the model the right context at the right time
for the given task.

The table below maps common capabilities to middleware that support them. Most
production agents end up using several together, depending on the agent’s
needs (is it long running? how complex are the tasks? how sensitive are the
agent’s actions?, etc):

Capability | Why it Matters | Middleware
---|---|---
Prevent context overflow | Long-running sessions accumulate message history fast. Without intervention, it overflows the context window. | SummarizationMiddleware, ContextEditingMiddleware
Access and update memory | Load relevant knowledge at startup, write it back at the end of a run. Lets the agent improve over time from real usage. | FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware
Take actions in an environment | A fixed toolset limits what an agent can do. Access to a filesystem and execution environment unlocks more creative solutions, often with greater token efficiency. | ShellToolMiddleware, FilesystemMiddleware, CodeInterpreterMiddleware
Delegate tasks | Subagents handle complex sub-tasks with clean context windows. A todo list tracks progress across a long run. | SubAgentMiddleware, AsyncSubAgentMiddleware, TodoListMiddleware
Handle transient failures | Models and tools fail unpredictably. Production agents need retry logic with backoff and fallbacks when a model is unavailable. | ToolRetryMiddleware, ModelRetryMiddleware, ModelFallbackMiddleware
Enforce policies | PII handling, compliance checks, approval gates — these need to fire on every call regardless of what the model does. They don't belong in a prompt. | PIIMiddleware, HumanInTheLoopMiddleware
Steer the agent | Full autonomy isn't always appropriate. Pause before consequential actions and wait for a human to approve, reject, or redirect. | HumanInTheLoopMiddleware
Control costs | Prompt caching reduces token spend on long-running tasks. Call limits prevent costs from accumulating unchecked. | ModelCallLimitMiddleware, ToolCallLimitMiddleware, PromptCachingMiddleware

See the full list of prebuilt middleware
[here](https://docs.langchain.com/oss/python/langchain/middleware/built-in).

## Task-harness fit

Task-harness fit is how well your harness matches the actual demands of the
task: the context it needs, the failures it'll encounter, the policies it must
enforce, the environment it operates in. A harness for a customer service
agent looks very different from one built for a long-running coding agent.

Every agent we build at LangChain, including our [GTM
agent](https://www.langchain.com/blog/how-we-built-langchains-gtm-agent),
[asynchronous coding agent](https://github.com/langchain-ai/open-swe), and our
[no-code agent builder](https://www.langchain.com/langsmith/fleet), is built
on `create_agent` with a middleware stack tailored to that agent’s mission.

The best agents aren't just built with capable models, they're built with
harnesses that tightly fit the task. The easiest way to build a custom harness
is with `create_agent`.

## References

### Get Started

  * [Quickstart: build your first agent with `create_agent`](https://docs.langchain.com/oss/python/langchain/quickstart)
  * [`create_agent` guide](https://docs.langchain.com/oss/python/langchain/agents)
  * [Middleware reference](https://docs.langchain.com/oss/python/langchain/middleware/built-in)
  * [Custom middleware guide](https://docs.langchain.com/oss/python/langchain/middleware/custom)
  * [Deep Agents: a production harness built on `create_agent`](https://docs.langchain.com/oss/python/deepagents/overview)

### Acknowledgements

Thanks to [@hwchase17](https://x.com/@hwchase17),
[@huntlovell](https://x.com/@huntlovell),
[@masondrxy](https://x.com/@masondrxy), and
[@Vtrivedy10](https://x.com/@Vtrivedy10) for their thoughtful review and
feedback.

### Related content

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a2995e66365247c159e8c18_dark-52%20characters%20max.png)

Open Source

#### The Missing Link Between Agents and Applications

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a0f01c040ee659bfdddd9ab_T04F8K3FZB5-U097E05JJAF-a7911e89a90d-512.jpeg)

Christian Bromann

June 10, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

6

min

[](/blog/agents-and-applications)

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a20e9ecceb33c3aa6859462_neutrality.png)

Agent Architecture

#### Why Model Neutrality Matters More Than Cloud Neutrality

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a20ea98c4a790a40caac819_Screenshot%202026-06-03%20at%208.01.36%E2%80%AFPM.png)

Neil Dahlke

June 4, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

7

min

[](/blog/model-neutrality)

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a21b18252c6946e4744edfb_92%20\(1\).png)

Open Source

Agent Architecture

LangGraph

#### Fault Tolerance in LangGraph: Retries, Timeouts, and Error Handlers

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a21b46ce3c7b10f36e622cc_image%20\(19\).png)

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/69dcee60745f0e15b18ad4d5_sydney-runkle.png)

Quanzheng Long

Sydney Runkle

June 4, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

7

min

[](/blog/fault-tolerance-in-langgraph)

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69ce01ea562f8cc223cabf25_Frame%202147254328.svg)

Sign up for our newsletter to stay up to date

Thank you! Your submission has been received!

Oops! Something went wrong while submitting the form.

### See what your agent is really doing

LangSmith, our agent engineering platform, helps developers debug every agent
decision, eval changes, and deploy in one click.

[Try LangSmith ](https://smith.langchain.com/)[Get a demo ](/contact-sales)

###### Products

[LangSmith Platform](/langsmith-platform)[LangSmith
Observability](/langsmith/observability)[LangSmith
Evaluation](/langsmith/evaluation)[LangSmith
Deployment](/langsmith/deployment)[LangSmith
Fleet](/langsmith/fleet)[LangSmith Sandboxes](/langsmith/sandboxes)[Deep
Agents](/deep-agents)[LangChain](/langchain)[LangGraph](/langgraph)

###### Resources

[Blog](/blog)[Customer Stories](/customers)[Guides](/resources)[LangChain
Academy](https://academy.langchain.com)[Community](/join-
community)[Changelog](https://changelog.langchain.com/)[Docs](https://docs.langchain.com/)[Support](https://support.langchain.com/)

###### Company

[About](/about)[Careers](/careers)[Partners](/langchain-partner-network)[Trust
Center](https://trust.langchain.com/)[Marketing
Assets](https://drive.google.com/drive/folders/1cc_Wdd8k7J5wUONBMvtfIZH_BaYvonym)

[Events](/events)

###### Sign up for our newsletter to stay up to date

Thank you! Your submission has been received!

Oops! Something went wrong while submitting the form.

[ ](https://www.linkedin.com/company/langchain/)[
](https://twitter.com/LangChain)[ ](https://www.youtube.com/@LangChain)

[All systems operational](https://status.smith.langchain.com/)

[Privacy policy](/privacy-policy)[Terms of service](/terms-of-service)
