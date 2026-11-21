"""Cache em memória com expiração por tempo (TTL).

Cada valor guardado vale por `ttl_s` segundos; depois disso é tratado como
inexistente. Não é thread-safe e não é compartilhado entre processos.
"""

import time

# Limite de entradas no cache. Ao atingir esse limite, inserir uma chave nova
# remove a entrada mais antiga para abrir espaço.
MAX_ENTRIES = 1024


class TTLCache:
    def __init__(self, ttl_s, clock=time.monotonic):
        # ttl_s: tempo de vida de cada entrada, em segundos.
        # clock: função que devolve o "agora" em segundos. O padrão é
        # time.monotonic (não é afetado por mudanças no relógio do sistema).
        # Existe como parâmetro para os testes poderem simular a passagem do
        # tempo sem usar sleep.
        self._ttl_s = ttl_s
        self._clock = clock
        # chave -> (valor, instante em que foi gravado)
        self._entries = {}

    def get(self, key, default=None):
        """Devolve o valor de `key`, ou `default` se não existir ou tiver expirado."""
        entry = self._entries.get(key)
        if entry is None:
            return default
        value, stored_at = entry
        # A expiração é preguiçosa: entradas vencidas só são removidas quando
        # alguém tenta lê-las. Até lá, continuam ocupando espaço no cache.
        # Com idade exatamente igual ao TTL, a entrada ainda é válida (> e não >=).
        if self._clock() - stored_at > self._ttl_s:
            del self._entries[key]
            return default
        return value

    def put(self, key, value):
        """Grava `value` em `key`, reiniciando a contagem do TTL dessa chave."""
        # Só despeja quando a chave é nova: sobrescrever uma chave existente
        # não aumenta o tamanho do cache.
        if key not in self._entries and len(self._entries) >= MAX_ENTRIES:
            # Despeja a entrada gravada há mais tempo (varredura linear, O(n)).
            # Pode ser uma entrada ainda válida; não há prioridade por uso.
            oldest = min(self._entries, key=lambda k: self._entries[k][1])
            del self._entries[oldest]
        self._entries[key] = (value, self._clock())
