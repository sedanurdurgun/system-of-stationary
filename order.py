# order.py
from order_subject import OrderSubject
from typing import List, Tuple
from product import Product # For type hinting
from enum import Enum # Sipariş durumları için Enum
from customer import Customer # Type hinting için

class OrderStatus(Enum):
    """
    Siparişin mevcut durumlarını temsil eden Enum.
    """
    PREPARING = "Hazırlanıyor"
    SHIPPED = "Kargoya Verildi"
    DELIVERED = "Teslim Edildi"
    CANCELLED = "İptal Edildi"
    RETURNED = "İade Edildi"
    PENDING_PAYMENT = "Ödeme Bekleniyor"

    def __str__(self):
        return self.value

class Order:
    """
    Sipariş bilgilerini, ürün listesini ve durumunu tutan temel sınıf.
    Observer deseni için konu (subject) görevi görür.
    """
    def __init__(self, order_id: str, customer: Customer, products: List[Tuple[Product, int]]):
        self.order_id = order_id
        self.customer = customer
        self.products = products  # (ürün, adet) tuple'larından oluşan liste
        self.total = self.calculate_total() # Kargo ve ek hizmetler hariç temel toplam
        self.status: OrderStatus = OrderStatus.PREPARING # Başlangıç durumu Enum olarak
        self.shipping_strategy = None # Kargo stratejisi
        self._subject = OrderSubject()
        self._subject.attach(customer)  # Müşteri, sipariş durumu değişikliklerini dinlemek için bağlanır

    def calculate_total(self) -> float:
        """
        Siparişin ürün maliyetini hesaplar.
        """
        return sum(product.price * qty for product, qty in self.products)

    def set_shipping_strategy(self, strategy):
        """
        Sipariş için kargo stratejisini ayarlar.
        """
        self.shipping_strategy = strategy

    def get_shipping_cost(self) -> float:
        """
        Seçilen kargo stratejisine göre kargo maliyetini hesaplar.
        """
        if self.shipping_strategy is None:
            raise Exception("Kargo stratejisi seçilmedi.")
        return self.shipping_strategy.calculate(self) # Sipariş objesi, kargo stratejisine gönderilir

    def update_status(self, new_status: OrderStatus):
        """
        Siparişin durumunu günceller ve gözlemcilere (müşteriye) bildirim gönderir.
        """
        if not isinstance(new_status, OrderStatus):
            raise ValueError("Geçersiz sipariş durumu. Lütfen OrderStatus enum'ından bir değer kullanın.")
        self.status = new_status
        self._subject.notify(self) # Gözlemcilere bildirim gönderilir

    def get_type(self) -> str:
        """
        Siparişin genel türünü döndürür. Alt sınıflar override edebilir.
        """
        return "Standard"

    def __str__(self):
        """
        Sipariş bilgilerini özetleyen string temsilini döndürür.
        """
        product_names = ", ".join([f"{p.name} (x{q})" for p, q in self.products])
        return (f"Sipariş ID: {self.order_id} | Müşteri: {self.customer.name} | "
                f"Ürünler: [{product_names}] | Toplam: {self.total:.2f}₺ | Durum: {self.status.value}")

# --- Sipariş Alt Sınıfları (Factory Method için) ---

class ExpressOrder(Order):
    """
    Ekspres sipariş sınıfı. Ekstra ücret veya farklı hesaplama içerebilir.
    """
    def calculate_total(self) -> float:
        base_total = super().calculate_total()
        return base_total * 1.10 # %10 ek ücret (örneğin hızlandırılmış işlem için)

    def get_type(self) -> str:
        return "Express"

class SubscriptionOrder(Order):
    """
    Abonelik siparişi sınıfı. Belirli bir indirim veya farklı işleme mantığı olabilir.
    """
    def calculate_total(self) -> float:
        return super().calculate_total() * 0.85  # %15 indirim

    def get_type(self) -> str:
        return "Subscription"

class PreOrder(Order):
    """
    Ön sipariş sınıfı. Tahmini teslim tarihi gibi ek bilgiler içerir.
    """
    def __init__(self, order_id: str, customer: Customer, products: List[Tuple[Product, int]], expected_delivery_date: str):
        super().__init__(order_id, customer, products)
        self.expected_delivery_date = expected_delivery_date

    def get_type(self) -> str:
        return "PreOrder"

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} - Tahmini Teslim: {self.expected_delivery_date}"

class GiftOrder(Order):
    """
    Hediye siparişi sınıfı. Hediye notu gibi ek bilgiler içerir.
    """
    def __init__(self, order_id: str, customer: Customer, products: List[Tuple[Product, int]], gift_note: str):
        super().__init__(order_id, customer, products)
        self.gift_note = gift_note

    def get_type(self) -> str:
        return "Gift"

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} - Hediye Notu: '{self.gift_note}'"


class BulkOrder(Order):
    """
    Toplu sipariş sınıfı. Büyük siparişler için indirim içerebilir.
    """
    def calculate_total(self) -> float:
        base_total = super().calculate_total()
        if base_total > 1000: # Örnek: 1000 TL üzeri toplu siparişlerde %5 indirim
            return base_total * 0.95
        return base_total

    def get_type(self) -> str:
        return "Bulk"