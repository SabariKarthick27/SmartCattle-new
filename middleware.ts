import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { getToken } from "next-auth/jwt";

// Route prefix → allowed roles
const ROUTE_ROLES: Record<string, string[]> = {
  "/farmer": ["farmer"],
  "/vet": ["vet"],
  "/admin": ["admin"],
};

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Find which protected prefix this matches
  const protectedPrefix = Object.keys(ROUTE_ROLES).find((prefix) =>
    pathname.startsWith(prefix)
  );

  if (!protectedPrefix) {
    return NextResponse.next();
  }

  const token = await getToken({
    req: request,
    secret: process.env.NEXTAUTH_SECRET,
  });

  // Common headers to disable caching on protected routes (prevents bfcache and back-button showing cached state)
  const noCacheHeaders = {
    "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
    Pragma: "no-cache",
    Expires: "0",
  };

  // Not authenticated → redirect to login
  if (!token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    const redirectResponse = NextResponse.redirect(loginUrl);
    Object.entries(noCacheHeaders).forEach(([key, value]) => {
      redirectResponse.headers.set(key, value);
    });
    return redirectResponse;
  }

  // Role check
  const allowedRoles = ROUTE_ROLES[protectedPrefix];
  if (!allowedRoles.includes(token.role as string)) {
    const dashboardMap: Record<string, string> = {
      farmer: "/farmer",
      vet: "/vet",
      admin: "/admin",
    };
    const correctDashboard = dashboardMap[token.role as string] ?? "/";
    const redirectResponse = NextResponse.redirect(new URL(correctDashboard, request.url));
    Object.entries(noCacheHeaders).forEach(([key, value]) => {
      redirectResponse.headers.set(key, value);
    });
    return redirectResponse;
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/farmer/:path*", "/vet/:path*", "/admin/:path*"],
};
