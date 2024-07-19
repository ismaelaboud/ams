"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { Icons } from "@/components/dashboard/icons";
import { cn } from "@/lib/utils";
import { NavItem } from "@/types";
import { Dispatch, SetStateAction } from "react";

interface DashboardNavProps {
  items: NavItem[];
  setOpen?: Dispatch<SetStateAction<boolean>>;
}

export function DashboardNav({ items, setOpen }: DashboardNavProps) {
  const path = usePathname();

  if (!items?.length) {
    return null;
  }

  return (
    <nav className="grid items-start gap-2">
      <div>
        {items.map((item, index) => {
          const Icon = Icons[item.icon || "arrowRight"];
          return (
            item.href && (
              <Link
                key={index}
                href={item.disabled ? "/" : item.href}
                className={cn(
                  "flex items-center gap-2 overflow-hidden rounded-md mb-3 py-3 text-sm font-medium hover:bg-accent hover:text-accent-foreground",
                  path === item.href ? "bg-accent" : "transparent",
                  item.disabled && "cursor-not-allowed opacity-80"
                )}
                onClick={() => {
                  if (setOpen) setOpen(false);
                }}
              >
                <Icon className={`ml-3 size-5`} />
                <span className="mr-2 truncate">{item.title}</span>
              </Link>
            )
          );
        })}
      </div>
    </nav>
  );
}
