"""Short, synchronous, process-local operations without database dependencies.

Routes call these methods from one event loop. With no await in a method, each
operation completes before another task runs. This is NOT a thread-safe or
distributed repository. Adding threads, I/O, or workers requires revisiting
synchronization and persistence. See docs/06-scaling.md.
"""

from app.models import Order, OrderCreate, OrderPage, OrderStatus, OrderSummary

ACTIVE_STATUSES = frozenset({OrderStatus.pending, OrderStatus.preparing})


class OrderRepository:
    def __init__(self) -> None:
        self._orders = {
            1: Order(id=1, item="Chicken Kadai", count=1, status=OrderStatus.delivered),
            2: Order(id=2, item="Chicken Sukka", count=2, status=OrderStatus.preparing),
            3: Order(id=3, item="Chicken Steak", count=1, status=OrderStatus.pending),
        }
        self._next_id = 4

    def list_orders(
        self,
        *,
        status: OrderStatus | None = None,
        active_only: bool = False,
        limit: int = 20,
        offset: int = 0,
    ) -> OrderPage:
        matches = [
            order
            for order in self._orders.values()
            if (status is None or order.status == status)
            and (not active_only or order.status in ACTIVE_STATUSES)
        ]
        matches.sort(key=lambda order: order.id)
        return OrderPage(
            orders=matches[offset : offset + limit],
            total=len(matches),
            limit=limit,
            offset=offset,
        )

    def get(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)

    def create(self, payload: OrderCreate) -> Order:
        order = Order(id=self._next_id, **payload.model_dump(), status=OrderStatus.pending)
        self._orders[order.id] = order
        self._next_id += 1
        return order

    def update_status(self, order_id: int, status: OrderStatus) -> Order | None:
        current = self.get(order_id)
        if current is None:
            return None
        # model_copy does not revalidate updates. Here status is already an enum
        # validated by OrderStatusUpdate; never pass an arbitrary dict to it.
        updated = current.model_copy(update={"status": status})
        self._orders[order_id] = updated
        return updated

    def delete(self, order_id: int) -> bool:
        return self._orders.pop(order_id, None) is not None

    def summary(self) -> OrderSummary:
        counts = dict.fromkeys(OrderStatus, 0)
        for order in self._orders.values():
            counts[order.status] += 1
        return OrderSummary(
            total=len(self._orders),
            active=sum(counts[state] for state in ACTIVE_STATUSES),
            by_status=counts,
        )
