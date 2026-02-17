# order_subject.py
from observer import Observer # Import Observer for type hinting
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from order import Order # Döngüsel bağımlılığı önlemek için

class OrderSubject:
    """
    Sipariş durum değişikliklerini gözlemcilere (müşterilere) bildirmekten sorumlu konu nesnesi.
    Observer desenini uygular.
    """
    def __init__(self):
        self.observers: List[Observer] = [] # Gözlemcileri (müşterileri) tutacak liste

    def attach(self, observer: Observer):
        """
        Yeni bir gözlemciyi (müşteriyi) konuya ekler.
        """
        if observer not in self.observers:
            self.observers.append(observer)
            # print(f"'{observer.name}' gözlemci olarak eklendi.") # Opsiyonel: hata ayıklama için

    def detach(self, observer: Observer):
        """
        Bir gözlemciyi (müşteriyi) konudan kaldırır.
        """
        if observer in self.observers:
            self.observers.remove(observer)
            # print(f"'{observer.name}' gözlemci olarak kaldırıldı.")

    def notify(self, order: 'Order'):
        """
        Tüm kayıtlı gözlemcilere (müşterilere) siparişin durumu hakkında bildirim gönderir.
        """
        for observer in list(self.observers):
            observer.update(order) # Her bir gözlemciye sipariş objesi ile bildirim gönderilir