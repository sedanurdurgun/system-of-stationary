# order_decorator.py
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

# Döngüsel bağımlılıkları önlemek için
if TYPE_CHECKING:
    from order import Order
    from customer import Customer
    from order import OrderStatus


class OrderComponent(ABC):
    """
    Sipariş bileşenlerinin temel arayüzü. Hem ana sipariş hem de dekoratörler bu arayüzü uygular.
    """
    @abstractmethod
    def get_description(self) -> str:
        """Siparişin açıklamasını döndürür."""
        pass

    @abstractmethod
    def get_total_cost(self) -> float:
        """Siparişin toplam maliyetini döndürür."""
        pass

    # __getattr__ için özel bir abstract method tanımlamaya gerek yok,
    # ancak OrderComponent'ten türeyen tüm sınıfların
    # Order nesnesinin özelliklerine erişilebilir olmasını sağlamalıyız.
    # Bu, BaseOrder ve OrderDecorator'da uygulanacak.


class BaseOrder(OrderComponent):
    """
    Dekorasyon zincirinin temel bileşeni olan gerçek sipariş nesnesini sarar.
    """
    def __init__(self, order: 'Order'):
        self.order = order

    def get_description(self) -> str:
        """Temel siparişin açıklamasını döndürür."""
        return str(self.order)

    def get_total_cost(self) -> float:
        """
        Temel siparişin toplam maliyetini (kargo dahil) döndürür.
        """
        cost = self.order.total
        if self.order.shipping_strategy:
            cost += self.order.get_shipping_cost()
        return cost

    def __getattr__(self, name: str) -> Any:
        """
        Dekoratör zinciri aracılığıyla temel Order nesnesinin özelliklerine ve metotlarına erişimi sağlar.
        """
        # Temel 'order' nesnesinin özelliklerine erişimi yönlendir
        if hasattr(self.order, name):
            return getattr(self.order, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")


class OrderDecorator(OrderComponent):
    """
    Tüm sipariş dekoratörleri için temel soyut sınıf.
    Dekoratörler zincirleme bir şekilde birbirine eklenebilir.
    """
    def __init__(self, component: OrderComponent):
        self.component = component

    def get_description(self) -> str:
        """Alt bileşenin açıklamasını döndürür."""
        return self.component.get_description()

    def get_total_cost(self) -> float:
        """Alt bileşenin maliyetini döndürür."""
        return self.component.get_total_cost()

    def __getattr__(self, name: str) -> Any:
        """
        Dekoratör zinciri aracılığıyla temel Order nesnesinin özelliklerine ve metotlarına erişimi sağlar.
        Bu, dekore edilmiş nesne üzerinde temel Order'ın özelliklerine erişimi sağlar.
        """
        # Eğer attribute alt bileşende varsa, ona yönlendir
        if hasattr(self.component, name):
            return getattr(self.component, name)
        # Eğer alt bileşen de bir OrderComponent ise ve attribute'ı yoksa,
        # onun içindeki order'a bakması gerekir. Bu zincirleme __getattr__ sayesinde otomatikleşir.
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")


class FragileDecorator(OrderDecorator):
    """
    Siparişin kırılabilir etiketli olduğunu belirten dekoratör.
    Maliyete ek ücret ekler.
    """
    def get_description(self) -> str:
        return self.component.get_description() + " + Kırılabilir Etiketi"

    def get_total_cost(self) -> float:
        return self.component.get_total_cost() + 20  # 20 TL ek ücret


class InsuranceDecorator(OrderDecorator):
    """
    Siparişin sigortalı gönderim olduğunu belirten dekoratör.
    Maliyete ek ücret ekler.
    """
    def get_description(self) -> str:
        return self.component.get_description() + " + Sigortalı Gönderim"

    def get_total_cost(self) -> float:
        return self.component.get_total_cost() + 35  # 35 TL ek ücret


class GiftWrapDecorator(OrderDecorator):
    """
    Siparişin hediye paketi olduğunu belirten dekoratör.
    Maliyete ek ücret ekler.
    """
    def get_description(self) -> str:
        return self.component.get_description() + " + Hediye Paketi"

    def get_total_cost(self) -> float:
        return self.component.get_total_cost() + 15  # 15 TL ek ücret