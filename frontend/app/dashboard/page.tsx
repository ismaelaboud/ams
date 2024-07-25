import Link from "next/link";
import {
  Boxes,
  CircuitBoard,
  Sofa,
  Eye,
  ChevronRight,
  Plus,
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
import { cn } from "@/lib/utils";

export default function Dashboard() {
  return (
    <ScrollArea className="h-full">
      <div className="flex-1 space-y-4 p-4 pt-6 md:p-8">
        <div className="flex items-center justify-between ">
          <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
          <Link
            href={"/dashboard/assets/new"}
            className={cn(buttonVariants({ variant: "default" }))}
          >
            <Plus className="mr-2 h-4 w-4" /> Add Asset
          </Link>
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
              <div className="text-2xl font-bold">300</div>
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
              <div className="text-2xl font-bold">150</div>
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
              <div className="text-2xl font-bold">100</div>
              <p className="text-xs text-muted-foreground">from database</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                View all assets
              </CardTitle>
              <Eye className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <Link href="/dashboard/assets">
                <Button size="sm" variant="secondary">
                  View all <ChevronRight size={14} />
                </Button>
              </Link>
              <p className="text-xs mt-1 text-muted-foreground">
                from database
              </p>
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
              <RecentAssets />
              <RecentAssets />
              <RecentAssets />
              <RecentAssets />
              <RecentAssets />
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
