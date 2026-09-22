import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { getToken } from "next-auth/jwt";

// Route prefix → allowed roles
const ROUTE_ROLES: Record<string, string[]> = {
  "/farmer": ["farmer"],
  "/vet": ["vet"],
  "/admin": ["admin"],
};

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Find which protected prefix this matches
  const protectedPrefix = Object.keys(ROUTE_ROLES).find((prefix) =>
    pathname.startsWith(prefix)
  );

  if (!protectedPrefix) return NextResponse.next();

  const token = await getToken({
    req: request,
    secret: process.env.NEXTAUTH_SECRET,
  });

  // Not authenticated → redirect to login
  if (!token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Role check
  const allowedRoles = ROUTE_ROLES[protectedPrefix];
  if (!allowedRoles.includes(token.role as string)) {
    // Redirect to user's own dashboard
    const dashboardMap: Record<string, string> = {
      farmer: "/farmer",
      vet: "/vet",
      admin: "/admin",
    };
    const correctDashboard = dashboardMap[token.role as string] ?? "/login";
    return NextResponse.redirect(new URL(correctDashboard, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/farmer/:path*", "/vet/:path*", "/admin/:path*"],
};
