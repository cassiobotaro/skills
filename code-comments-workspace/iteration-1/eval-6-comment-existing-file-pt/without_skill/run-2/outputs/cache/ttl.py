import time

# Limite de itens no cache. Ao atingir esse número, inserir uma chave nova
# descarta a entrada mais antiga (ver TTLCache.put).
MAX_ENTRIES = 1024


class TTLCache:
    """Cache em memória em que cada entrada expira após `ttl_s` segundos.

    A expiração é "preguiçosa": entradas vencidas só são removidas quando
    alguém chama `get` para a mesma chave (ou quando são despejadas por
    falta de espaço em `put`). Não há thread de limpeza em segundo plano.

    Não é thread-safe: use um lock externo se for compartilhar entre threads.
    """

    def __init__(self, ttl_s, clock=time.monotonic):
        # Tempo de vida de cada entrada, em segundos.
        self._ttl_s = ttl_s
        # Função que devolve "agora" em segundos. É injetável para os testes
        # poderem avançar o tempo sem dar sleep. O padrão, time.monotonic, não
        # é afetado por mudanças no relógio do sistema.
        self._clock = clock
        # chave -> (valor, instante em que foi gravado)
        self._entries = {}

    def get(self, key, default=None):
        """Devolve o valor de `key`, ou `default` se não existir ou tiver expirado."""
        entry = self._entries.get(key)
        if entry is None:
            return default
        value, stored_at = entry
        # Só expira quando a idade passa do TTL (estritamente maior):
        # com idade exatamente igual a ttl_s a entrada ainda é válida.
        if self._clock() - stored_at > self._ttl_s:
            # Remove na leitura, já que nada mais limpa entradas vencidas.
            del self._entries[key]
            return default
        return value

    def put(self, key, value):
        """Grava `value` em `key`, reiniciando o TTL dessa chave."""
        # Só despeja se a chave é nova e o cache está cheio; sobrescrever uma
        # chave existente não aumenta o tamanho.
        if key not in self._entries and len(self._entries) >= MAX_ENTRIES:
            # Despeja a entrada gravada há mais tempo (não a menos usada: ler
            # não atualiza `stored_at`). É uma busca linear, O(n), aceitável
            # com MAX_ENTRIES pequeno. Pode despejar uma entrada ainda válida
            # mesmo havendo vencidas, pois não procura por elas.
            oldest = min(self._entries, key=lambda k: self._entries[k][1])
            del self._entries[oldest]
        self._entries[key] = (value, self._clock())
