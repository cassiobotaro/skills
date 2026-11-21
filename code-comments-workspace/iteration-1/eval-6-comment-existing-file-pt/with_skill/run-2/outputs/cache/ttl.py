import time

# Limite de entradas; ao atingi-lo, put() descarta a entrada mais antiga.
MAX_ENTRIES = 1024


# Cache em memória em que cada entrada expira `ttl_s` segundos depois de gravada.
# A expiração é preguiçosa: uma entrada vencida só sai do dicionário quando é lida
# com get() ou quando é expulsa por falta de espaço. Até lá ela continua ocupando
# uma das MAX_ENTRIES vagas. Não há lock; não use a mesma instância em várias threads
# sem sincronização externa.
class TTLCache:
    # `clock` é uma função sem argumentos que devolve segundos. O padrão,
    # time.monotonic, não é afetado por ajustes do relógio do sistema.
    def __init__(self, ttl_s, clock=time.monotonic):
        self._ttl_s = ttl_s
        self._clock = clock
        # chave -> (valor, instante em que foi gravada)
        self._entries = {}

    # Devolve `default` se a chave não existe ou já expirou (e nesse caso a remove).
    # Uma entrada com idade exatamente igual a ttl_s ainda é válida.
    # Ler não renova o prazo: o TTL conta a partir do put().
    def get(self, key, default=None):
        entry = self._entries.get(key)
        if entry is None:
            return default
        value, stored_at = entry
        if self._clock() - stored_at > self._ttl_s:
            del self._entries[key]
            return default
        return value

    # Regravar uma chave existente reinicia o prazo dela e nunca expulsa ninguém.
    def put(self, key, value):
        if key not in self._entries and len(self._entries) >= MAX_ENTRIES:
            # Cache cheio e chave nova: expulsa a entrada gravada há mais tempo
            # (pode ser uma já expirada ou não). É uma busca linear, O(n) por put()
            # com o cache cheio.
            oldest = min(self._entries, key=lambda k: self._entries[k][1])
            del self._entries[oldest]
        self._entries[key] = (value, self._clock())
