**Short version:**
- **Concurrency** means juggling several tasks so they overlap in time. They take turns, and only one may be running at any instant.
- **Parallelism** means actually running several tasks at the same moment, on different CPU cores.

**An analogy.** One cook is making soup and bread. While the soup simmers, they knead the dough. That's concurrency: one cook, two tasks in progress, switching whenever one is waiting. Two cooks, one on soup and one on bread, working at the same time is parallelism.

Concurrency is about *structuring* work so waiting time isn't wasted. Parallelism is about *executing* work simultaneously to go faster.

**What this means in Python for data cleanup**

The kind of slowness you have decides which tool to use:

| Your script is slow because it... | Problem type | Tool |
|---|---|---|
| waits on files, network, APIs, or a database | I/O-bound | concurrency: `threading`, `asyncio`, or `concurrent.futures.ThreadPoolExecutor` |
| crunches numbers, parses, or transforms lots of data | CPU-bound | parallelism: `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` |

Python's GIL (Global Interpreter Lock) lets only one thread run Python code at a time. So threads give you concurrency, not parallelism, for CPU work. They still help when the program is mostly waiting, because a waiting thread releases the lock. To use several cores, you need separate processes.

**Examples**

I/O-bound, such as fetching 100 URLs. Threads overlap the waiting:
```python
from concurrent.futures import ThreadPoolExecutor
import requests

def fetch(url):
    return requests.get(url).text

with ThreadPoolExecutor(max_workers=10) as pool:
    pages = list(pool.map(fetch, urls))
```

CPU-bound, such as cleaning 50 big CSV files. Processes use all cores:
```python
from concurrent.futures import ProcessPoolExecutor

def clean_file(path):
    ...  # read, transform, write

if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        list(pool.map(clean_file, paths))
```

Both use the same `pool.map` interface, so switching between them is a one-word change.

**Practical advice**
- If your scripts finish in seconds, you probably need neither. Don't add this complexity without a reason.
- If you're cleaning many independent files, `ProcessPoolExecutor` is usually the easiest win.
- With pandas or polars, vectorized operations are often faster than either approach, so try those first.
- Measure before and after. Parallelism has overhead and can be slower for small jobs.

To remember it: **concurrency is about dealing with many things at once, and parallelism is about doing many things at once.**
