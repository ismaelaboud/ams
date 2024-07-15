import Link from "next/link";
import { Home } from "lucide-react";

export default function Logo() {
  return (
    <>
      <Link href="/" className="flex gap-2 !items-center">
        <Home size={18} />
        <h2 className="text-lg p-0 m-0 text-primary font-bold">SPH-AMS</h2>
      </Link>
    </>
  );
}
