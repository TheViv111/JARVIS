"use client";

import { useState } from "react";
import AppShell from "@/components/layout/AppShell";

const memoryTiers = [
  { name: "Session Memory", storage: "Redis", entries: "124", size: "2.4 MB", status: "Active", retention: "Session + 30min" },
  { name: "Episodic Memory", storage: "pgvector", entries: "3,847", size: "156 MB", status: "Active", retention: "Indefinite" },
  { name: "Knowledge Graph", storage: "Neo4j", entries: "892 nodes", size: "45 MB", status: "Active", retention: "Indefinite" },
  { name: "Event Log", storage: "Postgres", entries: "12,456", size: "89 MB", status: "Active", retention: "90 days" },
];

const entities = [
  { name: "Sarah Chen", type: "Person", connections: 14, lastSeen: "2 hours ago", tags: ["Client", "BuildFlow"] },
  { name: "BuildFlow Inc.", type: "Company", connections: 8, lastSeen: "2 hours ago", tags: ["Active Deal", "$45K"] },
  { name: "Q4 Strategy Deck", type: "Document", connections: 5, lastSeen: "1 day ago", tags: ["Internal", "Strategy"] },
  { name: "Sprint Review Meeting", type: "Event", connections: 12, lastSeen: "3 hours ago", tags: ["Recurring", "Weekly"] },
  { name: "HubSpot CRM", type: "Tool", connections: 23, lastSeen: "30 min ago", tags: ["Integration", "Active"] },
  { name: "Vendor Approval Process", type: "Process", connections: 7, lastSeen: "2 days ago", tags: ["Blocked", "Finance"] },
];

const recentMemories = [
  { content: "User prefers email responses to be concise and action-oriented", type: "Preference", score: 0.95, timestamp: "Today, 2:34 PM" },
  { content: "Sarah Chen from BuildFlow rescheduled meeting to tomorrow 3 PM", type: "Event", score: 0.92, timestamp: "Today, 2:32 PM" },
  { content: "Q4 budget allocation needs team approval — deadline Friday", type: "Task", score: 0.89, timestamp: "Today, 2:32 PM" },
  { content: "Server maintenance scheduled for this weekend — notify team", type: "Alert", score: 0.85, timestamp: "Today, 2:32 PM" },
  { content: "Weekly report was submitted successfully to management", type: "Completion", score: 0.78, timestamp: "Today, 1:15 PM" },
  { content: "User typically starts day with email triage at 9 AM", type: "Pattern", score: 0.74, timestamp: "Yesterday" },
  { content: "BuildFlow proposal needs competitor pricing data before sending", type: "Dependency", score: 0.71, timestamp: "Yesterday" },
  { content: "Client prefers Friday afternoon calls over morning slots", type: "Preference", score: 0.68, timestamp: "2 days ago" },
];

export default function MemoryPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState<"memories" | "entities" | "graph">("memories");

  return (
    <AppShell>
      <div className="p-6 space-y-6 max-w-[1600px] mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="font-orbitron text-2xl font-bold gradient-text">Memory Management</h1>
            <p className="text-sm text-text-secondary mt-1">Persistent memory tiers, knowledge graph, and entity tracking</p>
          </div>
          <button className="bg-gunmetal border border-steel-dark px-4 py-2 rounded-lg text-sm text-text-secondary hover:border-cyan-glow/30 hover:text-cyan-glow transition-all">
            Run Compaction
          </button>
        </div>

        {/* Memory Tiers */}
        <div className="grid grid-cols-4 gap-4">
          {memoryTiers.map((tier) => (
            <div key={tier.name} className="bg-charcoal border border-steel-dark rounded-xl p-5 hover:border-steel-mid transition-all">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold">{tier.name}</h3>
                <div className="w-2.5 h-2.5 rounded-full bg-success" style={{ boxShadow: "0 0 6px rgba(0, 232, 140, 0.5)" }} />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-text-muted">Storage</span>
                  <span className="text-text-secondary font-jetbrains">{tier.storage}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-text-muted">Entries</span>
                  <span className="text-cyan-glow font-semibold">{tier.entries}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-text-muted">Size</span>
                  <span className="text-text-secondary font-jetbrains">{tier.size}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-text-muted">Retention</span>
                  <span className="text-text-secondary">{tier.retention}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Search */}
        <div className="relative">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Semantic search across all memory tiers..."
            className="w-full h-12 bg-charcoal border border-steel-dark rounded-xl px-5 pl-12 text-base text-text-primary placeholder-text-muted focus:border-cyan-glow/40 focus:outline-none transition-all"
          />
          <svg className="w-5 h-5 text-text-muted absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        {/* Tabs */}
        <div className="flex items-center gap-1 bg-charcoal rounded-xl p-1 border border-steel-dark w-fit">
          {(["memories", "entities", "graph"] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-5 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === tab
                  ? "bg-gunmetal text-text-primary shadow-sm"
                  : "text-text-secondary hover:text-cyan-glow"
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Content */}
        {activeTab === "memories" && (
          <div className="space-y-3">
            {recentMemories.map((mem, i) => (
              <div key={i} className="bg-charcoal border border-steel-dark rounded-xl p-5 hover:border-steel-mid transition-all group">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-[15px] text-text-primary leading-relaxed">{mem.content}</p>
                    <div className="flex items-center gap-3 mt-3">
                      <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                        mem.type === "Preference" ? "bg-purple-500/10 text-purple-400" :
                        mem.type === "Event" ? "bg-cyan-glow/10 text-cyan-glow" :
                        mem.type === "Task" ? "bg-warning/10 text-warning" :
                        mem.type === "Alert" ? "bg-error/10 text-error" :
                        mem.type === "Pattern" ? "bg-success/10 text-success" :
                        "bg-steel-dark text-text-secondary"
                      }`}>
                        {mem.type}
                      </span>
                      <span className="text-xs text-text-muted">{mem.timestamp}</span>
                    </div>
                  </div>
                  <div className="ml-4 text-right">
                    <div className="text-sm font-jetbrains text-cyan-glow">{(mem.score * 100).toFixed(0)}%</div>
                    <div className="text-xs text-text-muted">relevance</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "entities" && (
          <div className="grid grid-cols-3 gap-4">
            {entities.map((entity) => (
              <div key={entity.name} className="bg-charcoal border border-steel-dark rounded-xl p-5 hover:border-steel-mid transition-all cursor-pointer">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h4 className="text-sm font-semibold">{entity.name}</h4>
                    <span className="text-xs text-text-muted">{entity.type}</span>
                  </div>
                  <div className="w-10 h-10 bg-gunmetal rounded-lg flex items-center justify-center">
                    <span className="text-lg font-bold text-cyan-glow">{entity.connections}</span>
                  </div>
                </div>
                <div className="flex flex-wrap gap-1.5 mb-3">
                  {entity.tags.map((tag) => (
                    <span key={tag} className="text-xs bg-gunmetal border border-steel-dark px-2 py-0.5 rounded-md text-text-secondary">{tag}</span>
                  ))}
                </div>
                <p className="text-xs text-text-muted">Last seen: {entity.lastSeen}</p>
              </div>
            ))}
          </div>
        )}

        {activeTab === "graph" && (
          <div className="bg-charcoal border border-steel-dark rounded-xl p-8 flex items-center justify-center min-h-[400px]">
            <div className="text-center">
              <div className="w-20 h-20 bg-gunmetal rounded-2xl flex items-center justify-center mx-auto mb-4 glow-soft">
                <svg className="w-10 h-10 text-cyan-glow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5" />
                </svg>
              </div>
              <h3 className="font-orbitron text-lg font-semibold gradient-text mb-2">Knowledge Graph Viewer</h3>
              <p className="text-sm text-text-secondary max-w-md">
                Interactive 3D visualization of entities, relationships, and connections.
                <br />892 nodes, 2,340 edges across your business context.
              </p>
              <button className="mt-4 bg-cyan-glow text-deep-space px-6 py-2 rounded-lg text-sm font-semibold hover:bg-cyan-teal transition-all">
                Launch Graph Explorer
              </button>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
