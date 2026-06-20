[ ](/)

Products

[LangSmith Platform ](/langsmith-platform)

Agent Improvement

[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6a1c6031b3db015796401c5b_LangSmith%20Engine_Icon_light%201.svg)EngineImprove
agents autonomously](/langsmith/engine)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c024180a65887312dd40_Frame%202147254707.svg)ObservabilitySee
exactly what your agents are
doing](/langsmith/observability)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c0247f235ca5583fa63b_Frame%202147255166.svg)EvaluationScore
and improve agent performance](/langsmith/evaluation)

Agent Infrastructure

[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c024926f877c1de6e728_updated.svg)DeploymentShip
and scale agents in
production](/langsmith/deployment)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6a020888f9b2346912c07f41_sandboxes_light_mode%202.svg)SandboxesRun
agent-generated code safely](/langsmith/sandboxes)

No-Code Agents

[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69baea024a5f7c2d229815b0_LangSmith%20Fleet_icon_light%20mode%203.svg)FleetAgents
for the whole company](/langsmith/fleet)

Open Source Frameworks

[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c024409fcfc7e5b8f78f_Frame%202147254707-1.svg)langchainQuick
start agents with any model
provider](/langchain)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c024c2d98286a8fb058f_Frame%202147255166-1.svg)langgraphBuild
reliable agents with low-level
control](/langgraph)[![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/6989c02453d869396317aaa3_updated-1.svg)deepagentsBuild
long-running agents for complex tasks](/deep-agents)

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

# The Missing Link Between Agents and Applications

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a0f01c040ee659bfdddd9ab_T04F8K3FZB5-U097E05JJAF-a7911e89a90d-512.jpeg)

Christian Bromann

June 10, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69ce2c533137196179bae949_Icon-7.svg)

6

min

[ Go back to blog](/blog)

Create agents

Share

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a2995e66365247c159e8c18_dark-52%20characters%20max.png)

## Key Takeaways

  * **Most agent tools only see the backend.** Browsers, apps, and devices contain valuable state and capabilities that traditional server-side tools cannot directly access.
  * **Headless tools bring client-side capabilities into the agent loop.** Agents can invoke browser APIs, local memory, and application-specific actions as first-class tools while preserving structured inputs and outputs.
  * **Keeping execution on the client improves both UX and privacy.** Agents can interact with the user's environment directly, reducing round trips and allowing sensitive data to remain local by default.

‍

** _TL;DR: Most agent tools run on the server, which means agents can call
APIs but not interact with the browser, app state, or device capabilities
where users actually work. With headless tools in LangChain we close this gap
by letting agents invoke client-side capabilities like geolocation, clipboard
access, local memory, and in-app actions as first-class tools. That makes
agents more useful, more private, and better aligned with real application
behavior._**

Today's agents are increasingly capable, but many of the capabilities users
care about live in the client runtime rather than on the server. Browsers and
applications own things like local state, user selections, device APIs, and
application-specific actions that are often unavailable through backend
systems. As a result, agents can reason about what should happen next but
still struggle to act on the environment where the user is actually working.

One reason for this gap is that most agent tools execute on the server. When a
model decides to use a tool, the agent runs it in-process or delegates it to
an external service such as an MCP server, then feeds the result back into the
reasoning loop. This works well for APIs, databases, and backend systems, but
it has clear limitations:

  * It cannot directly access browser-only or device-only APIs.
  * It cannot act on frontend state that has never been synchronized to the server.
  * It often forces privacy-sensitive data to leave the device.
  * It introduces unnecessary round trips for actions that are inherently local.

The browser is where many high-value agent actions actually happen: reading
local application state, acting on the current UI, and using device
capabilities without shipping that data to a backend first. Desktop apps
expose the same pattern through local files, native integrations, and session-
specific state. If your agent cannot reach that runtime, it stays good at
backend workflows but weak at the interactions users actually experience.

Imagine you are building a sidecar agent for Figma, Google Slides, or a rich-
text editor. The agent can reason about the user's request on the server, but
the document model, selection state, and editing commands all live in the
client. A server-side tool cannot insert text at the cursor, reformat the
selected object, or jump to the active slide, because those actions belong to
the application runtime, not the backend API. Today, teams usually bridge this
with an ad-hoc UI bridge: serialize some client state to the server, get a
response back, then imperatively patch the client. It works, but it is
fragile, hard to compose, and invisible to the model's reasoning loop.

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a29971f331e51d15edef8fd_headless-tools-
demo.gif)

_Let your agent access memory or the geolocation API directly from the users
browser._

‍

That is the problem [headless
tools](https://docs.langchain.com/oss/python/langchain/frontend/headless-
tools) solve in LangChain.

## What headless tools change

A headless tool looks like any other tool to the model: it has a name, a
description, and a set of expected inputs. The model decides when to call it,
just like any other tool. The difference is what happens next.

Instead of the server running the tool itself, it sends the tool call to the
client: the user's browser, desktop app, or whatever environment actually has
the capability. The client runs the tool locally and sends the result back,
and the agent picks up where it left off.

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a2997e2ba2469142d2ecb78_1.png)

While this sounds like a small implementation detail at first, it actually
changes what kinds of systems an agent can reliably control.

The model never needs to know where the tool runs. It sees a tool, decides to
use it, and gets a result. But behind the scenes, the server and the client
are coordinating: the server knows _what_ the agent wants to do, and the
client knows _how_ to do it. That separation is the core idea.

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a299822df8f9322bf816b73_2.png)

You could wire this up manually, call
`navigator.geolocation.getCurrentPosition()` from your React app and send the
result to the agent. But then the model has no way to discover or decide when
to invoke that capability. It lives outside the reasoning loop as an ad-hoc
side channel. Headless tools put client-side actions inside the agent's
reasoning loop, not alongside it.

## Why this matters

The benefit is not just "browser access." Imagine an agent helping you work
through a slide deck: it should be able to jump to the active slide, read
local context, and update the presentation in place without shipping the whole
session to a backend. Headless tools make that kind of interaction possible by
exposing client-side capabilities as real tools inside the agent loop.

Some operations are impossible to emulate correctly on the backend.
Geolocation is the obvious example — the browser owns permission prompts and
device signals. Clipboard access, canvas rendering, file pickers, and live UI
navigation all depend on the active client environment. A standard tool can
approximate these through a backend service. A headless tool can call the real
thing.

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a2998ab21667aea15b1199a_3.png)

But headless tools are not just for browser APIs. They are a general mechanism
for giving agents safe access to application-native actions. For example:
[`slidev-agent`](https://github.com/christian-bromann/slidev-agent) , a plugin
for the popular [Slidev](https://sli.dev/) presentation framework, uses a
headless tool to navigate to a specific slide in the user's active
presentation. This is not a data retrieval problem or a server automation
problem.

This pattern also changes privacy tradeoffs. Agent memory does not always
belong in a centralized backend. With a headless tool backed by a browser
storage like IndexedDB, memory can stay local by default — durable, low-
latency, and naturally scoped to that user and browser — without turning
recall into a server-side data management problem.

## How it works in code

In TypeScript, the separation between definition and implementation is
especially clean. You define the tool once, attach the implementation with
`.implement(...)`, and pass the implementation into the [frontend streaming
hook](https://reference.langchain.com/javascript/langchain-react/useStream).
The server and client share the same schema, but only the client loads the
browser-specific execution logic.



    // tools.ts
    import { tool } from "langchain";

    export const geolocationGet = tool({
      name: "geolocation_get",
      description: "Get the user's current location from the browser.",
      schema: z.object({}),
    });


    // App.tsx
    import { useStream } from '@langchain/react';

    // shared tools definition
    import { geolocationGet as geolocationGetDefinition } from './tools';

    export function App() {
      const stream = useStream({
        // ...
        tools: [
          // actual tool implementation on the client side
          geolocationGetDefinition.implement(async () => {
            const position = await new Promise<GeolocationPosition>((resolve, reject) =>
              navigator.geolocation.getCurrentPosition(resolve, reject),
            );

            return {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
              accuracy: position.coords.accuracy,
            };
          }),
        ],
      });

      return <div> ... </div>;
    }

Check out a live demo in our [LangChain
docs](https://docs.langchain.com/oss/javascript/langchain/frontend/headless-
tools), combining browser-local memory with geolocation and optional human
approval.

## Summary

Standard tools gave agents access to backend systems. Headless tools give them
access to where users actually work.

Users do not live on your backend. They live in browsers, apps, and devices,
where many of the most valuable agent interactions happen. Headless tools make
those interactions available while preserving typed schemas, explicit
capabilities, structured outputs, and reviewability, allowing agents to use
tools that are native to the user, not just convenient for the server.

Get started with headless tools in [LangChain
Python](https://docs.langchain.com/oss/python/langchain/frontend/headless-
tools) or [LangChain
JS](https://docs.langchain.com/oss/javascript/langchain/frontend/headless-
tools).

Thanks to [@huntlovell](https://x.com/@huntlovell),
[@colifran_](https://x.com/@colifran_), and
[@sydneyrunkle](https://x.com/@sydneyrunkle) for their thoughtful review and
feedback.

### Related content

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/6a317b118693f5be4a8e220f_97.png)

Deep Agents

Open Source

Agent Architecture

#### The Art of Loop Engineering

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/69dcee60745f0e15b18ad4d5_sydney-runkle.png)

Sydney Runkle

June 16, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

7

min

[](/blog/the-art-of-loop-engineering)

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
files.com/65c81e88c254bb0f97633a71/6a2035adfcf624bfe1b4fd22_94%20\(1\).png)

Open Source

LangChain

Agent Architecture

Deep Agents

#### How to Build a Custom Agent Harness

![](https://cdn.prod.website-
files.com/65c81e88c254bb0f97633a71/69dcee60745f0e15b18ad4d5_sydney-runkle.png)

Sydney Runkle

June 3, 2026

![](https://cdn.prod.website-
files.com/65b8cd72835ceeacd4449a53/69cd1fd0002272ce39bf1241_Icon-6.svg)

6

min

[](/blog/how-to-build-a-custom-agent-harness)

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

[Blog](/blog)[Customer
Stories](/customers)[Guides](/resources)[Community](/join-
community)[Changelog](https://changelog.langchain.com/)[Docs](https://docs.langchain.com/)[Support](https://support.langchain.com/)[LangChain
Academy](https://academy.langchain.com)

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
