import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export function RecentAssets() {
  return (
    <div className="space-y-8 mb-8">
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/assets/avatars/avatar1.jpg" alt="Avatar" />
          <AvatarFallback>SC</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Sony Camera</p>
          <p className="text-sm text-muted-foreground">AS7634164705</p>
        </div>
        <div className="ml-auto text-muted-foreground text-sm">Electronics</div>
      </div>
    </div>
  );
}
