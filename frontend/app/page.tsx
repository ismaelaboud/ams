"use client";

import Link from "next/link";
import { redirect } from "next/navigation";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import  RegistrationForm from "@/components/Registration/RegistrationForm";

export default function Home() {
  useEffect(() => {
    redirect("/login");
  }, []);

  return (
    <main className="grid place-items-center h-screen p-24">
      <Link href="/login">
        <Button>Login First</Button>
      </Link>
      <RegistrationForm />
      <Button>Contribute</Button>
    </main>
  );
}
