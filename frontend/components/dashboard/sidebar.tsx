"use client";
import React, { useState } from "react";
import { DashboardNav } from "@/components/dashboard/dashboard-nav";
import { NavItem } from "@/types";
import { cn } from "@/lib/utils";
import { ChevronLeft } from "lucide-react";
import { useSidebar } from "@/hooks/useSidebar";

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
  const { isMinimized, toggle } = useSidebar();
  const [status, setStatus] = useState(false);

  const handleToggle = () => {
    setStatus(true);
    toggle();
    setTimeout(() => setStatus(false), 500);
  };
  return (
    <nav
      className={cn(
        `relative hidden h-screen flex-none border-r z-10 pt-20 md:block`,
        status && "duration-500",
        !isMinimized ? "w-72" : "w-[72px]",
        className
      )}
    >
      <ChevronLeft
        className={cn(
          "absolute -right-3 top-20 cursor-pointer rounded-full border bg-background text-3xl text-foreground",
          isMinimized && "rotate-180"
        )}
        onClick={handleToggle}
      />
      <div className="space-y-4 py-4">
        <div className="px-3 py-2">
          <div className="mt-3 space-y-1">
            <DashboardNav items={navItems} />
          </div>
        </div>
      </div>
    </nav>
  );
}
