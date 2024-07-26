"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import Logo from "@/components/sharable/logo";
import SectionOverlay from "@/components/section-overlay";
import { AlignJustify } from "lucide-react";
import { useAuth } from "@/contexts/auth";

export default function Home() {
  const { user } = useAuth();

  return (
    <>
      <header className="container border-b py-4">
        <div className="flex justify-between items-center">
          <Logo />
          <nav className="hidden sm:block">
            {user ? (
              <Link href="/dashboard">
                <Button>Explore Dashboard</Button>
              </Link>
            ) : (
              <ul className="flex items-center gap-x-6">
                <li>
                  <Link
                    href="/"
                    className="text-muted-foreground hover:text-foreground duration-200 ease-in"
                  >
                    Home
                  </Link>
                </li>
                <li>
                  <Link
                    href="/login"
                    className="text-muted-foreground hover:text-foreground duration-200 ease-in"
                  >
                    Login
                  </Link>
                </li>
                <li>
                  <Link href="/register">
                    <Button>Register</Button>
                  </Link>
                </li>
              </ul>
            )}
          </nav>
          <div className="sm:hidden">
            <Sheet>
              <SheetTrigger>
                <AlignJustify size={20} className="cursor-pointer" />
              </SheetTrigger>
              <SheetContent side="bottom" className="rounded-t-3xl">
                {user ? (
                  <Link href="/dashboard">
                    <Button>Explore Dashboard</Button>
                  </Link>
                ) : (
                  <ul className="flex flex-col gap-y-6">
                    <li>
                      <Link
                        href="/"
                        className="text-muted-foreground hover:text-foreground duration-200 ease-in"
                      >
                        Home
                      </Link>
                    </li>
                    <li>
                      <Link
                        href="/login"
                        className="text-muted-foreground hover:text-foreground duration-200 ease-in"
                      >
                        Login
                      </Link>
                    </li>
                    <li>
                      <Link href="/register">
                        <Button>Register</Button>
                      </Link>
                    </li>
                  </ul>
                )}
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </header>

      <SectionOverlay bgImage="bg-hero">
        <section className="container relative flex py-20 sm:py-32">
          <div className="w-full max-w-3xl">
            <h2 className="text-5xl md:text-7xl font-bold mb-6 text-background">
              Swahilipot Hub Asset Management System
            </h2>
            <p className="mb-10 text-lg text-background">
              Login to access Swahilipot Hub Asset Management system.
            </p>
            {user ? (
              <Link href="/dashboard">
                <Button size="lg">Explore Dashboard</Button>
              </Link>
            ) : (
              <Link href="/login">
                <Button size="lg">Login</Button>
              </Link>
            )}
          </div>
        </section>
      </SectionOverlay>
      <footer className="py-4 container">
        <small className="block px-6 text-center text-sm text-muted-foreground">
          &copy; 2024 SPH Asset Management. All rights reserved.
        </small>
      </footer>
    </>
  );
}
