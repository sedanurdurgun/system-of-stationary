# shipping_selector.py
from shippingstrategy import FastShipping, CheapShipping, DroneShipping, ShippingStrategy
from order import Order  # Type hinting için


def choose_optimal_shipping_strategy(order: Order) -> ShippingStrategy:
    """
    Sipariş özelliklerine göre en uygun kargo stratejisini otomatik olarak seçer.
    """
    print("\nOtomatik kargo stratejisi belirleniyor...")

    if order.total >= 1000:
        strategy = FastShipping()
        print(f"Siparişinizin toplam maliyeti ({order.total:.2f}₺) yüksek olduğu için '{strategy.get_name()}' seçildi.")
    elif order.total >= 500:
        strategy = DroneShipping()
        print(
            f"Siparişinizin toplam maliyeti ({order.total:.2f}₺) orta seviyede olduğu için '{strategy.get_name()}' seçildi.")
    else:
        strategy = CheapShipping()
        print(f"Siparişinizin toplam maliyeti ({order.total:.2f}₺) düşük olduğu için '{strategy.get_name()}' seçildi.")

    return strategy