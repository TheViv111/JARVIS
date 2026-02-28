"use client";

import { useState } from "react";
import AppShell from "@/components/layout/AppShell";

const integrations = [
  {
    name: "Gmail",
    category: "Email",
    description: "Read, compose, send, search, label, and archive emails",
    status: "connected",
    connectorType: "MCP Server",
    riskTier: "medium",
    calls: 245,
    lastUsed: "2 min ago",
  },
  {
    name: "Google Calendar",
    category: "Calendar",
    description: "Read, create, update, delete events; find free slots",
    status: "connected",
    connectorType: "MCP Server",
    riskTier: "medium",
    calls: 89,
    lastUsed: "15 min ago",
  },
  {
    name: "ClickUp",
    category: "Project Mgmt",
    description: "Create tasks, update status, assign, comment",
    status: "connected",
    connectorType: "MCP Server",
    riskTier: "low",
    calls: 156,
    lastUsed: "5 min ago",
  },
  {
    name: "HubSpot CRM",
    category: "CRM",
    description: "Read/write contacts, deals, tasks, notes, pipelines",
    status: "connected",
    connectorType: "OpenAPI + Custom",
    riskTier: "high",
    calls: 67,
    lastUsed: "1 hour ago",
  },
  {
    name: "Google Docs",
    category: "Documents",
    description: "Read, create, edit, search documents",
    status: "connected",
    connectorType: "MCP Server",
    riskTier: "low",
    calls: 42,
    lastUsed: "3 hours ago",
  },
  {
    name: "Google Drive",
    category: "Files",
    description: "Upload, download, search, share files",
    status: "connected",
    connectorType: "MCP Server",
    riskTier: "low",
    calls: 34,
    lastUsed: "2 hours ago",
  },
  {
    name: "Notion",
    category: "Documents",
    description: "Read, create, update pages, databases, and blocks",
    status: "disconnected",
    connectorType: "MCP Server",
    riskTier: "low",
    calls: 0,
    lastUsed: "Never",
  },
  {
    name: "Slack",
    category: "Communication",
    description: "Send messages, read channels, manage threads",
    status: "disconnected",
    connectorType: "MCP Server",
    riskTier: "medium",
    calls: 0,
    lastUsed: "Never",
  },
  {
    name: "Web Browser",
    category: "Web",
    description: "Fetch URLs, extract content, screenshot, search",
    status: "connected",
    connectorType: "Custom Handler",
    riskTier: "low",
    calls: 312,
    lastUsed: "10 min ago",
  },
  {
    name: "n8n Workflows",
    category: "Workflow",
    description: "Trigger workflows, pass data, receive results",
    status: "connected",
    connectorType: "Webhook + API",
    riskTier: "medium",
    calls: 28,
    lastUsed: "30 min ago",
  },
  {
    name: "Salesforce",
    category: "CRM",
    description: "Enterprise CRM with contacts, opportunities, reports",
    status: "disconnected",
    connectorType: "OpenAPI + Custom",
    riskTier: "high",
    calls: 0,
    lastUsed: "Never",
  },
  {
    name: "Asana",
    category: "Project Mgmt",
    description: "Task management, project tracking, team collaboration",
    status: "disconnected",
    connectorType: "MCP Server",
    riskTier: "low",
    calls: 0,
    lastUsed: "Never",
  },
];

export default function IntegrationsPage() {
  const [filter, setFilter] = useState<"all" | "connected" | "disconnected">("all");
  const filtered = integrations.filter((i) =>
    filter === "all" ? true : i.status === filter
  );

  return (
    <AppShell>
      <div className="p-6 space-y-6 max-w-[1600px] mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="font-orbitron text-2xl font-bold gradient-text">Integrations</h1>
            <p className="text-sm text-text-secondary mt-1">MCP tool registry — connect, manage, and monitor external services</p>
          </div>
          <button className="bg-cyan-glow text-deep-space px-4 py-2 rounded-lg text-sm font-semibold hover:bg-cyan-teal transition-all flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Integration
          </button>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-4 gap-4">
          {[
            { label: "Connected", value: integrations.filter(i => i.status === "connected").length, color: "text-success" },
            { label: "Available", value: integrations.filter(i => i.status === "disconnected").length, color: "text-text-secondary" },
            { label: "Total API Calls", value: integrations.reduce((s, i) => s + i.calls, 0).toLocaleString(), color: "text-cyan-glow" },
            { label: "Connector Types", value: "3", color: "text-cyan-glow" },
          ].map((s) => (
            <div key={s.label} className="bg-charcoal border border-steel-dark rounded-xl p-4">
              <p className="text-xs text-text-muted">{s.label}</p>
              <p className={`text-2xl font-bold ${s.color} mt-1`}>{s.value}</p>
            </div>
          ))}
        </div>

        {/* Filter Tabs */}
        <div className="flex items-center gap-1 bg-charcoal rounded-xl p-1 border border-steel-dark w-fit">
          {(["all", "connected", "disconnected"] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`px-5 py-2 rounded-lg text-sm font-medium transition-all capitalize ${
                filter === tab
                  ? "bg-gunmetal text-text-primary shadow-sm"
                  : "text-text-secondary hover:text-cyan-glow"
              }`}
            >
              {tab} {tab !== "all" ? `(${integrations.filter(i => i.status === tab).length})` : ""}
            </button>
          ))}
        </div>

        {/* Integration Cards */}
        <div className="grid grid-cols-3 gap-4">
          {filtered.map((tool) => (
            <div key={tool.name} className="bg-charcoal border border-steel-dark rounded-xl p-5 hover:border-steel-mid transition-all group">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-base font-semibold">{tool.name}</h3>
                    <div className={`w-2 h-2 rounded-full ${
                      tool.status === "connected" ? "bg-success" : "bg-steel-mid"
                    }`} style={tool.status === "connected" ? { boxShadow: "0 0 6px rgba(0, 232, 140, 0.5)" } : undefined} />
                  </div>
                  <span className="text-xs text-text-muted">{tool.category}</span>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  tool.riskTier === "low" ? "bg-success/10 text-success" :
                  tool.riskTier === "medium" ? "bg-warning/10 text-warning" :
                  "bg-error/10 text-error"
                }`}>
                  {tool.riskTier} risk
                </span>
              </div>

              <p className="text-sm text-text-secondary mb-4">{tool.description}</p>

              <div className="flex items-center justify-between text-xs text-text-muted border-t border-steel-dark/50 pt-3">
                <span>{tool.connectorType}</span>
                <span>{tool.calls > 0 ? `${tool.calls} calls` : ""}</span>
                <span>{tool.lastUsed}</span>
              </div>

              <button className={`w-full mt-4 py-2 rounded-lg text-sm font-medium transition-all ${
                tool.status === "connected"
                  ? "bg-gunmetal border border-steel-dark text-text-secondary hover:border-error/30 hover:text-error"
                  : "bg-cyan-glow/10 border border-cyan-glow/20 text-cyan-glow hover:bg-cyan-glow/20"
              }`}>
                {tool.status === "connected" ? "Manage" : "Connect"}
              </button>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
