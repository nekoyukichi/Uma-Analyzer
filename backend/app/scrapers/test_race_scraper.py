from __future__ import annotations

from app.scrapers.race_scraper import parse_race_results, rows_to_dataframe


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


def main() -> None:
    rows = parse_race_results(SAMPLE_HTML)
    df = rows_to_dataframe(rows)
    print(df)

    assert len(rows) == 2
    assert rows[0].finish_position == 1
    assert rows[0].horse_name == "サンプルホースA"


if __name__ == "__main__":
    main()


