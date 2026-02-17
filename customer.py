# customer.py
from observer import Observer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from order import Order # Döngüsel bağımlılığı önlemek için

class Customer(Observer):
    """
    Müşteri bilgilerini ve sipariş geçmişini tutan sınıf.
    Observer arayüzünü uygulayarak sipariş durumu değişikliklerinden haberdar olur.
    """
    def __init__(self, customer_id: str, name: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.orders = [] # Müşterinin verdiği siparişlerin listesi

    def add_order(self, order: 'Order'):
        """
        Müşterinin sipariş geçmişine yeni bir sipariş ekler.
        """
        self.orders.append(order)

    def display_profile(self):
        """
        Müşterinin profil bilgilerini görüntüler.
        """
        print("\n--- Müşteri Profili ---")
        print(f"ID: {self.customer_id}")
        print(f"Ad: {self.name}")
        print(f"E-posta: {self.email}")
        print(f"Sipariş sayısı: {len(self.orders)}")

    def display_order_history(self):
        """
        Müşterinin geçmiş siparişlerini görüntüler.
        """
        if not self.orders:
            print("\nHenüz hiç siparişiniz yok.")
            return
        print("\n--- Sipariş Geçmişi ---")
        for order in self.orders:
            # order'ın __str__ metodunu kullanarak özet görüntüleme
            print(f"- {order}")

    def update(self, order: 'Order'):  # Observer arayüzü uygulaması
        """
        Sipariş durumu güncellendiğinde çağrılır ve müşteriye bildirim gönderir.
        """
        print(f"\n[BİLDİRİM] Sayın {self.name}, siparişiniz (ID: {order.order_id}) güncellendi. Yeni durum: {order.status.value}")

    def __str__(self):
        """
        Müşteri nesnesinin okunabilir string temsilini döndürür.
        """
        return f"Müşteri: {self.name} (ID: {self.customer_id}, Email: {self.email})"