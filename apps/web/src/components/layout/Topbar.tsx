"use client";

import { Command, Search } from "lucide-react";

export function Topbar() {
  return (
    <header className="sticky top-0 z-10 flex h-16 items-center gap-4 border-b border-line bg-bg/70 px-6 backdrop-blur-md">
      <button className="focus-ring flex h-9 w-72 items-center gap-2 rounded-lg border border-line bg-panel px-3 text-sm text-muted transition hover:border-accent/40">
        <Search size={15} />
        <span>Search missions, ideas…</span>
        <span className="mono ml-auto flex items-center gap-0.5 text-[10px] text-faint">
          <Command size={11} />K
        </span>
      </button>

      <div className="ml-auto flex items-center gap-3">
        <span className="hidden items-center gap-1.5 rounded-full border border-line bg-panel px-2.5 py-1 text-xs text-muted sm:inline-flex">
          <span className="status-dot text-accent" style={{ width: 6, height: 6 }} />
          Mission Control Dev
        </span>
        <div className="flex h-9 items-center gap-2 rounded-lg border border-line bg-panel px-2.5">
          <div className="grid h-6 w-6 place-items-center rounded-full bg-accent/15 text-xs font-semibold text-accent">
            G
          </div>
          <div className="hidden leading-none sm:block">
            <div className="text-xs font-medium">George Dev</div>
            <div className="label mt-0.5">Owner</div>
          </div>
        </div>
      </div>
    </header>
  );
}
