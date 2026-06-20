---
name: implement-headless-tools
description: Allows an agent to invoke client-side capabilities (e.g., browser APIs, local memory, app-specific actions) as first-class tools. Use when an agent needs to interact with the frontend environment or device capabilities directly.
---

# Implement Headless Tools

This skill enables agents to execute capabilities natively within the user's client environment (e.g., browser, desktop app) rather than relying exclusively on backend server tools. This approach bridges the gap between the agent's reasoning loop and local state such as geolocation, file pickers, local storage, or application-specific commands (like slide navigation).

## When to Use

- When the agent needs access to device APIs (e.g., `navigator.geolocation`, clipboard).
- When the agent must act on frontend state that is not synchronized to the server (e.g., current document selection, active slide).
- When privacy or latency concerns dictate that operations or memory should remain local to the user's device.
- When an application-specific sidecar agent needs to execute real-time actions on the client interface.

## CRITICAL: Core Principles

- **Separation of Definition and Implementation:** Define the tool interface (schema and description) so that both the server and the client share the same understanding. The server directs *what* to do, but only the client defines *how* to execute it locally.
- **In-Loop Reasoning:** Do not treat client-side capabilities as ad-hoc side channels. Expose them as first-class tools so the agent can discover and decide when to invoke them within its standard reasoning loop.
- **Security & Privacy:** Ensure operations that touch local memory or device capabilities are correctly sandboxed to the user environment, avoiding unnecessary round trips of sensitive data to the backend.

## Implementation Pattern (TypeScript/React)

The headless tool pattern typically involves two parts: a shared tool definition and a client-side implementation hook. While the general concept is framework-agnostic, the below demonstrates the pattern using typical LangChain JS primitives.

### 1. Define the Shared Tool
Define the tool with its name, description, and input schema. This definition will be known to both the reasoning agent and the client.

```typescript
// tools.ts
import { tool } from "langchain";
import { z } from "zod";

export const geolocationGet = tool({
  name: "geolocation_get",
  description: "Get the user's current location from the browser.",
  schema: z.object({}),
});
```

### 2. Implement the Tool on the Client
On the client side (e.g., a React application), attach the actual implementation logic that executes within the browser context and pass it to the streaming/hook interface.

```tsx
// App.tsx
import { useStream } from '@langchain/react';
// Import the shared tool definition
import { geolocationGet as geolocationGetDefinition } from './tools';

export function App() {
  const stream = useStream({
    // Provide other necessary configurations...
    tools: [
      // Attach the actual client-side implementation here
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

  return <div>{/* Your UI Components */}</div>;
}
```

## Best Practices and Caveats

- **User Permissions:** Remember that calling native browser APIs (like geolocation or file access) may trigger user permission prompts. Handle rejection scenarios gracefully.
- **State Management:** When using headless tools to manage local memory (e.g., IndexedDB), ensure the data schema aligns with what the agent expects so it can effectively read from and write to local state without server dependency.
- **Latency & Round Trips:** Prefer headless tools over backend alternatives for any operation that relies heavily on the client runtime, as it reduces unnecessary server round trips and serialization overhead.
