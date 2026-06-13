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

LangSmith

# Give your agent its own computer

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a2208d9f4f51f9565792dae_Amy%20ru.jpeg)

Amy Ru

June 5, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69ce2c533137196179bae949_Icon-7.svg)

7

min

[ Go back to blog](/blog)

Create agents

Share

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a230182ec72c27d00c09ed6_Give%20Your%20Agents%20it%27s%20Own%20Computer.png)

LLMs can reason. But reasoning alone doesn't get much done.

Running code execution in an AI agent is harder than it looks. Your agent
needs a real computer (filesystem, shell, package manager, persistent state)
but handing it access to your infrastructure is dangerous.

Think about it this way: you use one laptop. You are n of one. But agents are
going to run millions of tasks, and each one needs its own computer to work
from. That's the infrastructure shift happening right now. Satya Nadella put
it plainly: "Every agent needs a computer." The question is what that computer
looks like, and how you give it to them safely.

LangSmith Sandboxes are our answer to that. Here's why it matters, and why
doing it yourself is harder than it sounds.

## What becomes possible when an agent has a computer

Think about what Cursor, Claude Code, or ChatGPT's code interpreter can do
that a plain chat interface can't. They don't just answer questions: they run
the code, see the error, fix it, run it again, and hand you something that
works. That feedback loop is what makes them useful.

That same loop is what separates a demo agent from a production agent. Once
your agent can execute, a whole category of work opens up:

  * A **coding assistant** that doesn't just suggest a fix: it applies the fix, runs your tests, and confirms nothing broke
  * A **data analyst** that pulls a CSV, runs Python against it, and hands you a formatted report
  * A **CI agent** that clones your repo, installs dependencies, runs the full test suite, and opens a PR (like [OpenSWE](https://github.com/langchain-ai/open-swe))
  * A **research agent** that browses, scrapes, synthesizes, and writes — not just searches
  * A **content pipeline** that generates, renders, and exports finished artifacts
  * An **RL or eval harness** that needs to spin up environments in parallel, run episodes at burst scale, and tear them down immediately — zero to thousands of sandboxes, then back to zero

The common thread: these agents need more than a token stream. They need a
place to _work_.

## Why you can't just hand your agent your laptop

The obvious next question is: why not just let the agent run code locally? Or
in a Docker container? Teams do this in early prototypes. It stops working in
production for two reasons.

**First: agents run untrusted code by definition.**

The code your agent executes might come from a model, a user prompt, a cloned
repo, or an installed package. You didn't write it. You can't fully vet it. In
September 2025, a self-replicating npm worm called [Shai-
Hulud](https://unit42.paloaltonetworks.com/npm-supply-chain-attack/)
backdoored 500+ packages — code that executed in preinstall before any
validation could run. A second wave in November hit 796 more packages and
25,000+ GitHub repos in hours. An agent that installs npm packages as part of
its workflow is exposed to exactly this.

**Second: containers aren 't enough.**

The common instinct is "just run it in Docker." Containers are great for
isolating known, vetted application code (i.e. a web server, a background
job). They're not designed for an agent that's installing arbitrary
dependencies, running model-generated scripts, and persisting state across a
long-running session. And critically: containers share a kernel with the host.
A kernel exploit reaches through them. [Copy Fail
(CVE-2026-31431)](https://www.bugcrowd.com/blog/what-we-know-about-copy-fail-
cve-2026-31431/) is a 732-byte Python script that roots every major Linux
distribution back to 2017 via the kernel crypto API. _AI tooling found it in
about an hour._

A container boundary is not an isolation boundary. For untrusted, model-
generated code, you need hardware-level separation.

## LangSmith Sandboxes: a computer for every agent

The mental model that helps here: a sandbox needs to be two things at once. It
needs the instant startup of a serverless function because you can't make an
agent wait two minutes for a VM to boot. And it needs the statefulness of a
full machine because agents aren't stateless request-handlers; they're mid-
session workers that install dependencies, edit files, and pick up where they
left off.

LangSmith Sandboxes are built for that model. Each one is a hardware-
virtualized microVM. Not a container, a full machine with its own kernel. The
agent gets:



    Agent
    └── its own computer
        ├── filesystem
        ├── shell
        ├── package manager
        ├── network access
        ├── code execution
        └── persistent state

It can install packages, run scripts, edit files, spin up a local server, and
keep working across a long session — all without touching your production
infrastructure or any other agent's sandbox. When the work is done, the
sandbox disappears.

You access it through the same LangSmith SDK and API key you already use:



    from langsmith import Client

    client = Client()
    sandbox = client.create_sandbox()

    # Give the agent a shell
    result = sandbox.run("pip install pandas && python analysis.py")
    print(result.stdout)

It just takes one call, and your agent has a computer.

There's also a less obvious benefit for teams running GPU workloads: when your
sandbox spins up instantly, your GPU doesn't idle waiting for CPU compute to
provision. Fast sandboxes are a GPU efficiency multiplier — a detail that
compounds quickly at scale.

## What you get beyond basic execution

A sandbox is more than a place to run code. The GA release ships a set of
primitives that make agent workflows production-ready:

**Snapshots and forks:** Capture a sandbox mid-session and boot new ones from
it. Forks use copy-on-write, so spinning up ten parallel branches costs
roughly the same as one. When your agent goes down the wrong path, restore and
try again, without rebuilding from scratch.

**Blueprints for pre-warmed environments:** Define a base image (your repo
cloned, your deps installed, your config in place) and boot sandboxes from it
in seconds instead of minutes.

**Service URLs:** If the agent starts a local web server — say, to preview a
generated report — you get an authenticated URL you can open in a browser or
share with a teammate. No port forwarding.

**Auth proxy:** Outbound requests from the sandbox flow through a proxy that
injects credentials at the network layer. Secrets never touch the agent
runtime.

**Creator-private by default:** Only the user who launched a sandbox (and
workspace admins) can access it. Share when you're ready.

## When to reach for Sandboxes

Sandboxes are the right layer when your agent needs to _do_ something, not
just _say_ something. Concretely:

  * Your agent generates code and you want it to verify that code runs before responding
  * You're building a coding assistant, CI agent, or data pipeline that operates on real files
  * You're running multi-step workflows where state needs to persist across tool calls
  * You need burst capacity (i.e. thousands of parallel environments for RL training or evals) that has to scale from zero in seconds
  * You're accepting any user-supplied input that could end up being executed

Sandboxes are overkill if your agent only calls APIs with fixed schemas and
never executes dynamic code. A retrieval agent that searches docs and returns
citations doesn't need one. An agent that writes and runs a Python script
does.

## How teams are using this today

At [monday.com](http://monday.com/), Sandboxes power their Sidekick AI
assistant, giving it a secure environment to write and run code for advanced
user workflows, including data analysis and multimedia generation.

> _" LangSmith Sandboxes are helping us make our Sidekick much more capable
> for monday.com users. With secure environments, Sidekick can write and run
> code, and use the results to create richer workflows, like running data
> analysis and generating multimedia."_

> — Omri Bruchim, AI Platform Group Manager, monday.com

## The shift worth paying attention to

For the last few years, making an agent more capable meant giving it better
tools: a search API, a calculator, a database connector. That's still true.
But the ceiling on what predefined tools can do is low.

The agents that will actually replace workflows (not just assist with them!)
are the ones that can pick up whatever tool they need, run it, see what
happened, and adapt. That's what having a computer makes possible. It's not an
infrastructure detail. It's the difference between an agent that can _think_
and an agent that can _act_.

You use one laptop. Your agents will each need their own. LangSmith Sandboxes
are how you give them one.

‍

**Get started:** [Try LangSmith Sandboxes](https://smith.langchain.com/) or
[read the docs](https://docs.langchain.com/langsmith/sandboxes).

‍

### Related content

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a2b60bb89294179fd4a62eb_plum-77%20characters%20max.png)

LangSmith

#### How to Choose the Right Sandbox for Your Agent

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/69dd2d3bf32d4fc06a289383_rahul-verma.png)

Rahul Verma

June 12, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

min

[](/blog/how-to-choose-the-right-sandbox-for-your-agent)

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a0f309a0e77b5e3544965e5_Lyft-customer-
support-blog.png)

Case Studies

LangGraph

LangSmith

Tutorials & How-Tos

#### How Lyft Built a Self-Serve AI Agent Platform for Customer Support with
LangGraph and LangSmith

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a0f35862276d228fb60ba48_akshay-
sharma.jpeg)

Akshay Sharma

May 27, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

10

min

[](/blog/lyft-built-a-self-serve-ai-agent-platform-for-customer-support-with-
langgraph-and-langsmith)

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a15d44fbcc56ddb5fa6ef30_mission-
control.png)

LangSmith

#### Mission Control: Operating Self-Hosted LangSmith on Kubernetes

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a15d9b4090cf7ce7d82ae27_BlogPostImage%201.png)

Gethin Dibben

May 26, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

6

min

[](/blog/mission-control-operating-self-hosted-langsmith-on-kubernetes)

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
