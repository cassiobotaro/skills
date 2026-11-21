"""Cache em memória em que cada entrada expira `ttl_s` segundos após ser gravada.

Leitura não renova a validade (não é LRU): só `put` reinicia o relógio da chave.
Não há trava interna, então o acesso concorrente de várias threads não é protegido.
"""
import time

# Limite de entradas; ao atingi-lo, `put` de chave nova descarta a mais antiga.
MAX_ENTRIES = 1024


class TTLCache:
    def __init__(self, ttl_s, clock=time.monotonic):
        self._ttl_s = ttl_s
        # `clock` é injetável para testes controlarem o tempo. O padrão é monotônico,
        # então o cache não é afetado por ajustes no relógio do sistema.
        self._clock = clock
        # chave -> (valor, instante em que foi gravada, segundo `_clock`)
        self._entries = {}

    def get(self, key, default=None):
        """Devolve o valor, ou `default` se a chave não existe ou já expirou.

        Entrada expirada só é removida aqui, na leitura: uma chave que nunca mais
        é lida continua ocupando espaço (e contando para MAX_ENTRIES).
        """
        entry = self._entries.get(key)
        if entry is None:
            return default
        value, stored_at = entry
        # `>` estrito: com idade exatamente igual ao ttl a entrada ainda é válida.
        if self._clock() - stored_at > self._ttl_s:
            del self._entries[key]
            return default
        return value

    def put(self, key, value):
        """Grava `value`, reiniciando a contagem do ttl se a chave já existia."""
        if key not in self._entries and len(self._entries) >= MAX_ENTRIES:
            # Despeja a entrada gravada há mais tempo, expirada ou não. Varre todas
            # as entradas (O(n)), custo que se paga em todo put com o cache cheio.
            oldest = min(self._entries, key=lambda k: self._entries[k][1])
            del self._entries[oldest]
        self._entries[key] = (value, self._clock())
