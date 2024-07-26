"use client";

import ThemeProvider from "@/components/theme/theme-provider";
import AuthProvider from "@/contexts/auth";

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <>
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
        <AuthProvider>{children}</AuthProvider>
      </ThemeProvider>
    </>
  );
}
