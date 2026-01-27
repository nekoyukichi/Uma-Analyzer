-- Supabase (PostgreSQL) schema
-- Races table: stores basic race metadata

create table if not exists public.races (
  race_id text primary key,
  held_on date not null,
  race_name text not null,
  course text not null,           -- e.g., "東京", "中山"
  track_type text not null,       -- e.g., "芝", "ダート"
  distance_m integer not null check (distance_m > 0),
  race_class text null,           -- e.g., "G1", "G2", "1勝クラス"
  weather text null,
  track_condition text null,      -- e.g., "良", "稍重", "重", "不良"
  raw_source_url text null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

comment on table public.races is 'Race metadata scraped/ingested from external sources (e.g., netkeiba).';
comment on column public.races.race_id is 'Race identifier (e.g., netkeiba race_id) stored as text for flexibility.';

-- Optional index examples
create index if not exists races_held_on_idx on public.races (held_on);
create index if not exists races_course_idx on public.races (course);

-- updated_at auto-update trigger
create or replace function public.set_updated_at() returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists races_set_updated_at on public.races;
create trigger races_set_updated_at
before update on public.races
for each row
execute function public.set_updated_at();
