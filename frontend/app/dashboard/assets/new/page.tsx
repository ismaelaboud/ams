import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import AssetAddForm from "@/components/dashboard/asset-add-form";
import { ScrollArea } from "@/components/ui/scroll-area";

export default async function NewAsset() {
  return (
    <ScrollArea className="h-full">
      <div className="flex-1 space-y-4  p-4 pt-6 md:p-8">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">New asset</h2>
            <p className="text-sm text-muted-foreground tracking-tight">
              Add a new asset here
            </p>
          </div>
          <Link
            href={"/dashboard/assets"}
            className={cn(buttonVariants({ variant: "default" }))}
          >
            View Assets <ChevronRight className="ml-2 h-4 w-4" />
          </Link>
        </div>
        <Separator />
        <AssetAddForm />
      </div>
    </ScrollArea>
  );
}
