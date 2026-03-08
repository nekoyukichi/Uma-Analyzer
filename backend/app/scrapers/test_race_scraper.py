from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.scrapers.race_scraper import parse_race_metadata, parse_race_results, rows_to_dataframe


SAMPLE_HTML = """
<!doctype html>
<html lang="ja">
  <body>
    <table class="race_table_01">
      <tr>
        <th>着順</th><th>馬名</th>
      </tr>
      <tr>
        <td class="rank">1</td>
        <td class="horse_name"><a href="/horse/2018100001/">サンプルホースA</a></td>
      </tr>
      <tr>
        <td class="rank">2</td>
        <td class="horse_name"><a href="/horse/2018100002/">サンプルホースB</a></td>
      </tr>
      <tr>
        <td class="rank">取消</td>
        <td class="horse_name"><a href="/horse/2018100003/">サンプルホースC</a></td>
      </tr>
    </table>
  </body>
</html>
""".strip()

SAMPLE_METADATA_HTML = """
<!doctype html>
<html lang="ja">
  <head>
    <title>パラダイスステークス｜2023年6月25日 | 競馬データベース - netkeiba</title>
  </head>
  <body>
    <h1></h1>
    <p class="smalltxt">2023年06月25日 3回東京8日目 3歳以上オープン</p>
    <diary_snap_cut>
      <span>芝左1400m / 天候 : 晴 / 芝 : 良 / 発走 : 15:30</span>
    </diary_snap_cut>
  </body>
</html>
""".strip()


def main() -> None:
    rows = parse_race_results(SAMPLE_HTML)
    df = rows_to_dataframe(rows)
    print(df)

    assert len(rows) == 2
    assert rows[0].finish_position == 1
    assert rows[0].horse_name == "サンプルホースA"

    race = parse_race_metadata(
        SAMPLE_METADATA_HTML, url="https://db.netkeiba.com/race/202305030811/"
    )
    assert race.race_name == "パラダイスステークス"
    assert race.course == "東京"
    assert race.track_type == "芝"
    assert race.distance_m == 1400
    assert race.weather == "晴"
    assert race.track_condition == "良"


if __name__ == "__main__":
    main()
