"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Plus } from "lucide-react";
import { cn, sortAssetsByDateAdded } from "@/lib/utils";
import { Asset } from "@/components/tables/assets/columns";
import AssetsTable from "@/components/tables/assets/data-table";
import { buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { apiUrl } from "@/lib/axios";
import { useAuth } from "@/contexts/auth";

export default function ElectronicsAssets() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const { user } = useAuth();

  useEffect(() => {
    const fetchAllAssets = async () => {
      const accessToken = localStorage.getItem("access");
      try {
        const { data } = await apiUrl.get(
          "/assets-by-category/?category_name=Office Supplies",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        const allOfficeAsupplies = sortAssetsByDateAdded(data?.results);
        setAssets(allOfficeAsupplies);
        // console.log(data);
      } catch (error: any) {
        console.log(error);
      }
    };
    fetchAllAssets();
  }, []);

  return (
    <>
      <div className="flex-1 space-y-4  p-4 pt-6 md:p-8">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Assets</h2>
            <p className="text-sm text-muted-foreground tracking-tight">
              Manage all office supplies assets
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

        <AssetsTable data={assets} />
      </div>
    </>
  );
}
