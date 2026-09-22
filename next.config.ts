import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow SVG and image handling
  images: {
    remotePatterns: [],
  },
  // Suppress Recharts and other peer dep warnings
  serverExternalPackages: ["@prisma/client", "prisma"],
};

export default nextConfig;
