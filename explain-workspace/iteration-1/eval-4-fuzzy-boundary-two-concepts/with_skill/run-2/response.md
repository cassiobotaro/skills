**Short answer:** concurrency is about *juggling* several tasks so they overlap in time. Parallelism is about *actually running* several at the same instant on different CPU cores. You can have concurrency without parallelism, but not the reverse.

I'm assuming you know what a function and a loop are, and that you haven't used `threading`, `asyncio` or `multiprocessing` much. Tell me if that's off.

**One pair of cases that differ in a single trait.** Say you have 100 files to clean.

- **Case A: the slow part is waiting.** Each file comes from a web API, and each download takes 2 seconds of mostly idle time. A single core can start download 1, and while it waits, start download 2, and so on. Only one thing runs at any instant, but the waits overlap, so 100 files take about 2 seconds instead of 200. That's **concurrency without parallelism**. In Python you'd use `threading`, `ThreadPoolExecutor` or `asyncio`.
- **Case B: the slow part is computing.** The files are already on disk, and each one takes 2 seconds of real CPU work (heavy regex, big transformations). Overlapping gains nothing, because nothing is waiting. The only way to speed this up is more cores working at once. That's **parallelism**. In Python you'd use `multiprocessing` or `ProcessPoolExecutor`.

The one trait that differs is what the time is spent on, waiting or computing. That trait decides which tool helps.

**Where this stops being simple.** In standard CPython, the Global Interpreter Lock (GIL) lets only one thread run Python code at a time. That's why threads help in Case A but not in Case B, and why Case B needs separate processes. This is true of the standard build. Newer free-threaded builds change it, but I haven't checked their current state. Also, running processes in parallel has its own costs (starting them, copying data between them), so for small jobs it can be slower than a plain loop.

**For your scripts:** if a cleanup script already finishes in a few seconds, you probably need neither. Reach for one of these only when you can see where the time goes: waiting on network or disk, or computing.

**A check:** you have a script that reads 50 local CSVs and runs a slow pandas transformation on each. Would threads or processes speed it up, and why? If you tell me which one you picked, I can check your reasoning.
