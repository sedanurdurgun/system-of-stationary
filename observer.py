# observer.py
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from order import Order # Döngüsel bağımlılığı önlemek için

class Observer(ABC):
    """
    Observer arayüzü, konu nesnesindeki değişiklikleri almak isteyen sınıflar tarafından uygulanır.
    """
    @abstractmethod
    def update(self, order: 'Order'):
        """
        Gözlemcinin güncellemeleri alması için çağrılan soyut metot.
        Parametre olarak güncellenen sipariş nesnesini alır.
        """
        pass