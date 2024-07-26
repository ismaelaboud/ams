"use client";

import LoginForm from "@/components/auth/Login-Form";
import { useAuth } from "@/contexts/auth";
import { redirect } from "next/navigation";
import { useEffect } from "react";

export default function Login() {
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      redirect("/dashboard");
    }
  }, [user]);
  return (
    <>
      <main>
        <LoginForm />
      </main>
    </>
  );
}
