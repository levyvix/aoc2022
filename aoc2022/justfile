DAY := `date +%-d`
md day=DAY:
  uv run utils/make_day.py {{day}}
  uv run aocd 2025 {{day}} > d{{day}}/r.in
  uv run aocd 2025 {{day}} --example | sed -n '/Example data/,/^---/p' | sed '1d;$d' > d{{day}}/t.in
