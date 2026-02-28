import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "JARVIS - Personal AI Operating System",
  description: "Multi-modal AI operating system with voice, memory, and task execution",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        suppressHydrationWarning
        className="bg-deep-space text-text-primary antialiased"
      >
        {children}
      </body>
    </html>
  );
}
