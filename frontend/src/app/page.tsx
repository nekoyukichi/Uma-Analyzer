import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-slate-900 via-slate-950 to-black px-4">
      <div className="max-w-2xl text-center space-y-6">
        <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-white">
          Uma Analyzer
        </h1>
        <p className="text-slate-300">
          過去レースデータから傾向を可視化し、
          次のレース予想に役立てるための競馬分析ダッシュボードです。
        </p>
        <Button size="lg" className="mt-2">
          分析を始める
        </Button>
      </div>
    </main>
  );
}


