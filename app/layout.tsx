import type { Metadata } from "next";
import { Inter, Space_Grotesk, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space-grotesk",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "SmartCattle — Intelligent Cattle Health Operations",
  description:
    "QR-based operational cattle health intelligence platform for dairy farmers, field veterinarians, and livestock administrators.",
  keywords: "cattle health, dairy operations, veterinary triage, QR livestock, CHDI model, livestock telemetry",
  openGraph: {
    title: "SmartCattle — Precision Livestock Health",
    description: "Operational QR-based cattle health management & clinical triage",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${spaceGrotesk.variable} ${jetbrainsMono.variable}`}
      suppressHydrationWarning
    >
      <body className="font-sans antialiased bg-slate-900/5 text-slate-900 selection:bg-emerald-600 selection:text-white" suppressHydrationWarning>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
