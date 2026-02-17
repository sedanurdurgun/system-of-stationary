# product.py
from abc import ABC, abstractmethod

class Product(ABC): # Abstract Base Class olarak tanımlandı
    """
    Mağazadaki tüm ürünler için temel soyut sınıf.
    """
    def __init__(self, product_id: int, name: str, category: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock # Fiziksel ürünler için geçerli, diğerleri için 0 olabilir

    @abstractmethod
    def update_stock(self, quantity: int):
        """
        Ürünün stoğunu belirtilen miktar kadar azaltır veya ilgili işlemi yapar.
        Alt sınıflar bu metodu kendi türlerine göre uygulamalıdır.
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        Ürünün genel türünü döndürür. Alt sınıflar bu metodu uygulamalıdır.
        """
        pass

    def __str__(self):
        """
        Ürün bilgilerini özetleyen string temsilini döndürür.
        """
        return (f"ID: {self.product_id:<3} | {self.name:<20} | Tür: {self.get_type():<10} | "
                f"Kategori: {self.category:<12} | Fiyat: {self.price:>7.2f}₺ | Stok: {self.stock}")


class PhysicalProduct(Product):
    """
    Fiziksel ürünler için sınıf. Stok takibi yapılır.
    """
    def __init__(self, product_id: int, name: str, category: str, price: float, stock: int):
        super().__init__(product_id, name, category, price, stock)

    def update_stock(self, quantity: int):
        """
        Fiziksel ürünün stoğunu belirtilen miktar kadar azaltır.
        Yetersiz stok durumunda ValueError döndürür.
        """
        if quantity > self.stock:
            raise ValueError(f"Yeterli stok yok! '{self.name}' için mevcut stok: {self.stock} adet. İstenen: {quantity} adet.")
        self.stock -= quantity
        print(f"'{self.name}' (ID: {self.product_id}) stoğu güncellendi. Yeni stok: {self.stock}")

    def get_type(self) -> str:
        return "Physical"

    def __str__(self):
        return (f"ID: {self.product_id:<3} | {self.name:<20} | Tür: {self.get_type():<10} | "
                f"Kategori: {self.category:<12} | Fiyat: {self.price:>7.2f}₺ | Stok: {self.stock:>5}")


class DigitalProduct(Product):
    """
    Dijital ürünler için sınıf. Stok takibi yapılmaz (sanal stok 0'dır).
    """
    def __init__(self, product_id: int, name: str, category: str, price: float, download_link: str):
        # Dijital ürünlerin stoğu yoktur, bu yüzden 0 olarak set edilir
        super().__init__(product_id, name, category, price, stock=0)
        self.download_link = download_link

    def get_type(self) -> str:
        return "Digital"

    def update_stock(self, quantity: int):
        """
        Dijital ürünler için stok güncelleme mantığı yoktur.
        """
        print(f"Bilgi: '{self.name}' bir dijital üründür, stok takibi yapılmaz.")

    def __str__(self):
        return (f"ID: {self.product_id:<3} | {self.name:<20} | Tür: {self.get_type():<10} | "
                f"Kategori: {self.category:<12} | Fiyat: {self.price:>7.2f}₺ | Link: {self.download_link}")


class ServiceProduct(Product):
    """
    Hizmet ürünleri için sınıf. Stok takibi yapılmaz (sanal stok 0'dır).
    """
    def __init__(self, product_id: int, name: str, category: str, price: float, duration: int):
        # Hizmet ürünlerinin stoğu yoktur, bu yüzden 0 olarak set edilir
        super().__init__(product_id, name, category, price, stock=0)
        self.duration = duration # Örneğin, gün bazlı süre

    def get_type(self) -> str:
        return "Service"

    def update_stock(self, quantity: int):
        """
        Hizmet ürünleri için stok güncelleme mantığı yoktur.
        """
        print(f"Bilgi: '{self.name}' bir hizmet ürünüdür, stok takibi yapılmaz.")

    def __str__(self):
        return (f"ID: {self.product_id:<3} | {self.name:<20} | Tür: {self.get_type():<10} | "
                f"Kategori: {self.category:<12} | Fiyat: {self.price:>7.2f}₺ | Süre: {self.duration} gün")