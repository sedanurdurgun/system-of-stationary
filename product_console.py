# product_console.py
from inventorymanager import InventoryManager
from product_manager import ProductManager # ProductManager import edildi

def run_product_menu():
    """
    Ürün yönetimi için interaktif konsol menüsünü çalıştırır.
    """
    inventory_manager = InventoryManager.get_instance() # Singleton örneği
    product_manager = ProductManager() # ProductManager örneği

    while True:
        print("\n--- ÜRÜN YÖNETİM PANELİ ---")
        print("1. Tüm Ürünleri Listele (Envanter)")
        print("2. Kategoriye Göre Ürünleri Filtrele")
        print("3. Ürün ID ile Ürün Bul")
        print("4. Mevcut Kategorileri Listele") # Yeni seçenek
        print("0. Ana Menüye Dön")

        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            inventory_manager.get_stock_info()
        elif secim == "2":
            category_name = input("Filtrelemek istediğiniz kategori adını girin: ").strip()
            product_manager.filter_products_by_category(category_name)
        elif secim == "3":
            try:
                product_id = int(input("Bulmak istediğiniz ürün ID'sini girin: "))
                product_manager.search_product_by_id(product_id)
            except ValueError:
                print("Hata: Lütfen geçerli bir sayı girin.")
        elif secim == "4": # Yeni seçenek
            product_manager.list_categories()
        elif secim == "0":
            print("Ürün Yönetim Paneli'nden çıkılıyor.")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")