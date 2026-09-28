#!/usr/bin/env bash
# Counts the no-ai-slop patterns that the 1.3.6 run tripped, per file.
for f in "$@"; do
  echo "== $f  ($(wc -w < "$f") words)"
  echo "  em dashes total:        $(grep -o '—' "$f" | wc -l)"
  echo "  em dashes in prose:     $(grep '—' "$f" | grep -vE '^\s*(#|\||[0-9]+\. \*\*|!\[)' | grep -o '—' | wc -l)"
  echo "  emphasis bold in text:  $(grep -cE '[a-záéíóú,] \*\*[^*]+\*\* [a-záéíóú]' "$f")"
  echo "  gap-marker repeats:     $(grep -ciE 'ainda não (definiu|discutiu|levantou|acordaram|decidiu|tem)|não está definido|nada disso está definido' "$f")"
  echo "  colon reveal candidates:"
  grep -nE '^[^|#`>-][^:]{0,60}: [a-záéíóú]' "$f" | cut -c1-100 | sed 's/^/    /'
  echo "  'este documento' paragraph: $(grep -ciE '^(o|este) documento (registra|descreve|cobre|apresenta)' "$f")"
  echo "  passive (é/são/foi + particípio): $(grep -cE '\b(é|são|foi|foram|será|serão) [a-zç]+(ad[oa]s?|id[oa]s?)\b' "$f")"
  echo "  banned/puffery hits: $(grep -ciE 'robust|alavanc|otimiz|transformad|fundamental|crucial|essencial|vale (notar|lembrar|destacar)|é importante|garantindo|permitindo|refletindo' "$f")"
done
