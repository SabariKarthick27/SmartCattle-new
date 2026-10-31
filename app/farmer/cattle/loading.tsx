export default function CattleListLoading() {
  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 animate-pulse">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div className="space-y-2">
          <div className="h-7 w-40 bg-slate-200 rounded"></div>
          <div className="h-4 w-72 bg-slate-100 rounded"></div>
        </div>
        <div className="h-9 w-32 bg-slate-200 rounded-lg"></div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="card p-4 bg-white border border-slate-200 rounded-xl space-y-3">
            <div className="flex items-start justify-between">
              <div className="w-10 h-10 bg-slate-100 rounded-lg"></div>
              <div className="h-5 w-20 bg-slate-100 rounded-full"></div>
            </div>
            <div className="space-y-1.5">
              <div className="h-5 w-36 bg-slate-200 rounded"></div>
              <div className="h-3 w-48 bg-slate-100 rounded"></div>
            </div>
            <div className="grid grid-cols-2 gap-2 pt-2">
              <div className="h-12 bg-slate-50 border border-slate-100 rounded"></div>
              <div className="h-12 bg-slate-50 border border-slate-100 rounded"></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
