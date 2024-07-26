import { RefreshCcw } from "lucide-react";

export default function Loading() {
  return (
    <main className="h-screen grid place-items-center">
      <div className="text-primary animate-spin">
        <RefreshCcw size={60} />
      </div>
    </main>
  );
}
