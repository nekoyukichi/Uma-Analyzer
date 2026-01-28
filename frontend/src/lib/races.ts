import { createSupabaseServerClient } from "@/lib/supabase/server";

export type RaceRow = {
  race_id: string;
  held_on: string; // ISO date
  race_name: string;
  course: string;
  track_type: string;
  distance_m: number;
  race_class: string | null;
  weather: string | null;
  track_condition: string | null;
  raw_source_url: string | null;
};

export async function fetchAllRaces(): Promise<RaceRow[]> {
  const supabase = createSupabaseServerClient();

  const { data, error } = await supabase
    .from("races")
    .select(
      "race_id, held_on, race_name, course, track_type, distance_m, race_class, weather, track_condition, raw_source_url"
    )
    .order("held_on", { ascending: false })
    .order("race_id", { ascending: false });

  if (error) throw new Error(`Failed to fetch races: ${error.message}`);
  return data ?? [];
}


