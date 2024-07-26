import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";

export interface Category {
  title: string;
  link: string;
  sNo: string;
  image?: string;
  fallback: string;
}

const categories: Category[] = [
  {
    title: "Electronics",
    link: "/dashboard/assets/categories/electronics",
    sNo: "#1",
    image: "assets/avatars/avatar1.jpg",
    fallback: "EA",
  },
  {
    title: "Furnitures",
    link: "/dashboard/assets/categories/furnitures",
    sNo: "#2",
    image: "assets/avatars/avatar1.jpg",
    fallback: "FA",
  },
  {
    title: "Office Supplies",
    link: "/dashboard/assets/categories/office-supplies",
    sNo: "#3",
    image: "assets/avatars/avatar1.jpg",
    fallback: "OA",
  },
];

export function PopularCategories() {
  return (
    <>
      {categories?.map((category: Category) => (
        <div className="space-y-8 mb-8" key={category?.sNo}>
          <div className="flex items-center">
            <Avatar className="h-9 w-9">
              <AvatarImage src={category?.image} alt="Avatar" />
              <AvatarFallback>{category?.fallback}</AvatarFallback>
            </Avatar>
            <div className="ml-4 space-y-1">
              <p className="text-sm font-medium leading-none">
                {category?.title}
              </p>
              <p className="text-sm text-muted-foreground">{category?.sNo}</p>
            </div>
            <div className="ml-auto">
              <Link href={category?.link}>
                <Button size="sm" variant="secondary">
                  View <ChevronRight size={14} />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      ))}
    </>
  );
}
