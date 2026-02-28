"use client";

import { useState } from "react";
import AppShell from "@/components/layout/AppShell";

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState("general");

  const sections = [
    { id: "general", label: "General", icon: "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z" },
    { id: "models", label: "AI Models", icon: "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" },
    { id: "voice", label: "Voice & Avatar", icon: "M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" },
    { id: "security", label: "Security", icon: "M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" },
    { id: "billing", label: "Billing", icon: "M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" },
    { id: "api", label: "API Keys", icon: "M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" },
  ];

  return (
    <AppShell>
      <div className="flex h-[calc(100vh-4rem)]">
        {/* Settings Sidebar */}
        <div className="w-64 bg-charcoal border-r border-steel-dark p-4">
          <h2 className="font-orbitron text-lg font-semibold gradient-text px-3 mb-6">Settings</h2>
          <nav className="space-y-1">
            {sections.map((s) => (
              <button
                key={s.id}
                onClick={() => setActiveSection(s.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all ${
                  activeSection === s.id
                    ? "bg-gunmetal text-text-primary border-l-2 border-cyan-glow"
                    : "text-text-secondary hover:bg-gunmetal/50 hover:text-text-primary border-l-2 border-transparent"
                }`}
              >
                <svg className={`w-4 h-4 ${activeSection === s.id ? "text-cyan-glow" : ""}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d={s.icon} />
                </svg>
                {s.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Settings Content */}
        <div className="flex-1 overflow-y-auto p-8">
          {activeSection === "general" && (
            <div className="max-w-2xl space-y-8">
              <div>
                <h3 className="text-lg font-semibold mb-1">General Settings</h3>
                <p className="text-sm text-text-secondary">Configure your JARVIS AI preferences</p>
              </div>

              <div className="space-y-6">
                <div className="bg-charcoal border border-steel-dark rounded-xl p-5">
                  <h4 className="text-sm font-medium mb-4">Profile</h4>
                  <div className="space-y-4">
                    <div>
                      <label className="text-xs text-text-muted mb-1.5 block">Display Name</label>
                      <input type="text" placeholder="Enter display name" className="w-full h-10 bg-gunmetal border border-steel-dark rounded-lg px-3 text-sm text-text-primary focus:border-cyan-glow/40 focus:outline-none transition-all" />
                    </div>
                    <div>
                      <label className="text-xs text-text-muted mb-1.5 block">Email</label>
                      <input type="email" placeholder="Enter account email" className="w-full h-10 bg-gunmetal border border-steel-dark rounded-lg px-3 text-sm text-text-primary focus:border-cyan-glow/40 focus:outline-none transition-all" />
                    </div>
                    <div>
                      <label className="text-xs text-text-muted mb-1.5 block">Timezone</label>
                      <select className="w-full h-10 bg-gunmetal border border-steel-dark rounded-lg px-3 text-sm text-text-primary focus:border-cyan-glow/40 focus:outline-none transition-all">
                        <option>Asia/Kolkata (IST +5:30)</option>
                        <option>America/New_York (EST -5:00)</option>
                        <option>Europe/London (GMT +0:00)</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div className="bg-charcoal border border-steel-dark rounded-xl p-5">
                  <h4 className="text-sm font-medium mb-4">Product Mode</h4>
                  <div className="grid grid-cols-3 gap-3">
                    {[
                      { mode: "Personal", desc: "Single-user AI operator", active: true },
                      { mode: "Business", desc: "Multi-user team environment", active: false },
                      { mode: "Public", desc: "Demo & showcase mode", active: false },
                    ].map((m) => (
                      <button key={m.mode} className={`p-4 rounded-xl border text-left transition-all ${
                        m.active
                          ? "bg-gunmetal border-cyan-glow/30 glow-soft"
                          : "bg-gunmetal/50 border-steel-dark hover:border-steel-mid"
                      }`}>
                        <p className={`text-sm font-semibold ${m.active ? "text-cyan-glow" : "text-text-primary"}`}>{m.mode}</p>
                        <p className="text-xs text-text-muted mt-1">{m.desc}</p>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="bg-charcoal border border-steel-dark rounded-xl p-5">
                  <h4 className="text-sm font-medium mb-4">Preferences</h4>
                  <div className="space-y-4">
                    {[
                      { label: "Auto-execute low-risk actions", desc: "Skip approval for read-only operations", checked: true },
                      { label: "Voice auto-response", desc: "Respond with voice when voice input is detected", checked: true },
                      { label: "Proactive suggestions", desc: "JARVIS suggests actions based on context", checked: false },
                      { label: "Sound notifications", desc: "Play sound on task completion", checked: true },
                    ].map((pref) => (
                      <div key={pref.label} className="flex items-center justify-between">
                        <div>
                          <p className="text-sm">{pref.label}</p>
                          <p className="text-xs text-text-muted">{pref.desc}</p>
                        </div>
                        <div className={`w-10 h-6 rounded-full p-0.5 cursor-pointer transition-all ${
                          pref.checked ? "bg-cyan-glow" : "bg-steel-dark"
                        }`}>
                          <div className={`w-5 h-5 rounded-full bg-white shadow transition-transform ${
                            pref.checked ? "translate-x-4" : ""
                          }`} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeSection === "models" && (
            <div className="max-w-2xl space-y-8">
              <div>
                <h3 className="text-lg font-semibold mb-1">AI Model Configuration</h3>
                <p className="text-sm text-text-secondary">Multi-model routing with cost optimization</p>
              </div>

              <div className="space-y-4">
                {[
                  { category: "Triage / Classification", model: "GPT-4o-mini", cost: "$0.0001/1K", desc: "Fast intent classification and routing" },
                  { category: "Standard Response", model: "Claude Sonnet 4.6", cost: "$0.003/1K", desc: "Balanced quality and cost for most tasks" },
                  { category: "Complex Reasoning", model: "Claude Opus 4.6", cost: "$0.015/1K", desc: "Multi-step reasoning, planning, analysis" },
                  { category: "Code Generation", model: "Claude Sonnet 4.6", cost: "$0.003/1K", desc: "Code writing, debugging, review" },
                  { category: "Embeddings", model: "text-embedding-3-small", cost: "$0.00002/1K", desc: "Semantic search and memory retrieval" },
                ].map((m) => (
                  <div key={m.category} className="bg-charcoal border border-steel-dark rounded-xl p-5 hover:border-steel-mid transition-all">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-sm font-medium">{m.category}</h4>
                      <span className="text-xs font-jetbrains text-text-muted">{m.cost}</span>
                    </div>
                    <p className="text-xs text-text-muted mb-3">{m.desc}</p>
                    <select className="w-full h-9 bg-gunmetal border border-steel-dark rounded-lg px-3 text-sm text-cyan-glow focus:border-cyan-glow/40 focus:outline-none transition-all">
                      <option>{m.model}</option>
                    </select>
                  </div>
                ))}
              </div>

              <div className="bg-charcoal border border-steel-dark rounded-xl p-5">
                <h4 className="text-sm font-medium mb-4">Cost Controls</h4>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-xs mb-1.5">
                      <span className="text-text-muted">Daily Budget</span>
                      <span className="text-cyan-glow font-semibold">$5.00</span>
                    </div>
                    <input type="range" min="1" max="50" defaultValue="5" className="w-full" />
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm">Semantic Caching</p>
                      <p className="text-xs text-text-muted">Cache similar queries to reduce costs 30-50%</p>
                    </div>
                    <div className="w-10 h-6 rounded-full p-0.5 cursor-pointer bg-cyan-glow">
                      <div className="w-5 h-5 rounded-full bg-white shadow translate-x-4" />
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm">Context Compression</p>
                      <p className="text-xs text-text-muted">Auto-summarize at 80% context window</p>
                    </div>
                    <div className="w-10 h-6 rounded-full p-0.5 cursor-pointer bg-cyan-glow">
                      <div className="w-5 h-5 rounded-full bg-white shadow translate-x-4" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeSection === "voice" && (
            <div className="max-w-2xl space-y-8">
              <div>
                <h3 className="text-lg font-semibold mb-1">Voice & Avatar Settings</h3>
                <p className="text-sm text-text-secondary">Configure speech recognition, text-to-speech, and avatar</p>
              </div>

              <div className="bg-charcoal border border-steel-dark rounded-xl p-5">
                <h4 className="text-sm font-medium mb-4">Speech-to-Text (ASR)</h4>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { name: "Deepgram Nova-2", latency: "<300ms", cost: "$0.0043/min", active: true },
                    { name: "OpenAI Whisper", latency: "~1s", cost: "$0.006/min", active: false },
                  ].map((p) => (
                    <button key={p.name} className={`p-4 rounded-xl border text-left transition-all ${
                      p.active ? "bg-gunmetal border-cyan-glow/30 glow-soft" : "bg-gunmetal/50 border-steel-dark hover:border-steel-mid"
                    }`}>
                      <p className={`text-sm font-semibold ${p.active ? "text-cyan-glow" : ""}`}>{p.name}</p>
                      <div className="flex gap-3 mt-2 text-xs text-text-muted">
                        <span>{p.latency}</span>
                        <span>{p.cost}</span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              <div className="bg-charcoal border border-steel-dark rounded-xl p-5">
                <h4 className="text-sm font-medium mb-4">Text-to-Speech (TTS)</h4>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { name: "ElevenLabs", latency: "<500ms", cost: "$0.30/1K chars", active: true },
                    { name: "OpenAI TTS", latency: "<300ms", cost: "$0.015/1K chars", active: false },
                  ].map((p) => (
                    <button key={p.name} className={`p-4 rounded-xl border text-left transition-all ${
                      p.active ? "bg-gunmetal border-cyan-glow/30 glow-soft" : "bg-gunmetal/50 border-steel-dark hover:border-steel-mid"
                    }`}>
                      <p className={`text-sm font-semibold ${p.active ? "text-cyan-glow" : ""}`}>{p.name}</p>
                      <div className="flex gap-3 mt-2 text-xs text-text-muted">
                        <span>{p.latency}</span>
                        <span>{p.cost}</span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              <div className="bg-charcoal border border-steel-dark rounded-xl p-5">
                <h4 className="text-sm font-medium mb-4">Avatar (Phase 2)</h4>
                <div className="flex items-center gap-4 p-4 bg-gunmetal rounded-xl border border-steel-dark/50">
                  <div className="w-16 h-16 rounded-full bg-gradient-to-br from-cyan-glow to-cyan-teal flex items-center justify-center glow-medium">
                    <svg className="w-8 h-8 text-deep-space" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-sm font-medium">JARVIS Avatar</p>
                    <p className="text-xs text-text-muted mt-1">AI-powered lip-synced video avatar for presentations and demos.</p>
                    <span className="inline-block mt-2 text-xs bg-warning/10 text-warning px-2 py-0.5 rounded-full">Coming in Phase 2</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeSection === "security" && (
            <div className="max-w-2xl space-y-8">
              <div>
                <h3 className="text-lg font-semibold mb-1">Security & Access</h3>
                <p className="text-sm text-text-secondary">Authentication, encryption, and audit settings</p>
              </div>

              <div className="space-y-4">
                {[
                  { label: "Two-Factor Authentication", status: "Enabled", desc: "TOTP-based MFA on all admin actions" },
                  { label: "Session Timeout", status: "30 min", desc: "Auto-logout after idle period" },
                  { label: "Encryption at Rest", status: "AES-256", desc: "All data encrypted in database storage" },
                  { label: "TLS Version", status: "1.3", desc: "All connections encrypted in transit" },
                  { label: "Audit Logging", status: "Active", desc: "Immutable log of all tool executions and approvals" },
                  { label: "Prompt Injection Detection", status: "Active", desc: "Input sanitization and anomaly detection" },
                ].map((item) => (
                  <div key={item.label} className="bg-charcoal border border-steel-dark rounded-xl p-5 flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium">{item.label}</p>
                      <p className="text-xs text-text-muted mt-0.5">{item.desc}</p>
                    </div>
                    <span className="text-sm font-jetbrains text-success bg-success/10 px-3 py-1 rounded-lg">{item.status}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeSection === "billing" && (
            <div className="max-w-2xl space-y-8">
              <div>
                <h3 className="text-lg font-semibold mb-1">Billing & Plans</h3>
                <p className="text-sm text-text-secondary">Subscription management and usage billing</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                {[
                  { plan: "Starter", price: "$29-49", features: ["500 tasks/mo", "5 tool integrations", "30-day memory"], current: false },
                  { plan: "Pro", price: "$79-149", features: ["2,000 tasks/mo", "15 tools + voice", "90-day memory"], current: true },
                  { plan: "Agency", price: "$249-499", features: ["10,000 tasks/mo", "All tools + API", "White-label"], current: false },
                  { plan: "Enterprise", price: "$2,000+", features: ["Unlimited", "SSO + Data residency", "Dedicated support"], current: false },
                ].map((p) => (
                  <div key={p.plan} className={`bg-charcoal border rounded-xl p-5 transition-all ${
                    p.current ? "border-cyan-glow/30 glow-soft" : "border-steel-dark hover:border-steel-mid"
                  }`}>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-base font-semibold">{p.plan}</h4>
                      {p.current && <span className="text-xs bg-cyan-glow/10 text-cyan-glow px-2 py-0.5 rounded-full">Current</span>}
                    </div>
                    <p className="text-2xl font-bold text-cyan-glow">{p.price}<span className="text-sm text-text-muted font-normal">/mo</span></p>
                    <ul className="mt-3 space-y-1.5">
                      {p.features.map((f) => (
                        <li key={f} className="text-xs text-text-secondary flex items-center gap-2">
                          <svg className="w-3.5 h-3.5 text-success shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                          {f}
                        </li>
                      ))}
                    </ul>
                    <button className={`w-full mt-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      p.current
                        ? "bg-gunmetal border border-steel-dark text-text-secondary"
                        : "bg-cyan-glow/10 border border-cyan-glow/20 text-cyan-glow hover:bg-cyan-glow/20"
                    }`}>
                      {p.current ? "Current Plan" : "Upgrade"}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeSection === "api" && (
            <div className="max-w-2xl space-y-8">
              <div>
                <h3 className="text-lg font-semibold mb-1">API Keys</h3>
                <p className="text-sm text-text-secondary">Manage API keys for external integrations</p>
              </div>

              <div className="bg-charcoal border border-steel-dark rounded-xl p-5">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-sm font-medium">Active Keys</h4>
                  <button className="text-xs text-cyan-glow hover:text-cyan-teal transition-all">+ Generate New Key</button>
                </div>
                <div className="space-y-3">
                  <div className="bg-gunmetal rounded-lg p-4 border border-steel-dark/50 text-sm text-text-secondary">
                    No API keys configured yet.
                  </div>
                </div>
              </div>

              <div className="bg-charcoal border border-steel-dark rounded-xl p-5">
                <h4 className="text-sm font-medium mb-3">API Endpoints</h4>
                <div className="space-y-2">
                  {[
                    { method: "POST", path: "/api/v1/chat", desc: "Send message, get streaming response" },
                    { method: "POST", path: "/api/v1/tasks", desc: "Create new task" },
                    { method: "GET", path: "/api/v1/tasks/{id}", desc: "Get task status" },
                    { method: "POST", path: "/api/v1/memory/search", desc: "Semantic memory search" },
                    { method: "GET", path: "/api/v1/tools", desc: "List MCP tools" },
                    { method: "WS", path: "/ws/v1/voice", desc: "Real-time voice streaming" },
                  ].map((ep) => (
                    <div key={ep.path} className="flex items-center gap-3 py-2 border-b border-steel-dark/30 last:border-0">
                      <span className={`text-xs font-jetbrains font-semibold px-2 py-0.5 rounded ${
                        ep.method === "POST" ? "bg-cyan-glow/10 text-cyan-glow" :
                        ep.method === "GET" ? "bg-success/10 text-success" :
                        "bg-purple-500/10 text-purple-400"
                      }`}>{ep.method}</span>
                      <span className="text-sm font-jetbrains text-text-primary">{ep.path}</span>
                      <span className="text-xs text-text-muted ml-auto">{ep.desc}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
