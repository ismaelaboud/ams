"use client";

import { AlignJustify, LogOut } from "lucide-react";
import { useState } from "react";
import { navItems } from "./sidebar";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { ScrollArea } from "@/components/ui/scroll-area";
import { DashboardNav } from "@/components/dashboard/dashboard-nav";

export function MobileSidebar() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Sheet open={open} onOpenChange={setOpen}>
        <SheetTrigger asChild>
          <AlignJustify size={20} className="cursor-pointer" />
        </SheetTrigger>
        <SheetContent side="left" className="!px-0">
          <ScrollArea className="h-full">
            <div className="space-y-4 py-4">
              <div className="px-3 py-2">
                <h2 className="mb-6 px-4 text-lg font-semibold tracking-tight">
                  Overview
                </h2>
                <div className="space-y-1">
                  <DashboardNav items={navItems} setOpen={setOpen} />
                </div>
              </div>
            </div>
          </ScrollArea>
        </SheetContent>
      </Sheet>
    </>
  );
}
