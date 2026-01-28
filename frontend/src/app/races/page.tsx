import Link from "next/link";

import { fetchAllRaces } from "@/lib/races";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from "@/components/ui/table";

export const dynamic = "force-dynamic";

function formatDateJa(isoDate: string) {
  // isoDate is like "2026-01-28"
  const d = new Date(isoDate);
  if (Number.isNaN(d.getTime())) return isoDate;
  return d.toLocaleDateString("ja-JP", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  });
}

export default async function RacesPage() {
  const races = await fetchAllRaces();

  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-6xl px-4 py-10 space-y-6">
        <div className="flex items-end justify-between gap-4">
          <div className="space-y-1">
            <h1 className="text-2xl font-bold tracking-tight">レース一覧</h1>
            <p className="text-sm text-muted-foreground">
              Supabase の <code className="font-mono">races</code> テーブルから取得したデータです。
            </p>
          </div>
          <Link
            href="/"
            className="text-sm text-muted-foreground hover:text-foreground underline underline-offset-4"
          >
            ← Home
          </Link>
        </div>

        <div className="rounded-lg border bg-card">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[120px]">開催日</TableHead>
                <TableHead>レース名</TableHead>
                <TableHead className="w-[120px]">コース</TableHead>
                <TableHead className="w-[120px]">種別</TableHead>
                <TableHead className="w-[120px] text-right">距離</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {races.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="py-10 text-center text-muted-foreground">
                    データがありません（まだ取り込み前か、RLS/権限で取得できていない可能性があります）
                  </TableCell>
                </TableRow>
              ) : (
                races.map((r) => (
                  <TableRow key={r.race_id}>
                    <TableCell className="font-mono text-xs">
                      {formatDateJa(r.held_on)}
                    </TableCell>
                    <TableCell className="font-medium">
                      <div className="flex flex-col">
                        <Link
                          href={`/races/${r.race_id}`}
                          className="hover:underline underline-offset-4"
                        >
                          {r.race_name}
                        </Link>
                        <span className="text-xs text-muted-foreground font-mono">
                          {r.race_id}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>{r.course}</TableCell>
                    <TableCell>{r.track_type}</TableCell>
                    <TableCell className="text-right">{r.distance_m}m</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </div>
    </main>
  );
}


