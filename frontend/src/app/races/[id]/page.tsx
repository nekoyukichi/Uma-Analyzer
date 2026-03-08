import Link from "next/link";
import { notFound } from "next/navigation";

import { fetchRaceById } from "@/lib/races";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card";

export const dynamic = "force-dynamic";

function formatDateJa(isoDate: string) {
  const d = new Date(isoDate);
  if (Number.isNaN(d.getTime())) return isoDate;
  return d.toLocaleDateString("ja-JP", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  });
}

export default async function RaceDetailPage({
  params
}: {
  params: { id: string };
}) {
  let race: Awaited<ReturnType<typeof fetchRaceById>> = null;
  let loadError: string | null = null;

  try {
    race = await fetchRaceById(params.id);
  } catch (error) {
    loadError =
      error instanceof Error
        ? error.message
        : "レースデータの取得に失敗しました。";
  }

  if (loadError) {
    return (
      <main className="min-h-screen bg-background text-foreground">
        <div className="mx-auto max-w-4xl px-4 py-10 space-y-4">
          <h1 className="text-2xl font-bold tracking-tight">レース詳細</h1>
          <p className="rounded-md border border-destructive/30 bg-destructive/10 px-4 py-3 text-sm text-destructive">
            データの取得に失敗しました: {loadError}
          </p>
          <Link
            href="/races"
            className="inline-block text-sm text-muted-foreground hover:text-foreground underline underline-offset-4"
          >
            ← 一覧へ戻る
          </Link>
        </div>
      </main>
    );
  }

  if (!race) notFound();

  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-4xl px-4 py-10 space-y-6">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-2">
            <h1 className="text-2xl font-bold tracking-tight">{race.race_name}</h1>
            <div className="flex flex-wrap items-center gap-2">
              <Badge variant="secondary">{formatDateJa(race.held_on)}</Badge>
              <Badge variant="outline">{race.course}</Badge>
              <Badge variant="outline">{race.track_type}</Badge>
              <Badge variant="secondary">{race.distance_m}m</Badge>
              {race.race_class ? <Badge>{race.race_class}</Badge> : null}
            </div>
            <p className="text-xs text-muted-foreground font-mono">
              race_id: {race.race_id}
            </p>
          </div>
          <Link
            href="/races"
            className="text-sm text-muted-foreground hover:text-foreground underline underline-offset-4"
          >
            ← 一覧へ
          </Link>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>レース条件</CardTitle>
            <CardDescription>取得できた範囲で整理して表示します。</CardDescription>
          </CardHeader>
          <CardContent>
            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1">
                <dt className="text-xs text-muted-foreground">開催日</dt>
                <dd className="font-medium">{formatDateJa(race.held_on)}</dd>
              </div>
              <div className="space-y-1">
                <dt className="text-xs text-muted-foreground">コース</dt>
                <dd className="font-medium">{race.course}</dd>
              </div>
              <div className="space-y-1">
                <dt className="text-xs text-muted-foreground">種別</dt>
                <dd className="font-medium">{race.track_type}</dd>
              </div>
              <div className="space-y-1">
                <dt className="text-xs text-muted-foreground">距離</dt>
                <dd className="font-medium">{race.distance_m}m</dd>
              </div>
              <div className="space-y-1">
                <dt className="text-xs text-muted-foreground">天気</dt>
                <dd className="font-medium">{race.weather ?? "—"}</dd>
              </div>
              <div className="space-y-1">
                <dt className="text-xs text-muted-foreground">馬場状態</dt>
                <dd className="font-medium">{race.track_condition ?? "—"}</dd>
              </div>
            </dl>

            {race.raw_source_url ? (
              <div className="mt-6 text-sm">
                <a
                  href={race.raw_source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-muted-foreground hover:text-foreground underline underline-offset-4 break-all"
                >
                  元ページを開く
                </a>
              </div>
            ) : null}
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
