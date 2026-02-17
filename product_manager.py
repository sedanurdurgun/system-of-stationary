# product_manager.py
from inventorymanager import InventoryManager
from product import Product, PhysicalProduct, DigitalProduct, ServiceProduct
from typing import List

class ProductManager:
    """
    Ürün listeleme, filtreleme ve arama gibi işlemlerden sorumlu yardımcı sınıf.
    Ürün verilerini InventoryManager'dan alır.
    """
    def __init__(self):
        self.inventory_manager = InventoryManager.get_instance()

    def _print_product_table(self, products: List[Product]):
        """
        Ürün listesini tablo halinde görüntüler. Yardımcı metot.
        """
        if not products:
            print("Gösterilecek ürün bulunmamaktadır.")
            return

        print(f"{'ID':<4} | {'Ürün Adı':<25} | {'Tür':<10} | {'Kategori':<15} | {'Fiyat':<8} | {'Stok/Detay':<15}")
        print("-" * 90)
        for product in products:
            stock_info = ""
            if isinstance(product, PhysicalProduct):
                stock_info = str(product.stock)
            elif isinstance(product, DigitalProduct):
                stock_info = f"Link: {product.download_link[:10]}..."
            elif isinstance(product, ServiceProduct):
                stock_info = f"Süre: {product.duration} gün"
            else:
                stock_info = "N/A"
            print(
                f"{product.product_id:<4} | {product.name:<25} | {product.get_type():<10} | "
                f"{product.category:<15} | {product.price:<8.2f} | {stock_info:<15}"
            )

    def list_all_products(self):
        """
        Envanterdeki tüm ürünleri tablo halinde listeler.
        """
        print("\n--- Tüm Ürünler ---")
        self._print_product_table(self.inventory_manager.get_all_products())

    def filter_products_by_category(self, category_name: str):
        """
        Belirli bir kategoriye göre ürünleri filtreler ve tablo halinde listeler.
        """
        all_products = self.inventory_manager.get_all_products()
        found_products = [
            p for p in all_products
            if p.category.lower() == category_name.lower()
        ]
        if found_products:
            print(f"\n--- '{category_name}' Kategorisindeki Ürünler ---")
            self._print_product_table(found_products)
        else:
            print(f"'{category_name}' kategorisine ait ürün bulunamadı.")

    def list_categories(self):
        """
        Mevcut tüm ürün kategorilerini listeler.
        """
        products = self.inventory_manager.get_all_products()
        categories = sorted(list(set(p.category for p in products)))
        if not categories:
            print("Henüz kategori bulunmamaktadır.")
            return

        print("\n--- Mevcut Ürün Kategorileri ---")
        for category in categories:
            print(f"- {category}")

    def search_product_by_id(self, product_id: int):
        """
        Ürün ID'sine göre ürün arar ve bilgilerini gösterir.
        """
        product = self.inventory_manager.get_product(product_id)
        if product:
            print("\n--- Ürün Bilgileri ---")
            print(product) # Calls the __str__ method of the product object
        else:
            print(f"ID {product_id} ile ürün bulunamadı.")