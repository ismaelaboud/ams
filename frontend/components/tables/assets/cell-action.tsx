"use client";

import { useRouter } from "next/navigation";
import { Eye, MoreHorizontal, Pencil, Trash } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export const CellAction = ({ asset }: { asset: any }) => {
  const router = useRouter();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="h-8 w-8 p-0">
          <span className="sr-only">Open menu</span>
          <MoreHorizontal className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>Actions</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          onClick={() => router.push(`/dashboard/assets/${asset?.id}`)}
        >
          <Eye className="mr-2" size={15} />
          View asset
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() => router.push(`/dashboard/assets/${asset?.id}/edit`)}
        >
          <Pencil className="mr-2" size={15} />
          Update asset
        </DropdownMenuItem>
        <DropdownMenuItem>
          <Trash className="mr-2" size={15} />
          Delete asset
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
