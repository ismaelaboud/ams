import { Asset } from "@/components/tables/assets/columns";
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const sortAssetsByDateAdded = (assets: Asset[]): Asset[] => {
  return assets.sort((a, b) => {
    const dateA = new Date(a?.dateRecorded ?? 0).getTime();
    const dateB = new Date(b?.dateRecorded ?? 0).getTime();
    return dateB - dateA;
  });
};
