"use client";

import Link from "next/link";
import { Plus } from "lucide-react";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import ThemeToggle from "@/components/theme/theme-toggle";
import { useAuth } from "@/contexts/auth";

export default function Settings() {
  const { user } = useAuth();
  return (
    <>
      <div className="flex-1 space-y-4  p-4 pt-6 md:p-8">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
            <p className="text-sm text-muted-foreground tracking-tight">
              Change app theme here
            </p>
          </div>
          {user?.role !== "ADMIN" ? (
            ""
          ) : (
            <Link
              href={"/dashboard/assets/new"}
              className={cn(buttonVariants({ variant: "default" }))}
            >
              <Plus className="mr-2 h-4 w-4" /> New Asset
            </Link>
          )}
        </div>
        <Separator />

        <ThemeToggle />
      </div>
    </>
  );
}
