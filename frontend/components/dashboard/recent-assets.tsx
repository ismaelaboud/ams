import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Asset } from "../tables/assets/columns";

export function RecentAssets({ asset }: { asset: Asset }) {
  return (
    <div className="space-y-8 mb-8">
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/assets/avatars/avatar11.jpg" alt="Avatar" />
          <AvatarFallback>
            {asset?.name?.slice(0, 2)?.toUpperCase()}
          </AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">{asset?.name}</p>
          <p className="text-sm text-muted-foreground">{asset?.serialNumber}</p>
        </div>
        <div className="ml-auto text-muted-foreground text-sm">
          {asset?.category?.name}
        </div>
      </div>
    </div>
  );
}
