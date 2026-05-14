import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Neural Newz — Daily AI Intelligence",
  description: "Your daily deep-dive into AI. Neural Newz covers the latest breakthroughs, product launches, and research from the world's top AI labs — delivered as a sharp podcast and newsletter every evening.",
  openGraph: {
    title: "Neural Newz — Daily AI Intelligence",
    description: "The noise of AI, turned into signal. Subscribe for a daily podcast and newsletter.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable}`}>
      <body>{children}</body>
    </html>
  );
}
