import { cn } from "@/lib/utils";
import { MobileSidebar } from "./mobile-sidebar";
import { UserNav } from "./user-nav";
import Logo from "../sharable/logo";

export default function Header() {
  return (
    <div className="supports-backdrop-blur:bg-background/60 fixed left-0 right-0 top-0 z-20 border-b bg-background/95 backdrop-blur">
      <nav className="flex h-14 items-center justify-between px-4">
        <div className={cn("block lg:!hidden")}>
          <MobileSidebar />
        </div>
        <Logo />
        <UserNav />
      </nav>
    </div>
  );
}
