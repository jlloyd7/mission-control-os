"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Bot,
  FlaskConical,
  LayoutDashboard,
  Radio,
  Rocket,
  Scale,
  ShieldCheck,
  Wrench,
} from "lucide-react";

import { cx } from "@/lib/ui";

const NAV = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/ideas", label: "Forge", icon: FlaskConical },
  { href: "/missions", label: "Missions", icon: Rocket },
  { href: "/approvals", label: "Approvals", icon: ShieldCheck },
  { href: "/agents", label: "Agents", icon: Bot },
  { href: "/tools", label: "Tools", icon: Wrench },
  { href: "/governance", label: "Governance", icon: Scale },
];

export function Sidebar() {
  const path = usePathname();
  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-line bg-bg-2/70 backdrop-blur md:flex">
      <div className="flex h-16 items-center gap-2.5 border-b border-line px-5">
        <div className="grid h-9 w-9 place-items-center rounded-lg border border-accent/30 bg-gradient-to-br from-accent/25 to-accent-2/15">
          <Radio size={18} className="text-accent" />
        </div>
        <div>
          <div className="text-sm font-semibold leading-none tracking-tight">Mission Control</div>
          <div className="label mt-1.5">OS · v0.1</div>
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-3 py-4">
        {NAV.map((item) => {
          const active = path === item.href || path.startsWith(item.href + "/");
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cx(
                "group flex h-9 items-center gap-3 rounded-lg border px-3 text-sm transition",
                active
                  ? "border-accent/25 bg-accent/10 text-text"
                  : "border-transparent text-muted hover:bg-white/5 hover:text-text",
              )}
            >
              <Icon
                size={17}
                className={active ? "text-accent" : "text-faint group-hover:text-muted"}
              />
              <span>{item.label}</span>
              {active && (
                <span className="status-dot ml-auto text-accent" style={{ width: 6, height: 6 }} />
              )}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-line px-4 py-4">
        <div className="rounded-lg border border-line bg-panel px-3 py-2.5">
          <div className="label">Environment</div>
          <div className="mt-2 flex items-center gap-2 text-xs">
            <span className="status-dot text-ok" style={{ width: 6, height: 6 }} />
            <span className="text-text">Mock mode</span>
            <span className="mono ml-auto text-faint">safe</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
