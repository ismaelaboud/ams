"use client";

import { DashboardNav } from "@/components/dashboard/dashboard-nav";
import { ScrollArea } from "@/components/ui/scroll-area";
import { NavItem } from "@/types";
import { cn } from "@/lib/utils";

export const navItems: NavItem[] = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: "dashboard",
    label: "Dashboard",
  },
  {
    title: "Assets",
    href: "/dashboard/assets",
    icon: "assets",
    label: "Assets",
  },
  {
    title: "Usage",
    href: "/dashboard/usage",
    icon: "gauge",
    label: "Usage",
  },
  {
    title: "Profile",
    href: "/dashboard/profile",
    icon: "user",
    label: "Profile",
  },
  {
    title: "Settings",
    href: "/dashboard/settings",
    icon: "settings",
    label: "Settings",
  },
];

type SidebarProps = {
  className?: string;
};

export default function Sidebar({ className }: SidebarProps) {
  return (
    <nav
      className={cn(
        `relative hidden h-screen flex-none border-r z-10 pt-20 md:block w-72`,
        className
      )}
    >
      <ScrollArea className="h-full">
        <div className="space-y-4 py-4">
          <div className="px-3 py-2">
            <div className="mt-3 space-y-1">
              <DashboardNav items={navItems} />
            </div>
          </div>
        </div>
      </ScrollArea>
    </nav>
  );
}
