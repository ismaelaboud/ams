import Link from "next/link";
import { Plus } from "lucide-react";
import { cn } from "@/lib/utils";
import { Asset } from "@/components/tables/assets/columns";
import AssetsTable from "@/components/tables/assets/data-table";
import { buttonVariants } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

const data: Asset[] = [
  {
    id: "1",
    name: "Laptop",
    description: "A high-performance laptop for office work",
    serialNumber: "AS123456789",
    category: "electronics",
  },
  {
    id: "2",
    name: "Office Chair",
    description: "Ergonomic office chair",
    serialNumber: "AS987654321",
    category: "furniture",
  },
  {
    id: "3",
    name: "Printer",
    description: "All-in-one printer",
    serialNumber: "AS234567890",
    category: "electronics",
  },
  {
    id: "4",
    name: "Desk",
    description: "Large office desk",
    serialNumber: "AS876543210",
    category: "furniture",
  },
  {
    id: "5",
    name: "Monitor",
    description: "24-inch monitor",
    serialNumber: "AS345678901",
    category: "electronics",
  },
  {
    id: "6",
    name: "Notebook",
    description: "Spiral notebook for notes",
    serialNumber: "AS765432109",
    category: "office-supplies",
  },
  {
    id: "7",
    name: "Whiteboard",
    description: "Wall-mounted whiteboard",
    serialNumber: "AS654321098",
    category: "furniture",
  },
  {
    id: "8",
    name: "Smartphone",
    description: "Latest model smartphone",
    serialNumber: "AS456789012",
    category: "electronics",
  },
  {
    id: "9",
    name: "Pen",
    description: "Ballpoint pen",
    serialNumber: "AS543210987",
    category: "office-supplies",
  },
  {
    id: "10",
    name: "Tablet",
    description: "High-resolution tablet",
    serialNumber: "AS567890123",
    category: "electronics",
  },
  {
    id: "11",
    name: "Filing Cabinet",
    description: "Metal filing cabinet",
    serialNumber: "AS432109876",
    category: "furniture",
  },
  {
    id: "12",
    name: "Keyboard",
    description: "Mechanical keyboard",
    serialNumber: "AS678901234",
    category: "electronics",
  },
  {
    id: "13",
    name: "Paper",
    description: "Ream of A4 paper",
    serialNumber: "AS321098765",
    category: "office-supplies",
  },
  {
    id: "14",
    name: "Conference Table",
    description: "Large conference table",
    serialNumber: "AS210987654",
    category: "furniture",
  },
  {
    id: "15",
    name: "Mouse",
    description: "Wireless mouse",
    serialNumber: "AS789012345",
    category: "electronics",
  },
];

export default async function Assets() {
  return (
    <>
      <div className="flex-1 space-y-4  p-4 pt-6 md:p-8">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Assets</h2>
            <p className="text-sm text-muted-foreground tracking-tight">
              Manage all assets
            </p>
          </div>

          <Link
            href={"/dashboard/assets/new"}
            className={cn(buttonVariants({ variant: "default" }))}
          >
            <Plus className="mr-2 h-4 w-4" /> New Asset
          </Link>
        </div>
        <Separator />

        <AssetsTable data={data} />
      </div>
    </>
  );
}
