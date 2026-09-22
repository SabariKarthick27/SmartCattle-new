import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "SmartCattle — Intelligent Cattle Health Management",
  description:
    "QR-based cattle health management system for smallholder dairy farmers in India. Real-time CHDI scoring, vet coordination, and regional outbreak alerts.",
  keywords: "cattle health, dairy farmers, QR management, veterinary, CHDI, India",
  openGraph: {
    title: "SmartCattle",
    description: "Intelligent QR-based cattle health management",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable} suppressHydrationWarning>
      <body className="font-sans antialiased" suppressHydrationWarning>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
