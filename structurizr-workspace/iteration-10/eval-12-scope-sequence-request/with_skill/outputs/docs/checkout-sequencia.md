# Checkout — sequência de chamadas

Fluxo do checkout a partir da chamada do app à API de Pedidos: reserva de estoque, cobrança no gateway e publicação do evento de pedido confirmado. O ramo de pagamento recusado mostra apenas o que já foi estabelecido; as pendências estão listadas abaixo do diagrama.

```mermaid
sequenceDiagram
    autonumber
    participant app as App
    participant pedidos as API de Pedidos
    participant inventario as Serviço de Inventário
    participant pagamento as Gateway de Pagamento
    participant fila as Fila

    app->>+pedidos: Criar pedido (checkout)
    pedidos->>+inventario: Reservar estoque dos itens
    inventario-->>-pedidos: Reserva confirmada
    pedidos->>+pagamento: Cobrar o pedido
    alt pagamento aprovado
        pagamento-->>pedidos: Aprovado
        pedidos-)fila: Publica evento "pedido confirmado"
        pedidos-->>app: Pedido confirmado
    else pagamento recusado
        pagamento-->>pedidos: Recusado
        Note over pedidos: Nenhum evento é publicado.<br/>O que acontece com a reserva de estoque<br/>e o que o app recebe ainda não foi definido.
    end
    deactivate pagamento
    deactivate pedidos
```

## Pendências (ramo de pagamento recusado)

- A reserva de estoque é liberada? Por quem — a API de Pedidos chama o inventário, ou a reserva expira sozinha?
- O que o app recebe de volta: erro definitivo, ou o pedido fica pendente para tentar outro meio de pagamento?
- Algum evento é publicado na recusa (ex.: "pedido cancelado"), ou só no sucesso?
- Detalhes técnicos (endpoints, status HTTP, nome da fila/tópico, campos do evento) para as notas, se o diagrama deve carregá-los.

Validado com a imagem Docker do mermaid-cli (`minlag/mermaid-cli`).
