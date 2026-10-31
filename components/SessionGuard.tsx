"use client";

import { useEffect } from "react";
import { useSession } from "next-auth/react";

interface SessionGuardProps {
  requiredRole?: "farmer" | "vet" | "admin";
}

export default function SessionGuard({ requiredRole }: SessionGuardProps) {
  const { data: session, status } = useSession();

  useEffect(() => {
    // 1. Detect Back-Forward Cache (bfcache) restoration
    const handlePageShow = (event: PageTransitionEvent) => {
      if (event.persisted) {
        // Page was loaded from memory cache (e.g. user pressed back button after logout)
        // Hard reload forces middleware execution and fresh session check
        window.location.reload();
      }
    };

    // 2. Detect popstate navigation (user clicking back/forward buttons)
    const handlePopState = () => {
      if (status === "unauthenticated") {
        window.location.replace("/");
      }
    };

    window.addEventListener("pageshow", handlePageShow);
    window.addEventListener("popstate", handlePopState);

    return () => {
      window.removeEventListener("pageshow", handlePageShow);
      window.removeEventListener("popstate", handlePopState);
    };
  }, [status]);

  useEffect(() => {
    // If NextAuth determines user is no longer logged in, immediately redirect to landing page
    if (status === "unauthenticated") {
      window.location.replace("/");
    } else if (status === "authenticated" && requiredRole && session?.user?.role !== requiredRole) {
      window.location.replace("/");
    }
  }, [status, session, requiredRole]);

  return null;
}
