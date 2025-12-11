DAY := `date +%-d`
md day=DAY:
  uv run utils/make_day.py {{day}}
  uv run aocd 2022 {{day}} > d{{day}}/r.in
  uv run aocd 2022 {{day}} --example | sed -n '/Example data/,/^---/p' | sed '1d;$d' > d{{day}}/t.in
  printf 't1:\n  uv run p1.py < t.in\n\nr1:\n  uv run p1.py < r.in\n\nt2:\n  uv run p2.py < t.in\n\nr2:\n  uv run p2.py < r.in\n' > d{{day}}/justfile

desc day=DAY:
  uv run --with requests utils/fetch_desc.py {{day}} d{{day}}

test day=DAY part="1":
  @if [ {{day}} -eq 22 ] && [ {{part}} -eq 2 ]; then uv run --with numpy d{{day}}/p{{part}}.py < d{{day}}/t.in; else uv run d{{day}}/p{{part}}.py < d{{day}}/t.in; fi

run day=DAY part="1":
  @if [ {{day}} -eq 22 ] && [ {{part}} -eq 2 ]; then uv run --with numpy d{{day}}/p{{part}}.py < d{{day}}/r.in; else uv run d{{day}}/p{{part}}.py < d{{day}}/r.in; fi

submit part day=DAY:
  uv run --with requests utils/submit.py {{day}} {{part}}
