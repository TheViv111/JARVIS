"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import AppShell from "@/components/layout/AppShell";

type Role = "user" | "assistant";

interface Message {
  id: string;
  role: Role;
  content: string;
  time: string;
  meta?: {
    runId: string;
    risk: string;
    requiresApproval: boolean;
    providers: Record<string, string>;
    plan: string[];
  };
}

interface ExecuteIntentResponse {
  run_id: string;
  plan: string[];
  requires_approval: boolean;
  risk: string;
  assistant_output: string;
  providers: Record<string, string>;
}

const quickActions = [
  { label: "Check runtime health", prompt: "Check runtime health and summarize status." },
  { label: "Summarize tasks", prompt: "Summarize pending tasks from my recent context." },
  { label: "Plan my day", prompt: "Create a focused day plan with top 3 priorities." },
  { label: "Review risks", prompt: "Tell me any risky actions that would require approval." },
];

const API_BASE = process.env.NEXT_PUBLIC_RUNTIME_API_URL ?? "http://127.0.0.1:7777";

function nowLabel() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function makeSessionId() {
  return `web-${Date.now().toString(36)}`;
}

export default function CommandCenter() {
  const [sessionId, setSessionId] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [pending, setPending] = useState(false);
  const [showActivity, setShowActivity] = useState(true);

  const messageCount = messages.length;
  const lastAssistant = useMemo(
    () => [...messages].reverse().find((m) => m.role === "assistant"),
    [messages],
  );

  useEffect(() => {
    setSessionId(makeSessionId());
  }, []);

  async function submitPrompt(text: string) {
    const trimmed = text.trim();
    if (!trimmed || pending) return;

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: trimmed,
      time: nowLabel(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setPending(true);

    try {
      const resp = await fetch(`${API_BASE}/v1/intent/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId || makeSessionId(),
          input: trimmed,
          modality: "text",
          context: { source: "control-center" },
          prefer_cloud: true,
          speak_response: false,
        }),
      });

      if (!resp.ok) {
        let detail = `Request failed (${resp.status})`;
        try {
          const err = await resp.json();
          detail = err.detail ?? detail;
        } catch {
          // keep fallback detail
        }
        throw new Error(detail);
      }

      const data: ExecuteIntentResponse = await resp.json();
      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: data.assistant_output,
        time: nowLabel(),
        meta: {
          runId: data.run_id,
          risk: data.risk,
          requiresApproval: data.requires_approval,
          providers: data.providers ?? {},
          plan: data.plan ?? [],
        },
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: `Runtime request failed: ${message}`,
          time: nowLabel(),
        },
      ]);
    } finally {
      setPending(false);
    }
  }

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    void submitPrompt(input);
  }

  function resetChat() {
    setMessages([]);
    setInput("");
    setSessionId(makeSessionId());
  }

  return (
    <AppShell>
      <div className="flex h-[calc(100vh-4rem)]">
        <div className="flex-1 flex flex-col">
          <div className="px-6 pt-5 pb-3 border-b border-steel-dark bg-charcoal/40">
            <div className="flex items-center justify-between gap-4">
              <div>
                <h1 className="font-orbitron text-lg">Command Center</h1>
                <p className="text-xs text-text-muted mt-1">Session: {sessionId || "starting..."}</p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={resetChat}
                  className="px-3 py-2 rounded-lg text-xs font-medium bg-gunmetal border border-steel-dark text-text-secondary hover:text-cyan-glow hover:border-cyan-glow/30 transition-all"
                >
                  New Chat
                </button>
                {!showActivity && (
                  <button
                    onClick={() => setShowActivity(true)}
                    className="px-3 py-2 rounded-lg text-xs font-medium bg-gunmetal border border-steel-dark text-text-secondary hover:text-cyan-glow hover:border-cyan-glow/30 transition-all"
                  >
                    Show Activity
                  </button>
                )}
              </div>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4">
            {messages.length === 0 && (
              <div className="h-full flex items-center justify-center">
                <div className="max-w-lg text-center bg-charcoal border border-steel-dark rounded-2xl p-6">
                  <h2 className="font-orbitron text-lg mb-2">JARVIS is ready</h2>
                  <p className="text-sm text-text-secondary">
                    No hardcoded chat history. Start a new conversation and responses will come from your runtime API.
                  </p>
                </div>
              </div>
            )}

            {messages.map((msg) => (
              <div key={msg.id} className={`flex items-start gap-3 ${msg.role === "user" ? "justify-end" : ""}`}>
                {msg.role === "assistant" && (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-glow to-cyan-teal flex items-center justify-center border-2 avatar-glow shrink-0" style={{ borderColor: "rgba(0, 200, 232, 0.3)" }}>
                    <svg className="w-4 h-4 text-deep-space" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
                    </svg>
                  </div>
                )}

                <div className={`flex flex-col ${msg.role === "user" ? "items-end" : ""} max-w-[75%]`}>
                  <div
                    className={
                      msg.role === "user"
                        ? "px-4 py-3 rounded-2xl rounded-tr-sm border border-cyan-glow/20"
                        : "px-4 py-3 bg-charcoal border border-steel-dark rounded-2xl rounded-tl-sm"
                    }
                    style={
                      msg.role === "user"
                        ? { background: "linear-gradient(135deg, #1e1e24 0%, #141418 100%)" }
                        : undefined
                    }
                  >
                    <p className="text-[15px] leading-relaxed">{msg.content}</p>

                    {msg.meta && (
                      <div className="mt-3 bg-gunmetal border border-steel-dark rounded-lg p-3 text-xs text-text-secondary space-y-1">
                        <p>
                          <span className="text-text-muted">run:</span> {msg.meta.runId}
                        </p>
                        <p>
                          <span className="text-text-muted">risk:</span> {msg.meta.risk}
                          {msg.meta.requiresApproval ? " (approval required)" : ""}
                        </p>
                        <p>
                          <span className="text-text-muted">providers:</span>{" "}
                          {Object.entries(msg.meta.providers)
                            .map(([k, v]) => `${k}=${v}`)
                            .join(", ") || "n/a"}
                        </p>
                        <p>
                          <span className="text-text-muted">plan:</span> {msg.meta.plan.join(" -> ") || "n/a"}
                        </p>
                      </div>
                    )}
                  </div>
                  <span className={`text-xs text-text-muted mt-1 ${msg.role === "user" ? "mr-2" : "ml-2"}`}>{msg.time}</span>
                </div>
              </div>
            ))}

            {pending && (
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-glow to-cyan-teal flex items-center justify-center border-2 avatar-glow shrink-0" style={{ borderColor: "rgba(0, 200, 232, 0.3)" }}>
                  <svg className="w-4 h-4 text-deep-space" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
                  </svg>
                </div>
                <div className="bg-charcoal border border-steel-dark rounded-2xl rounded-tl-sm px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="typing-dot w-2 h-2 rounded-full bg-cyan-glow" />
                    <div className="typing-dot w-2 h-2 rounded-full bg-cyan-glow" />
                    <div className="typing-dot w-2 h-2 rounded-full bg-cyan-glow" />
                    <span className="text-sm text-text-secondary italic ml-2">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="border-t border-steel-dark" style={{ background: "linear-gradient(to top, #0a0a0f 0%, transparent 100%)" }}>
            <div className="px-6 pt-4 pb-6">
              <form onSubmit={onSubmit} className="flex items-end gap-3 mb-3">
                <div className="flex-1 relative">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                    className="w-full h-12 bg-charcoal border border-steel-dark rounded-full px-5 text-base text-text-primary placeholder-text-muted focus:border-cyan-glow/40 focus:ring-0 focus:outline-none transition-all"
                    disabled={pending}
                  />
                </div>
                <button
                  type="submit"
                  disabled={pending || !input.trim()}
                  className="w-14 h-14 bg-gunmetal rounded-full flex items-center justify-center border-2 glow-medium transition-all shrink-0 disabled:opacity-40"
                  style={{ borderColor: "rgba(0, 200, 232, 0.3)" }}
                >
                  <svg className="w-6 h-6 text-cyan-glow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M13 5l7 7-7 7" />
                  </svg>
                </button>
              </form>

              <div className="flex items-center gap-2 overflow-x-auto pb-1">
                {quickActions.map((action) => (
                  <button
                    key={action.label}
                    onClick={() => void submitPrompt(action.prompt)}
                    className="bg-gunmetal border border-steel-dark rounded-full px-3 py-1.5 text-xs text-text-secondary whitespace-nowrap transition-all shrink-0 hover:border-cyan-glow/30 hover:text-cyan-glow"
                    disabled={pending}
                  >
                    {action.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {showActivity && (
          <aside className="w-80 bg-charcoal border-l border-steel-dark overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-orbitron text-lg font-semibold">Activity Feed</h2>
                <button
                  onClick={() => setShowActivity(false)}
                  className="w-8 h-8 bg-gunmetal rounded-lg flex items-center justify-center hover:bg-steel-mid transition-all"
                >
                  <svg className="w-4 h-4 text-cyan-glow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="space-y-3 mb-8">
                {messages.length === 0 && (
                  <div className="bg-gunmetal rounded-lg p-4 border border-steel-dark text-xs text-text-secondary">
                    No events yet for this session.
                  </div>
                )}

                {[...messages]
                  .filter((m) => m.role === "assistant")
                  .slice(-8)
                  .reverse()
                  .map((item) => (
                    <div key={item.id} className="bg-gunmetal rounded-lg p-4 border border-steel-dark">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-sm">Assistant Response</span>
                        <span className="text-xs text-text-muted">{item.time}</span>
                      </div>
                      <p className="text-xs text-text-secondary line-clamp-3">{item.content}</p>
                    </div>
                  ))}
              </div>

              <div>
                <h3 className="font-orbitron text-sm font-semibold text-cyan-glow mb-4">Session Stats</h3>
                <div className="space-y-3">
                  <div className="bg-gunmetal rounded-lg p-4 border border-steel-dark">
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-text-secondary">Messages</span>
                      <span className="text-lg font-bold text-cyan-glow">{messageCount}</span>
                    </div>
                  </div>
                  <div className="bg-gunmetal rounded-lg p-4 border border-steel-dark">
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-text-secondary">Last Risk</span>
                      <span className="text-sm font-bold text-cyan-glow uppercase">{lastAssistant?.meta?.risk ?? "n/a"}</span>
                    </div>
                  </div>
                  <div className="bg-gunmetal rounded-lg p-4 border border-steel-dark">
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-text-secondary">Runtime</span>
                      <span className="text-sm font-bold text-cyan-glow">{API_BASE}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </aside>
        )}
      </div>
    </AppShell>
  );
}
