# product_factory.py
from product import PhysicalProduct, DigitalProduct, ServiceProduct
from typing import Any

class ProductFactory:
    """
    Farklı türde ürün nesneleri oluşturmak için Factory Method deseni uygular.
    """
    @staticmethod
    def create_product(product_type: str, *args, **kwargs) -> Any:
        """
        Belirtilen türe göre bir ürün nesnesi oluşturur.

        Args:
            product_type (str): Oluşturulacak ürünün türü ('physical', 'digital', 'service').
            *args: Ürün sınıfının yapıcı metoduna iletilecek konum bağımsız değişkenleri.
            **kwargs: Ürün sınıfının yapıcı metoduna iletilecek anahtar kelime bağımsız değişkenleri.

        Returns:
            Product: Oluşturulan ürün nesnesi.

        Raises:
            ValueError: Geçersiz bir ürün türü belirtildiğinde.
        """
        if product_type == "physical":
            # PhysicalProduct(product_id, name, category, price, stock)
            return PhysicalProduct(*args, **kwargs) # <-- BURASI DA DOĞRU OLACAK!
        elif product_type == "digital":
            # DigitalProduct(product_id, name, category, price, download_link)
            return DigitalProduct(*args, **kwargs)
        elif product_type == "service":
            # ServiceProduct(product_id, name, category, price, duration)
            return ServiceProduct(*args, **kwargs)
        else:
            raise ValueError(f"Geçersiz ürün türü: '{product_type}'. Desteklenen türler: 'physical', 'digital', 'service'.")