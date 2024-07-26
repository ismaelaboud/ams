import Link from "next/link";
import Image from "next/image";

export default function Logo() {
  return (
    <>
      <Link href="/" className="flex gap-2 items-center">
        <Image
          src="/assets/logo.png"
          alt="sph_logo"
          width={200}
          height={50}
          className="w-full block max-w-[150px] h-6"
        />
        <span className="text-xl mb-2 text-primary font-bold border-l-2 pl-2 border-primary">
          AMS
        </span>
      </Link>
    </>
  );
}
