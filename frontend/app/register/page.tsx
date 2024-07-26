"use client";

import RegisterForm from "@/components/auth/register-form";
import { useAuth } from "@/contexts/auth";
import { redirect } from "next/navigation";
import { useEffect } from "react";

export default function Register() {
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      redirect("/dashboard");
    }
  }, [user]);

  return (
    <>
      <RegisterForm />
    </>
  );
}
