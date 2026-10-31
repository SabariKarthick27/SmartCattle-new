export default function VetCaseLoading() {
  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-5xl mx-auto animate-pulse">
      <div className="h-4 w-36 bg-slate-200 rounded"></div>

      {/* Header skeleton */}
      <div className="flex items-center gap-3.5">
        <div className="w-12 h-12 bg-slate-200 rounded-xl"></div>
        <div className="space-y-2">
          <div className="h-6 w-48 bg-slate-200 rounded"></div>
          <div className="h-3 w-64 bg-slate-200 rounded"></div>
        </div>
      </div>

      {/* Case Summary Card skeleton */}
      <div className="card p-5 bg-white border border-slate-200 rounded-xl space-y-4">
        <div className="h-5 w-40 bg-slate-200 rounded"></div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div className="h-10 bg-slate-100 rounded"></div>
          <div className="h-10 bg-slate-100 rounded"></div>
          <div className="h-10 bg-slate-100 rounded"></div>
        </div>
        <div className="h-16 bg-slate-100 rounded"></div>
      </div>

      {/* Diagnosis form skeleton */}
      <div className="card p-6 bg-white border border-slate-200 rounded-xl space-y-4">
        <div className="h-5 w-48 bg-slate-200 rounded"></div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="h-9 bg-slate-100 rounded"></div>
          <div className="h-9 bg-slate-100 rounded"></div>
          <div className="h-9 bg-slate-100 rounded"></div>
        </div>
        <div className="h-24 bg-slate-100 rounded"></div>
      </div>
    </div>
  );
}

