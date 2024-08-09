"use client";

import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button, buttonVariants } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Asset } from "@/components/tables/assets/columns";
import { useEffect, useState } from "react";
import { apiUrl } from "@/lib/axios";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/auth";

export default function ViewAsset({ params }: { params: { id: string } }) {
  const [asset, setAsset] = useState<Asset>();
  const [deleting, setDeleting] = useState<boolean>(false);
  const router = useRouter();
  const { user } = useAuth();

  useEffect(() => {
    const fetchAsset = async () => {
      const accessToken = localStorage.getItem("access");
      try {
        const { data } = await apiUrl.get(/assets/detail/${params?.id}, {
          headers: {
            Authorization: Bearer ${accessToken},
          },
        });
        setAsset(data);
      } catch (error: any) {
        console.log(error);
      }
    };
    fetchAsset();
  }, [params?.id]);

  const deleteAsset = async (id: number) => {
    const accessToken = localStorage.getItem("access");
    try {
      setDeleting(true);
      await apiUrl.delete(/assets/detail/${id}, {
        headers: {
          Authorization: Bearer ${accessToken},
        },
      });
      setDeleting(false);
      router.push("/dashboard/assets");
    } catch (error: any) {
      console.log(error);
      setDeleting(false);
    }
  };

  return (
    <ScrollArea className="h-full">
      <div className="flex-1 space-y-4  p-4 pt-6 md:p-8">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">View asset</h2>
            <p className="text-sm text-muted-foreground tracking-tight">
              View asset details here
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
        <div className="mb-4">
          <div>
            <span className="font-medium mr-2">Asset name:</span>
            <span className="text-sm text-muted-foreground">{asset?.name}</span>
          </div>
          <div>
            <span className="font-medium mr-2">Asset type:</span>
            <span className="text-sm text-muted-foreground">
              {asset?.assetType}
            </span>
          </div>
          <div>
            <span className="font-medium mr-2">Asset serial number:</span>
            <span className="text-sm text-muted-foreground">
              {asset?.serialNumber}
            </span>
          </div>
          <div className="mb-4">
            <span className="font-medium mr-2">Category:</span>
            <span className="text-sm text-muted-foreground">
              {asset?.category?.name}
            </span>
          </div>
          <div className="mb-4">
            <span className="font-medium mr-2">Status:</span>
            <span className="text-sm text-muted-foreground">
              {asset?.status}
            </span>
          </div>
          <div className="mb-4">
            <span className="font-medium mr-2">Date recorded:</span>
            <span className="text-sm text-muted-foreground">
              {new Date(asset?.dateRecorded ?? "")?.toLocaleString()}
            </span>
          </div>
          <div className="mb-4">
            <span className="font-medium mr-2">Description:</span>
            <span className="text-sm text-muted-foreground">
              {asset?.description}
            </span>
          </div>
        </div>
        {user?.role !== "ADMIN" ? (
          ""
        ) : (
          <div className="flex items-center gap-x-3 mt-6">
            <Button
              onClick={() =>
                router?.push(/dashboard/assets/${asset?.id}/edit)
              }
            >
              Edit
            </Button>

            <Button
              disabled={deleting}
              aria-disabled={deleting}
              variant="destructive"
              onClick={() => deleteAsset(asset?.id as number)}
            >
              {deleting ? "Deleting..." : "Delete"}
            </Button>
          </div>
        )}
      </div>
    </ScrollArea>
  );
}
