"use client";

import Link from "next/link";
import { Plus } from "lucide-react";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import ProfileDetails from "@/components/dashboard/profile";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAuth } from "@/contexts/auth";

export default function Profile() {
  const { user } = useAuth();

  return (
    <ScrollArea className="h-full">
      <div className="flex-1 space-y-4  p-4 pt-6 md:p-8">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Profile</h2>
            <p className="text-sm text-muted-foreground tracking-tight">
              View or update your profile
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
        <ProfileDetails />
      </div>
    </ScrollArea>
  );
}
