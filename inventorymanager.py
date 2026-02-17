# inventorymanager.py
from product import Product, PhysicalProduct, DigitalProduct, ServiceProduct
from typing import List, Dict

class InventoryManager:
    """
    Envanter yöneticisi sınıfı. Singleton deseni uygular.
    Mağazadaki tüm ürünlerin stok bilgilerini yönetir.
    """
    _instance = None # Singleton örneğini tutar

    def __new__(cls):
        """
        Singleton desenini uygulamak için __new__ metodu override edildi.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.stock: Dict[int, Product] = {} # Ürün stoklarını tutacak dictionary: {product_id: Product_object}
        return cls._instance

    @staticmethod
    def get_instance():
        """
        InventoryManager'ın tek örneğini döndürür (Singleton deseni).
        """
        if InventoryManager._instance is None:
            InventoryManager._instance = InventoryManager() # __new__ metodu çağrılır
        return InventoryManager._instance

    def add_product(self, product: Product):
        """
        Envantere bir ürün ekler.
        """
        if product.product_id in self.stock:
            print(f"Uyarı: '{product.name}' (ID: {product.product_id}) zaten envanterde. Stok güncelleniyor.")
        self.stock[product.product_id] = product
        print(f"'{product.name}' (ID: {product.product_id}) envantere eklendi/güncellendi.")

    def update_stock(self, product_id: int, quantity: int) -> bool:
        """
        Belirtilen ürünün stoğunu günceller.
        Sadece fiziksel ürünler için stok azaltımı yapar.
        """
        product = self.stock.get(product_id)
        if product:
            try:
                # Ürünün kendi update_stock metodunu çağırır.
                # PhysicalProduct stok düşürür, diğerleri bilgilendirme yapar.
                product.update_stock(quantity)
                return True
            except ValueError as e:
                print(f"Stok güncelleme hatası: {e}")
                return False
        else:
            print(f"Hata: ID {product_id} ile ürün bulunamadı.")
            return False

    def get_product(self, product_id: int) -> Product | None:
        """
        Ürün ID'sine göre ürün nesnesini döndürür. Bulamazsa None döner.
        """
        return self.stock.get(product_id)

    def get_all_products(self) -> List[Product]:
        """
        Envanterdeki tüm ürünlerin listesini döndürür.
        """
        return list(self.stock.values())

    def get_stock_info(self):
        """
        Tüm ürünlerin stok bilgilerini tablo halinde listeler.
        """
        print("\n--- Stok Bilgileri ---")
        # Sütun genişlikleri düzenlendi
        print(f"{'ID':<4} | {'Ürün Adı':<25} | {'Tür':<10} | {'Kategori':<15} | {'Fiyat':<8} | {'Stok/Detay':<15}")
        print("-" * 90) # Çizgi uzunluğu ayarlandı
        if not self.stock:
            print("Envanterde henüz ürün bulunmamaktadır.")
            return

        for product_id, product in self.stock.items():
            stock_info = ""
            if isinstance(product, PhysicalProduct):
                stock_info = str(product.stock)
            elif isinstance(product, DigitalProduct):
                stock_info = f"Link: {product.download_link[:10]}..." # Link kısaltıldı
            elif isinstance(product, ServiceProduct):
                stock_info = f"Süre: {product.duration} gün"
            else:
                stock_info = "N/A"

            print(
                f"{product.product_id:<4} | {product.name:<25} | {product.get_type():<10} | "
                f"{product.category:<15} | {product.price:<8.2f} | {stock_info:<15}"
            )