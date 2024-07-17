import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function PageNotFound() {
  return (
    <>
      <main>
        <section className="grid h-screen place-items-center">
          <div className="flex flex-col items-center gap-6">
            <Image
              src="/assets/illustration_404.svg"
              alt="404_image"
              width={500}
              height={500}
            />
            <p className="text-muted-foreground font-bold">
              Looks like you&apos;re lost
            </p>
            <Link href="/dashboard">
              <Button>Explore dashboard</Button>
            </Link>
          </div>
        </section>
      </main>
    </>
  );
}
