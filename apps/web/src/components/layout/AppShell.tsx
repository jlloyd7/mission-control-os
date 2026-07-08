import type { ReactNode } from "react";

import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-full">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar />
        <main className="bg-grid flex-1">
          <div className="mx-auto max-w-[1220px] px-6 py-8">{children}</div>
        </main>
      </div>
    </div>
  );
}
