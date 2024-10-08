"use client";

import Link from "next/link";
import { Plus } from "lucide-react";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import AssetUpdateForm from "@/components/dashboard/asset-edit-form";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useAuth } from "@/contexts/auth";

export default function EditAsset({ params }: { params: { id: string } }) {
  const { user } = useAuth();

  return (
    <ScrollArea className="h-full">
      <div className="flex-1 space-y-4  p-4 pt-6 md:p-8">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Update asset</h2>
            <p className="text-sm text-muted-foreground tracking-tight">
              Update/Edit asset here
            </p>
          </div>
          {user?.role !== "ADMIN" ? (
            ""
          ) : (
            <Link
              href={"/dashboard/assets"}
              className={cn(buttonVariants({ variant: "default" }))}
            >
              <Plus className="mr-2 h-4 w-4" /> Add Asset
            </Link>
          )}
        </div>
        <Separator />
        <AssetUpdateForm params={params} />
      </div>
    </ScrollArea>
  );
}
