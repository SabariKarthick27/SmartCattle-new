/**
 * NextAuth.js configuration
 * app/api/auth/[...nextauth]/route.ts
 */
import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import bcrypt from "bcryptjs";
import prisma from "@/lib/prisma";
import type { NextAuthOptions } from "next-auth";

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;

        const user = await prisma.user.findUnique({
          where: { email: credentials.email },
        });

        if (!user) return null;
        if (!user.isActive) return null;

        const passwordMatch = await bcrypt.compare(
          credentials.password,
          user.passwordHash
        );
        if (!passwordMatch) return null;

        // Admin must approve farmers/vets before they can log in
        if (!user.isVerified && user.role !== "admin") {
          throw new Error("PENDING_APPROVAL");
        }

        return {
          id: user.id,
          name: user.name,
          email: user.email,
          role: user.role,
          farmId: user.farmId,
          assignedRegion: user.assignedRegion,
          image: user.photoUrl || user.image || null,
        };
      },
    }),
  ],

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        const u = user as any;
        token.id = u.id;
        token.role = u.role;
        token.farmId = u.farmId;
        token.assignedRegion = u.assignedRegion;
        token.picture = u.image;
      }
      return token;
    },
    async session({ session, token }) {
      if (token && session.user) {
        session.user.id = token.id as string;
        session.user.role = token.role as string;
        session.user.farmId = token.farmId as string | null;
        session.user.assignedRegion = token.assignedRegion as string | null;
        if (token.picture) session.user.image = token.picture as string;
      }
      return session;
    },
  },

  pages: {
    signIn: "/login",
    error: "/login",
  },

  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },

  secret: process.env.NEXTAUTH_SECRET,
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
