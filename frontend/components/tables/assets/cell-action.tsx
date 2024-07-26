"use client";

import { apiUrl } from "@/lib/axios";
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
import { useAuth } from "@/contexts/auth";
import { Asset } from "./columns";

export const CellAction = ({ asset }: { asset: Asset }) => {
  const router = useRouter();
  const { user } = useAuth();

  const deleteAsset = async (id: number) => {
    const accessToken = localStorage.getItem("access");
    try {
      await apiUrl.delete(`/assets/detail/${id}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      router.push("/dashboard/assets");
    } catch (error: any) {
      console.log(error);
    }
  };

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
        {user?.role !== "ADMIN" ? (
          ""
        ) : (
          <>
            {" "}
            <DropdownMenuItem
              onClick={() => router.push(`/dashboard/assets/${asset?.id}/edit`)}
            >
              <Pencil className="mr-2" size={15} />
              Update asset
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => deleteAsset(asset?.id as number)}>
              <Trash className="mr-2" size={15} />
              Delete asset
            </DropdownMenuItem>
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
