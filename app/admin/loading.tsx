export default function AdminLoading() {
  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-7xl mx-auto animate-pulse">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div className="space-y-2">
          <div className="h-7 w-60 bg-slate-200 rounded"></div>
          <div className="h-4 w-80 bg-slate-100 rounded"></div>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="card p-3.5 bg-white border border-slate-200 rounded-xl space-y-2">
            <div className="h-3 w-12 bg-slate-100 rounded"></div>
            <div className="h-7 w-16 bg-slate-200 rounded"></div>
            <div className="h-3 w-20 bg-slate-100 rounded"></div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 space-y-3">
          <div className="card p-4 bg-white border border-slate-200 rounded-xl space-y-3">
            <div className="h-4 w-44 bg-slate-200 rounded"></div>
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-14 bg-slate-100 rounded-lg"></div>
            ))}
          </div>
        </div>
        <div className="lg:col-span-5 space-y-3">
          <div className="card p-4 bg-white border border-slate-200 rounded-xl space-y-3">
            <div className="h-4 w-44 bg-slate-200 rounded"></div>
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-10 bg-slate-100 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
