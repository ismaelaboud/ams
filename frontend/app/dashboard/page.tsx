"use client";

import Link from "next/link";
import {
  Boxes,
  CircuitBoard,
  Sofa,
  Eye,
  ChevronRight,
  Plus,
  Printer,
} from "lucide-react";
import { Button, buttonVariants } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { RecentAssets } from "@/components/dashboard/recent-assets";
import { PopularCategories } from "@/components/dashboard/popular-categories";
import { cn, sortAssetsByDateAdded } from "@/lib/utils";
import { useAuth } from "@/contexts/auth";
import { useEffect, useState } from "react";
import { redirect } from "next/navigation";
import { Asset } from "@/components/tables/assets/columns";
import { apiUrl } from "@/lib/axios";

export default function Dashboard() {
  const { user } = useAuth();
  const [assets, setAssets] = useState<number>(0);
  const [allAssets, setAllAssets] = useState<Asset[]>([]);
  const [furnitures, setFurnitures] = useState<number>(0);
  const [electronics, setElectronics] = useState<number>(0);
  const [officeSupplies, setOfficeSupplies] = useState<number>(0);

  useEffect(() => {
    if (!user || user === undefined) {
      redirect("/login");
    }
  }, [user]);

  useEffect(() => {
    const fetchAllAssets = async () => {
      const accessToken = localStorage.getItem("access");
      try {
        const { data } = await apiUrl.get("/assets-by-category/", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        setAssets(data?.count);

        const allAssets = sortAssetsByDateAdded(data?.results);
        setAllAssets(allAssets);
        // console.log(data);
      } catch (error: any) {
        console.log(error);
      }
    };

    const fetchAllFurnitureAssets = async () => {
      const accessToken = localStorage.getItem("access");
      try {
        const { data } = await apiUrl.get(
          "/assets-by-category/?category_name=Furnitures",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setFurnitures(data?.count);
        // console.log(data);
      } catch (error: any) {
        console.log(error);
      }
    };

    const fetchAllElectronicsAssets = async () => {
      const accessToken = localStorage.getItem("access");
      try {
        const { data } = await apiUrl.get(
          "/assets-by-category/?category_name=Electronics",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        setElectronics(data?.count);
        // console.log(data);
      } catch (error: any) {
        console.log(error);
      }
    };

    const fetchAllOfficeSuppliesAssets = async () => {
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
        setOfficeSupplies(data?.count);
        // console.log(data);
      } catch (error: any) {
        console.log(error);
      }
    };

    fetchAllAssets();
    fetchAllFurnitureAssets();
    fetchAllElectronicsAssets();
    fetchAllOfficeSuppliesAssets();
  }, []);

  return (
    <ScrollArea className="h-full">
      <div className="flex-1 space-y-4 p-4 pt-6 md:p-8">
        <div className="flex items-center justify-between ">
          <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
          {user?.role !== "ADMIN" ? (
            ""
          ) : (
            <Link
              href={"/dashboard/assets/new"}
              className={cn(buttonVariants({ variant: "default" }))}
            >
              <Plus className="mr-2 h-4 w-4" /> Add Asset
            </Link>
          )}
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Assets
              </CardTitle>
              <Boxes className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{assets ?? 0}</div>
              <p className="text-xs text-muted-foreground">from database</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Electronics
              </CardTitle>
              <CircuitBoard className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{electronics ?? 0}</div>
              <p className="text-xs text-muted-foreground">from database</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total furnitures
              </CardTitle>
              <Sofa className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{furnitures ?? 0}</div>
              <p className="text-xs text-muted-foreground">from database</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total office supplies
              </CardTitle>
              <Printer className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{officeSupplies ?? 0}</div>
              <p className="text-xs text-muted-foreground">from database</p>
            </CardContent>
          </Card>
        </div>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-7">
          <Card className="col-span-4">
            <CardHeader>
              <CardTitle>Recent Assets</CardTitle>
              <CardDescription>
                Some of the assets added recently
              </CardDescription>
            </CardHeader>
            <CardContent>
              {allAssets?.slice(0, 4)?.map((asset: Asset) => (
                <RecentAssets key={asset?.id} asset={asset} />
              ))}
            </CardContent>
          </Card>
          <Card className="col-span-4 md:col-span-3">
            <CardHeader>
              <CardTitle>Popular Categories</CardTitle>
              <CardDescription>
                Explore categories with more assets
              </CardDescription>
            </CardHeader>
            <CardContent>
              <PopularCategories />
            </CardContent>
          </Card>
        </div>
      </div>
    </ScrollArea>
  );
}
