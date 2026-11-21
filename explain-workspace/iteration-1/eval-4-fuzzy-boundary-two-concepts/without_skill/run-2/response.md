**Short version:**
- **Concurrency** means juggling several tasks, so that they overlap in time. Only one of them may actually be running at any instant.
- **Parallelism** means several tasks literally running at the same instant, on different CPU cores.

**Analogy:** One cook with three pots on the stove. While the pasta boils, they chop vegetables, then stir the sauce. Only one thing gets attention at a time, but all three dishes make progress. That's concurrency. Now hire three cooks, one per pot, all working at once. That's parallelism.

Concurrency is about how you *structure* work, so you don't sit idle while waiting. Parallelism is about how you *execute* work, so you use more than one core.

**What this means for your cleanup scripts**

The first question is what your script spends its time on.

1. **Waiting (I/O-bound):** downloading files, calling APIs, querying a database, reading many files from a slow disk. The CPU is mostly idle. Concurrency fixes this. While one request waits, you start another.
   - Tools: `threading`, `concurrent.futures.ThreadPoolExecutor`, or `asyncio`.
   - Example: fetching 500 URLs. Sequentially that takes 500 × latency. With 20 threads, it takes roughly 25 × latency.

2. **Computing (CPU-bound):** heavy regex over millions of rows, parsing, hashing, number crunching in pure Python. The CPU is busy the whole time. Only parallelism helps, because you need more cores working.
   - Tool: `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`.
   - Why not threads? Standard CPython has the GIL, which lets only one thread run Python bytecode at a time. Threads give you concurrency but not parallelism for CPU work. Processes each have their own interpreter, so they really do run in parallel. (Recent Python versions have an optional free-threaded build, but processes are still the safe default.)

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# I/O-bound: concurrency via threads
with ThreadPoolExecutor(max_workers=20) as pool:
    results = list(pool.map(download, urls))

# CPU-bound: parallelism via processes
with ProcessPoolExecutor() as pool:
    results = list(pool.map(clean_chunk, chunks))
```

The two APIs are nearly identical, so switching is easy.

**Practical advice**

- Don't reach for either one until the script is actually too slow. For most cleanup jobs, a plain loop is fine.
- If you do need speed, measure first. Is the time spent waiting or computing? Something like `time python script.py` shows this. If "real" time is much bigger than "user" time, you're waiting (I/O). If they're about equal, you're CPU-bound.
- If you use pandas, vectorized operations (avoiding Python-level loops) usually beat both approaches, with less complexity.

**One-line memory aid:** concurrency is *dealing with* many things at once. Parallelism is *doing* many things at once.
