# order_factory.py
import uuid  # UUID modülünü import et
from typing import List, Tuple, Any
from order import Order, ExpressOrder, SubscriptionOrder, PreOrder, GiftOrder, BulkOrder
from product import Product  # Used for type hinting for products in product_data
from customer import Customer  # Used for type hinting for customer


class OrderFactory:
    """
    Sipariş nesneleri oluşturmak için Factory Method deseni uygular.
    Farklı sipariş türlerini (standart, ekspres, abonelik vb.) soyutlar.
    """

    # _order_counter = 1 # Benzersiz sipariş ID'leri için sayaç (artık UUID kullanılacak)

    @staticmethod
    def create_order(order_type: str, customer: Customer, product_data: List[Tuple[Product, int]], **kwargs) -> Order:
        """
        Belirtilen türe göre bir sipariş nesnesi oluşturur.

        Args:
            order_type (str): Oluşturulacak siparişin türü (standard, express, subscription, preorder, gift, bulk).
            customer (Customer): Siparişi veren müşteri nesnesi.
            product_data (List[Tuple[Product, int]]): (ürün, adet) tuple'larından oluşan liste.
            **kwargs: Sipariş türüne özgü ek argümanlar (örn. expected_delivery_date, gift_note).

        Returns:
            Order: Oluşturulan sipariş nesnesi.

        Raises:
            ValueError: Geçersiz bir sipariş türü belirtildiğinde.
        """
        # Benzersiz sipariş ID'si üretimi için UUID kullanıldı
        order_id = str(uuid.uuid4())

        if order_type == "standard":
            order = Order(order_id, customer, product_data)
        elif order_type == "express":
            order = ExpressOrder(order_id, customer, product_data)
        elif order_type == "subscription":
            order = SubscriptionOrder(order_id, customer, product_data)
        elif order_type == "preorder":
            expected_delivery_date = kwargs.get("expected_delivery_date")
            if not expected_delivery_date:
                raise ValueError("Ön sipariş için tahmini teslim tarihi belirtilmelidir.")
            order = PreOrder(order_id, customer, product_data, expected_delivery_date)
        elif order_type == "gift":
            gift_note = kwargs.get("gift_note", "")
            order = GiftOrder(order_id, customer, product_data, gift_note)
        elif order_type == "bulk":
            order = BulkOrder(order_id, customer, product_data)
        else:
            raise ValueError(
                f"Geçersiz sipariş türü: '{order_type}'. Desteklenen türler: standard, express, subscription, preorder, gift, bulk.")

        # Müşteriye siparişin orijinal halini ekle (Observer deseni için de gerekli)
        customer.add_order(order)
        return order