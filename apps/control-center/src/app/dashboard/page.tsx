"use client";

import AppShell from "@/components/layout/AppShell";

const statCards = [
  { label: "Daily Active Users", value: "24", change: "+12%", up: true, icon: "M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" },
  { label: "Tasks Completed", value: "156", change: "+8%", up: true, icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" },
  { label: "Memory Recall", value: "92%", change: "+3%", up: true, icon: "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" },
  { label: "Avg Latency", value: "1.2s", change: "-15%", up: true, icon: "M13 10V3L4 14h7v7l9-11h-7z" },
  { label: "API Cost Today", value: "$3.42", change: "+$0.80", up: false, icon: "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" },
  { label: "Tool Calls", value: "89", change: "+22%", up: true, icon: "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z" },
];

const modelUsage = [
  { model: "GPT-4o-mini", calls: 245, cost: "$0.12", category: "Triage" },
  { model: "Claude Sonnet 4.6", calls: 89, cost: "$1.34", category: "Standard" },
  { model: "GPT-4o", calls: 42, cost: "$0.84", category: "Standard" },
  { model: "Claude Opus 4.6", calls: 12, cost: "$0.72", category: "Complex" },
  { model: "Gemini Flash", calls: 156, cost: "$0.08", category: "Fast" },
  { model: "text-embedding-3-small", calls: 520, cost: "$0.01", category: "Embeddings" },
];

const recentTasks = [
  { name: "Check inbox & summarize", status: "completed", tools: ["Gmail", "LLM"], duration: "4.2s", cost: "$0.003" },
  { name: "Create ClickUp task from email", status: "completed", tools: ["Gmail", "ClickUp"], duration: "6.1s", cost: "$0.005" },
  { name: "Draft client proposal", status: "completed", tools: ["Google Docs", "LLM"], duration: "12.4s", cost: "$0.028" },
  { name: "Schedule follow-up meeting", status: "pending_approval", tools: ["Calendar", "Gmail"], duration: "—", cost: "$0.002" },
  { name: "Research competitor pricing", status: "executing", tools: ["Web Scraper", "LLM"], duration: "—", cost: "$0.015" },
  { name: "Update CRM deal stage", status: "failed", tools: ["HubSpot"], duration: "2.1s", cost: "$0.001" },
];

const costBreakdown = [
  { label: "LLM API Calls", amount: "$2.38", pct: 70 },
  { label: "Embeddings", amount: "$0.42", pct: 12 },
  { label: "Tool Execution", amount: "$0.35", pct: 10 },
  { label: "Voice (ASR+TTS)", amount: "$0.18", pct: 5 },
  { label: "Storage", amount: "$0.09", pct: 3 },
];

export default function Dashboard() {
  return (
    <AppShell>
      <div className="p-6 space-y-6 max-w-[1600px] mx-auto">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="font-orbitron text-2xl font-bold gradient-text">Dashboard</h1>
            <p className="text-sm text-text-secondary mt-1">System performance, cost tracking, and analytics</p>
          </div>
          <div className="flex items-center gap-3">
            <select className="bg-gunmetal border border-steel-dark rounded-lg px-3 py-2 text-sm text-text-secondary focus:outline-none focus:border-cyan-glow/40">
              <option>Last 24 Hours</option>
              <option>Last 7 Days</option>
              <option>Last 30 Days</option>
            </select>
            <button className="bg-cyan-glow text-deep-space px-4 py-2 rounded-lg text-sm font-semibold hover:bg-cyan-teal transition-all">
              Export Report
            </button>
          </div>
        </div>

        {/* Stat Cards */}
        <div className="grid grid-cols-6 gap-4">
          {statCards.map((stat) => (
            <div key={stat.label} className="bg-charcoal border border-steel-dark rounded-xl p-4 hover:border-steel-mid transition-all">
              <div className="flex items-center justify-between mb-3">
                <div className="w-10 h-10 bg-gunmetal rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-cyan-glow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d={stat.icon} />
                  </svg>
                </div>
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                  stat.up ? "bg-success/10 text-success" : "bg-error/10 text-error"
                }`}>
                  {stat.change}
                </span>
              </div>
              <p className="text-2xl font-bold text-text-primary">{stat.value}</p>
              <p className="text-xs text-text-muted mt-1">{stat.label}</p>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-3 gap-6">
          {/* Model Usage */}
          <div className="bg-charcoal border border-steel-dark rounded-xl p-6">
            <h3 className="font-orbitron text-sm font-semibold text-cyan-glow mb-4">Model Usage</h3>
            <div className="space-y-3">
              {modelUsage.map((m) => (
                <div key={m.model} className="flex items-center justify-between py-2 border-b border-steel-dark/50 last:border-0">
                  <div>
                    <p className="text-sm font-medium">{m.model}</p>
                    <p className="text-xs text-text-muted">{m.category}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-cyan-glow">{m.cost}</p>
                    <p className="text-xs text-text-muted">{m.calls} calls</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Cost Breakdown */}
          <div className="bg-charcoal border border-steel-dark rounded-xl p-6">
            <h3 className="font-orbitron text-sm font-semibold text-cyan-glow mb-4">Cost Breakdown</h3>
            <div className="text-center mb-6">
              <p className="text-4xl font-bold gradient-text">$3.42</p>
              <p className="text-sm text-text-muted mt-1">Total today</p>
            </div>
            <div className="space-y-4">
              {costBreakdown.map((item) => (
                <div key={item.label}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-text-secondary">{item.label}</span>
                    <span className="text-sm font-medium">{item.amount}</span>
                  </div>
                  <div className="w-full h-2 bg-steel-dark rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-cyan-glow to-cyan-teal rounded-full transition-all"
                      style={{ width: `${item.pct}%`, boxShadow: "0 0 6px rgba(0, 200, 232, 0.3)" }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* System Health */}
          <div className="bg-charcoal border border-steel-dark rounded-xl p-6">
            <h3 className="font-orbitron text-sm font-semibold text-cyan-glow mb-4">System Health</h3>
            <div className="space-y-4">
              {[
                { label: "LLM Gateway", status: "Operational", latency: "142ms" },
                { label: "MCP Registry", status: "Operational", latency: "23ms" },
                { label: "Memory Pipeline", status: "Operational", latency: "89ms" },
                { label: "Voice Pipeline", status: "Operational", latency: "310ms" },
                { label: "Task Engine", status: "Operational", latency: "56ms" },
                { label: "Vector DB", status: "Degraded", latency: "450ms" },
              ].map((s) => (
                <div key={s.label} className="flex items-center justify-between py-2 border-b border-steel-dark/50 last:border-0">
                  <div className="flex items-center gap-3">
                    <div className={`w-2.5 h-2.5 rounded-full ${
                      s.status === "Operational" ? "bg-success" : "bg-warning"
                    }`} style={{ boxShadow: s.status === "Operational" ? "0 0 6px rgba(0, 232, 140, 0.5)" : "0 0 6px rgba(232, 168, 0, 0.5)" }} />
                    <span className="text-sm">{s.label}</span>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-jetbrains text-text-muted">{s.latency}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Tasks */}
        <div className="bg-charcoal border border-steel-dark rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-orbitron text-sm font-semibold text-cyan-glow">Recent Task Executions</h3>
            <button className="text-xs text-text-secondary hover:text-cyan-glow transition-all">View All</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-steel-dark">
                  <th className="text-left text-xs text-text-muted font-medium pb-3 pr-4">Task</th>
                  <th className="text-left text-xs text-text-muted font-medium pb-3 pr-4">Status</th>
                  <th className="text-left text-xs text-text-muted font-medium pb-3 pr-4">Tools Used</th>
                  <th className="text-left text-xs text-text-muted font-medium pb-3 pr-4">Duration</th>
                  <th className="text-right text-xs text-text-muted font-medium pb-3">Cost</th>
                </tr>
              </thead>
              <tbody>
                {recentTasks.map((task, i) => (
                  <tr key={i} className="border-b border-steel-dark/30 last:border-0 hover:bg-gunmetal/30 transition-all">
                    <td className="py-3 pr-4">
                      <span className="text-sm">{task.name}</span>
                    </td>
                    <td className="py-3 pr-4">
                      <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                        task.status === "completed" ? "bg-success/10 text-success" :
                        task.status === "executing" ? "bg-cyan-glow/10 text-cyan-glow" :
                        task.status === "pending_approval" ? "bg-warning/10 text-warning" :
                        "bg-error/10 text-error"
                      }`}>
                        {task.status === "completed" ? "Completed" :
                         task.status === "executing" ? "Executing" :
                         task.status === "pending_approval" ? "Pending Approval" :
                         "Failed"}
                      </span>
                    </td>
                    <td className="py-3 pr-4">
                      <div className="flex gap-1.5">
                        {task.tools.map((tool) => (
                          <span key={tool} className="text-xs bg-gunmetal border border-steel-dark px-2 py-0.5 rounded-md text-text-secondary">{tool}</span>
                        ))}
                      </div>
                    </td>
                    <td className="py-3 pr-4">
                      <span className="text-sm font-jetbrains text-text-secondary">{task.duration}</span>
                    </td>
                    <td className="py-3 text-right">
                      <span className="text-sm font-jetbrains text-text-secondary">{task.cost}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
