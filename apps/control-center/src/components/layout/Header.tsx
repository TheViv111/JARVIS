"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { label: "Command Center", href: "/" },
  { label: "Dashboard", href: "/dashboard" },
  { label: "Memory", href: "/memory" },
  { label: "Integrations", href: "/integrations" },
  { label: "Settings", href: "/settings" },
];

export default function Header() {
  const pathname = usePathname();

  return (
    <header className="fixed top-0 left-0 right-0 h-16 bg-charcoal border-b border-steel-dark z-50 flex items-center">
      <div className="w-full px-6 flex items-center justify-between">
        <div className="flex items-center gap-12">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-gradient-to-br from-cyan-glow to-cyan-teal rounded-lg flex items-center justify-center glow-medium">
              <svg className="w-5 h-5 text-deep-space" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
              </svg>
            </div>
            <span className="font-orbitron text-2xl font-bold gradient-text">JARVIS</span>
          </div>
          <nav className="flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`relative px-4 py-2 text-sm font-medium transition-all rounded-lg ${
                    isActive
                      ? "text-text-primary bg-gunmetal"
                      : "text-text-secondary hover:text-cyan-glow hover:bg-gunmetal/50"
                  }`}
                >
                  {item.label}
                  {isActive && (
                    <span className="absolute bottom-0 left-2 right-2 h-0.5 bg-cyan-glow rounded-full" style={{ boxShadow: "0 0 8px rgba(0, 200, 232, 0.4)" }} />
                  )}
                </Link>
              );
            })}
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <button className="w-10 h-10 bg-gunmetal rounded-lg flex items-center justify-center hover:bg-steel-mid transition-all glow-soft">
            <svg className="w-5 h-5 text-cyan-glow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </button>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-success" style={{ boxShadow: "0 0 8px rgba(0, 232, 140, 0.6)" }} />
            <span className="text-xs text-text-secondary">Connected</span>
          </div>
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-glow to-cyan-teal flex items-center justify-center avatar-glow border border-cyan-glow/30">
            <span className="text-xs font-bold text-deep-space">DT</span>
          </div>
        </div>
      </div>
    </header>
  );
}
