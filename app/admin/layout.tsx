import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import { redirect } from "next/navigation";
import AdminSidebar from "@/components/AdminSidebar";

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const session = await getServerSession(authOptions);
  if (!session || session.user.role !== "admin") redirect("/login");

  return (
    <div className="min-h-screen bg-[#f6f8f7] flex">
      <AdminSidebar
        userName={session.user.name}
        userEmail={session.user.email}
        userImage={session.user.image}
      />
      <main className="flex-1 md:ml-60 min-h-screen pt-14 md:pt-0">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}

