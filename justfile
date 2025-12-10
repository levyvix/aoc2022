DAY := `date +%-d`
md day=DAY:
  uv run utils/make_day.py {{day}}
  uv run aocd 2022 {{day}} > d{{day}}/r.in
  uv run aocd 2022 {{day}} --example | sed -n '/Example data/,/^---/p' | sed '1d;$d' > d{{day}}/t.in
  printf 't1:\n  uv run p1.py < t.in\n\nr1:\n  uv run p1.py < r.in\n\nt2:\n  uv run p2.py < t.in\n\nr2:\n  uv run p2.py < r.in\n' > d{{day}}/justfile

desc day=DAY:
  uv run --with requests utils/fetch_desc.py {{day}} d{{day}}

submit part day=DAY:
  uv run --with requests utils/submit.py {{day}} {{part}}
