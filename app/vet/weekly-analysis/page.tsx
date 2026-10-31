import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import prisma from "@/lib/prisma";
import { generateBatchWeeklyHealthAnalysis } from "@/lib/chdi/weekly-analysis";
import VetWeeklyAnalysisClient from "./VetWeeklyAnalysisClient";

export default async function VetWeeklyAnalysisPage() {
  const session = await getServerSession(authOptions);
  const vetRegion = session?.user?.assignedRegion;

  let validReports: any[] = [];
  let errorMsg: string | null = null;

  try {
    validReports = await generateBatchWeeklyHealthAnalysis(vetRegion);
  } catch (err: any) {
    console.error("[Weekly Analysis DB Connection Error]", err);
    errorMsg = "Database server is connecting or temporarily busy. Please refresh to retry.";
  }

  if (errorMsg) {
    return (
      <div className="p-8 max-w-4xl space-y-4">
        <div className="card p-6 border-l-4 border-l-amber-500 bg-amber-50/50">
          <h2 className="text-lg font-bold text-amber-900 mb-2">Database Connection Re-connecting</h2>
          <p className="text-amber-800 text-sm mb-4">{errorMsg}</p>
          <a href="/vet/weekly-analysis" className="btn-primary inline-flex items-center gap-2">
            🔄 Refresh & Retry Page
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6 max-w-6xl">
      <VetWeeklyAnalysisClient initialReports={validReports} vetRegion={vetRegion} />
    </div>
  );
}
