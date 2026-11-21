**Concurrency is about *dealing with* several tasks at once. Parallelism is about *running* several tasks at the same instant.** Concurrency means the tasks overlap in time, and it works even on one CPU core. Parallelism needs more than one core doing work simultaneously.

I'm assuming you know what a function and a loop are, and that you may not have used `threading`, `asyncio` or `multiprocessing` yet.

**A pair that differs in one trait.** Suppose you clean 100 CSV files.

- **Concurrent, not parallel:** one worker starts file 1, and while it waits on the disk or network, it starts file 2, then returns to file 1 when its data arrives. One worker is only ever doing one thing at a given instant. It never sits idle, because it switches while something else is waiting.
- **Parallel:** four workers, each cleaning its own files at the same time on four cores.

The trait that differs is whether more than one thing is actually executing at the same instant. Both finish sooner than one worker going file by file, but for different reasons.

**Which one helps your script depends on where the time goes.**

| Your script is slow because it... | What helps | Python tool |
|---|---|---|
| waits (downloads, reads from a database or API, many small files) | concurrency | `threading`, `asyncio`, or `concurrent.futures.ThreadPoolExecutor` |
| computes (heavy regex, big transformations in pure Python) | parallelism | `multiprocessing`, or `concurrent.futures.ProcessPoolExecutor` |

The reason for the split is that in standard CPython, threads take turns running Python code because of the GIL (global interpreter lock). So threads give you concurrency, which is enough when the time is spent waiting. They don't speed up pure-Python computation, which needs separate processes. That is the usual behavior. Newer optional "free-threaded" builds change it, but I'm not covering those here.

**What this leaves out.** Many libraries you probably already use, such as pandas and NumPy, do much of their heavy work in compiled code. That work can sometimes run in parallel even with threads, so measure before assuming. If your cleanup finishes in a minute, you likely need neither.

**A check on whether it landed.** You have 500 URLs to fetch and clean, and each takes 2 seconds, almost all of it waiting on the server. Would you reach for threads or processes? If you answer threads, tell me why. I'll show it with your own script if you paste it.
