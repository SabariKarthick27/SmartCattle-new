export default function FarmerLoading() {
  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 animate-pulse">
      {/* Header Skeleton */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div className="space-y-2">
          <div className="h-7 w-48 bg-slate-200 rounded"></div>
          <div className="h-4 w-64 bg-slate-100 rounded"></div>
        </div>
        <div className="flex gap-2">
          <div className="h-9 w-28 bg-slate-200 rounded-lg"></div>
          <div className="h-9 w-28 bg-slate-100 rounded-lg"></div>
        </div>
      </div>

      {/* Stats Skeleton */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="card p-3.5 bg-white border border-slate-200 rounded-xl space-y-2">
            <div className="h-3 w-12 bg-slate-100 rounded"></div>
            <div className="h-7 w-16 bg-slate-200 rounded"></div>
            <div className="h-3 w-20 bg-slate-100 rounded"></div>
          </div>
        ))}
      </div>

      {/* Main Grid Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-8 space-y-3">
          <div className="card p-4 bg-white border border-slate-200 rounded-xl space-y-4">
            <div className="h-5 w-40 bg-slate-200 rounded"></div>
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex items-center justify-between p-2 border-b border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-slate-100 rounded-lg"></div>
                  <div className="space-y-1.5">
                    <div className="h-4 w-32 bg-slate-200 rounded"></div>
                    <div className="h-3 w-24 bg-slate-100 rounded"></div>
                  </div>
                </div>
                <div className="h-6 w-16 bg-slate-100 rounded-full"></div>
              </div>
            ))}
          </div>
        </div>
        <div className="lg:col-span-4 space-y-4">
          <div className="card p-4 bg-white border border-slate-200 rounded-xl space-y-3">
            <div className="h-4 w-32 bg-slate-200 rounded"></div>
            <div className="h-20 bg-slate-100 rounded-lg"></div>
            <div className="h-20 bg-slate-100 rounded-lg"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
