export default function CattleProfileLoading() {
  return (
    <div className="p-4 sm:p-6 lg:p-8 space-y-6 max-w-6xl mx-auto animate-pulse">
      {/* Header Skeleton */}
      <div className="flex items-start justify-between flex-wrap gap-4 pb-4 border-b border-slate-200">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 bg-slate-200 rounded-xl"></div>
          <div className="space-y-2">
            <div className="h-7 w-48 bg-slate-200 rounded"></div>
            <div className="h-4 w-64 bg-slate-100 rounded"></div>
          </div>
        </div>
        <div className="flex gap-2">
          <div className="h-9 w-24 bg-slate-200 rounded-lg"></div>
          <div className="h-9 w-24 bg-slate-100 rounded-lg"></div>
        </div>
      </div>

      {/* Hero Score Skeleton */}
      <div className="rounded-xl p-5 border border-slate-200 bg-white space-y-4">
        <div className="h-4 w-36 bg-slate-200 rounded"></div>
        <div className="flex items-end gap-4">
          <div className="h-12 w-28 bg-slate-200 rounded"></div>
          <div className="flex-1 space-y-2">
            <div className="h-3 w-full bg-slate-100 rounded-full"></div>
            <div className="h-3 w-48 bg-slate-100 rounded"></div>
          </div>
        </div>
      </div>

      {/* Tabs & Content Skeleton */}
      <div className="space-y-4">
        <div className="flex gap-2 border-b border-slate-200 pb-2">
          <div className="h-8 w-24 bg-slate-200 rounded"></div>
          <div className="h-8 w-24 bg-slate-100 rounded"></div>
          <div className="h-8 w-24 bg-slate-100 rounded"></div>
        </div>
        <div className="h-64 bg-white border border-slate-200 rounded-xl p-6"></div>
      </div>
    </div>
  );
}
