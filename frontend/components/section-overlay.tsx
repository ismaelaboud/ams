import React from "react";

export interface SectionOverlayProps {
  bgImage: string;
  children: React.ReactNode;
}

export default function SectionOverlay({
  bgImage,
  children,
}: SectionOverlayProps) {
  return (
    <section
      className={`${bgImage} relative overflow-hidden bg-no-repeat bg-cover bg-center bg-origin-border before:absolute before:content-[''] before:bg-foreground before:w-full before:h-full before:opacity-80`}
    >
      {children}
    </section>
  );
}
