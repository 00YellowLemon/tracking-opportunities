# How to Give AI Agents Enough Context to Be Useful

**Source:** [https://www.youtube.com/watch?v=1egwM88T3C0](https://www.youtube.com/watch?v=1egwM88T3C0)

* Sachin from Skyvern introduces the topic of context in AI, framing it with the idea that "context is all you need" or the phrase "stop the slop shop".
* He provides background on Skyvern, explaining it is an open-source company that primarily helps healthcare companies automate manual browser tasks.
* Skyvern has scaled past a 2 million run rate.
* Sachin mentions he functions as a Product Manager (PM), while also handling marketing, sales, and customer support entirely on his own.
* He attributes his ability to manage all these roles to the daily help he receives from various AI agents.
* The specific tasks his AI agents handle include writing Product Requirement Documents (PRDs), managing SEO, conducting content marketing, providing customer support, and fixing minor bugs.
* A major reason AI agents produce "slop" (poor quality output) is because, similar to new employees, they lack the necessary business context to perform their tasks well, despite their willingness to follow instructions.
* The solution to improving agent effectiveness involves providing good instructions, giving them proper context, and allowing them to critique their own work.
* Good context encompasses everything about a business, including access to emails, Slack messages, Notion documentation, and customer call recordings.
* Access to these resources allows agents to correlate specific customer issues with particular product features.
* Giving agents access to a company database can even enable them to look up specific runs or failures a customer experienced to accurately diagnose problems.
* Remote companies have an "unfair advantage" in building this context because communication is inherently recorded (e.g., via call recordings or Slack messages).
* In-person companies often lose context because communication is spoken and unrecorded.
* Sachin emphasizes that modern tools serve as a company's knowledge base, and anything not recorded is not saved, requiring companies to restructure to capture this information.
* He introduces two specific use cases/skills of AI at Skyvern that help them move faster.
* **Skill 1: Writing a PRD (Product Requirements Document)**
  * The instructions given to the agent for this skill are intentionally vague to allow it freedom in execution.
  * The agent begins by searching through all call recordings for the specific topic needed for the spec.
  * It then searches Slack for any communication related to the topic.
  * It searches Notion and customer communications to gather evidence.
  * The agent drafts an initial document that is grounded in this collected evidence and is concise.
  * Sub-agents then perform an adversarial review of the first draft, reading through the initial set of comments in the document.
  * The draft goes through a prioritization framework (Skyvern uses Rice, but any framework works) to remove junk requirements that the AI initially thought were important but aren't.
  * Initially, the team called the output "slop," but after tuning, it became useful enough that team members began using it to draft features.
  * An example provided involved an issue with CAPTCHA solvers in February. Sachin wanted a strategy to deal with customer complaints, and the agent successfully found and linked specific call recordings so engineers could review them directly.
* **Skill 2: Content Marketing**
  * Every morning, Sachin receives an email with five post ideas based on his last 20 internal and external customer call recordings.
  * The agent categorizes topics into buckets such as recurring pain points, contrarian observations, and content likely to perform well on social media.
  * It drafts five posts total—one for Twitter and one for LinkedIn for each of the five different topics.
  * The content is run through a DAI advisor (they use Pangram) to remove "sloppy" words and make the content feel more appropriate for platforms like LinkedIn.
  * The agent attempts to include a meme because funny content performs better.
  * The final drafts are sent to Sachin via email for review and publication.
  * This process enabled Sachin to publish five times a week, which he previously didn't have time to do.
  * A specific success story occurred on a Friday when a post about an insurance agency using their product for carrier portal automation (auto-generated from a customer requirement) led to a lead from someone in his network.
* Sachin reiterates that remote companies are automatically better positioned to use these tools, while in-person companies need to change their workflows.
* To adapt, Skyvern implemented a policy banning Direct Messages (DMs) within the company.
* Everyone at Skyvern must use public office channels to ask questions, which benefits all future hires by preserving that knowledge.
* Every call, whether internal, external, or even one-on-ones between co-founders, is recorded.
* Agents are given access to everything, and every employee is given access to an agent.
* When two new salespeople were hired, they were required to use this system. Though they initially struggled in the first hour, they quickly adapted.