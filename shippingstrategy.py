# shippingstrategy.py
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from order import Order # Döngüsel bağımlılığı önlemek için

class ShippingStrategy(ABC):
    """
    Kargo ücreti hesaplama stratejileri için soyut temel sınıf.
    Strategy desenini uygular.
    """
    @abstractmethod
    def calculate(self, order: 'Order') -> float:
        """
        Belirtilen sipariş için kargo ücretini hesaplar.
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Kargo stratejisinin adını döndürür.
        """
        pass


class FastShipping(ShippingStrategy):
    """
    Hızlı kargo stratejisi. Sabit ücret ve sipariş toplamının belirli bir yüzdesi.
    """
    def calculate(self, order: 'Order') -> float:
        return 30 + 0.05 * order.total  # Sabit 30₺ + %5 sipariş tutarı

    def get_name(self) -> str:
        return "Hızlı Kargo"

class CheapShipping(ShippingStrategy):
    """
    Ekonomik kargo stratejisi. Sabit ücret ve sipariş toplamının daha düşük bir yüzdesi.
    """
    def calculate(self, order: 'Order') -> float:
        return 10 + 0.02 * order.total  # Sabit 10₺ + %2 sipariş tutarı

    def get_name(self) -> str:
        return "Ekonomik Kargo"

class DroneShipping(ShippingStrategy):
    """
    Drone kargo stratejisi. Belirli koşullar (örneğin sipariş ağırlığı) için uygun olabilir.
    """
    def calculate(self, order: 'Order') -> float:
        # Drone kargosu sadece küçük ve hafif siparişler için uygundur.
        # Burada siparişin toplam ağırlığı, hacmi gibi gerçekçi kriterler eklenebilir.
        # Basitlik için sadece sabit bir ücret.
        # if sum(p.weight * q for p, q in order.products) > 5: # Örnek kontrol
        #     raise ValueError("Drone kargosu bu sipariş için uygun değil.")
        return 50 # Sabit 50₺ drone kargo ücreti

    def get_name(self) -> str:
        return "Drone Kargo"