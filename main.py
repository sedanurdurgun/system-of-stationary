# main.py
import sys
import os

# Modül yollarını doğru ayarlamak için (eğer doğrudan çalıştırılıyorsa)
# Bu, projeyi farklı dizin yapılarında çalıştırırken yardımcı olabilir.
script_dir = os.path.dirname(__file__)
sys.path.insert(0, script_dir)

from customer import Customer
from inventorymanager import InventoryManager
from product_console import run_product_menu
from customer_console import create_customer, customer_list, show_customer_profile
from order_console import create_order_interactive, update_order_status
from order_factory import OrderFactory
from product_factory import ProductFactory
from product_manager import ProductManager
from order_decorator import BaseOrder, OrderComponent
from order import OrderStatus  # OrderStatus enum'ını import et

# Bu liste BaseOrder veya OrderDecorator türünde objeler tutacak.
orders: list[OrderComponent] = []


def add_initial_products_to_inventory(inventory_manager: InventoryManager):
    """
    ProductFactory kullanarak InventoryManager'a bir dizi ilk ürün ekler.
    Bu, ürünlerin siparişler için kullanılabilir olmasını sağlar.
    """
    print("\nEnvantere başlangıç ürünleri ekleniyor...")
    # Physical Products
    inventory_manager.add_product(ProductFactory.create_product("physical", 1, "Klavye", "Elektronik", 500, 10))
    inventory_manager.add_product(ProductFactory.create_product("physical", 2, "Mouse", "Elektronik", 250, 5))
    inventory_manager.add_product(ProductFactory.create_product("physical", 3, "Defter", "Kırtasiye", 25, 50))
    inventory_manager.add_product(ProductFactory.create_product("physical", 4, "Kalem", "Kırtasiye", 10, 100))
    inventory_manager.add_product(ProductFactory.create_product("physical", 5, "Kitap: Python Programlama", "Kitap", 120, 20))
    inventory_manager.add_product(ProductFactory.create_product("physical", 6, "Akıllı Telefon", "Elektronik", 8000, 3))
    inventory_manager.add_product(ProductFactory.create_product("physical", 7, "Kulaklık", "Elektronik", 400, 15))
    inventory_manager.add_product(ProductFactory.create_product("physical", 8, "Masa Lambası", "Ev Eşyası", 150, 8))
    inventory_manager.add_product(ProductFactory.create_product("physical", 9, "Kahve Makinesi", "Mutfak Aletleri", 1200, 4))
    inventory_manager.add_product(ProductFactory.create_product("physical", 10, "Spor Ayakkabı", "Giyim", 750, 12))

    # Digital Products
    inventory_manager.add_product(ProductFactory.create_product("digital", 11, "E-Kitap: Yapay Zeka Temelleri", "E-Kitap", 75, "link-ai-book.pdf"))
    inventory_manager.add_product(ProductFactory.create_product("digital", 12, "Yazılım Lisansı: Pro Analiz", "Yazılım", 1500, "link-pro-analysis.zip"))
    inventory_manager.add_product(ProductFactory.create_product("digital", 13, "Müzik Albümü: Chill Mix", "Müzik", 30, "link-chill-mix.mp3"))
    inventory_manager.add_product(ProductFactory.create_product("digital", 14, "Online Kurs: Web Geliştirme", "Eğitim", 400, "link-web-dev-course.html"))

    # Service Products
    inventory_manager.add_product(ProductFactory.create_product("service", 15, "Premium Destek Paketi (1 Yıl)", "Hizmet", 1000, 365))
    inventory_manager.add_product(ProductFactory.create_product("service", 16, "Danışmanlık Hizmeti (Saatlik)", "Hizmet", 250, 1)) # Duration in hours or days? Let's assume days for consistency.
    inventory_manager.add_product(ProductFactory.create_product("service", 17, "Yazılım Kurulum Hizmeti", "Hizmet", 180, 1))
    inventory_manager.add_product(ProductFactory.create_product("service", 18, "Web Sitesi Bakım Hizmeti (Aylık)", "Hizmet", 300, 30))

    print("Başlangıç ürünleri envantere eklendi.")

def main_menu():
    """
    Ana menüyü gösterir ve kullanıcı seçimlerini işler.
    """
    inventory_manager = InventoryManager.get_instance()
    # add_initial_products_to_inventory(inventory_manager) # Her çalıştığında ürün eklemesin diye yorum satırı yaptım.

    while True:
        print("\n--- E-TİCARET PLATFORMU ---")
        print("1. Yeni Müşteri Oluştur")
        print("2. Müşteri Profili Görüntüle")
        print("3. Yeni Sipariş Oluştur")
        print("4. Sipariş Durumu Güncelle")
        print("5. Tüm Siparişleri Görüntüle")
        print("6. Ürün Yönetimi")
        print("0. Çıkış")

        choice = input("Seçiminiz: ").strip()

        if choice == "1":
            create_customer()
        elif choice == "2":
            if not customer_list:
                print("Henüz kayıtlı müşteri yok.")
                continue
            for i, cust in enumerate(customer_list):
                print(f"{i + 1}. {cust.name} (ID: {cust.customer_id})")
            try:
                cust_index = int(input("Profilini görüntülemek istediğiniz müşterinin numarasını girin: ")) - 1
                if 0 <= cust_index < len(customer_list):
                    show_customer_profile(customer_list[cust_index])
                else:
                    print("Geçersiz müşteri numarası.")
            except ValueError:
                print("Lütfen geçerli bir sayı girin.")
        elif choice == "3":
            if not customer_list:
                print("Sipariş oluşturmak için önce bir müşteri oluşturmalısınız.")
                continue
            if not inventory_manager.get_all_products():
                print("Sipariş oluşturmak için envanterde ürün bulunmalıdır.")
                continue

            print("\n--- Sipariş Oluşturulacak Müşteriyi Seçin ---")
            for i, cust in enumerate(customer_list):
                print(f"{i + 1}. {cust.name} (ID: {cust.customer_id})")
            try:
                cust_index = int(input("Sipariş oluşturmak istediğiniz müşterinin numarasını girin: ")) - 1
                if 0 <= cust_index < len(customer_list):
                    selected_customer = customer_list[cust_index]
                    # create_order_interactive artık InventoryManager'ı kendisi alıyor
                    new_order = create_order_interactive(selected_customer)
                    if new_order:
                        orders.append(new_order)
                        print(f"Sipariş {new_order.order_id} başarıyla eklendi.")
                else:
                    print("Geçersiz müşteri numarası.")
            except ValueError:
                print("Lütfen geçerli bir sayı girin.")
        elif choice == "4":
            if not orders:
                print("Güncellenecek sipariş bulunmamaktadır.")
                continue
            print("\n--- Güncellenecek Siparişi Seçin ---")
            for i, order_obj in enumerate(orders):
                # __getattr__ sayesinde doğrudan erişim
                print(f"{i + 1}. Sipariş ID: {order_obj.order_id}, Müşteri: {order_obj.customer.name}, Durum: {order_obj.status.value}")

            try:
                order_index = int(input("Durumunu güncellemek istediğiniz siparişin numarasını girin: ")) - 1
                if 0 <= order_index < len(orders):
                    update_order_status(orders[order_index])  # orders[order_index] zaten BaseOrder/Decorator
                else:
                    print("Geçersiz sipariş numarası.")
            except ValueError:
                print("Lütfen geçerli bir sayı girin.")

        elif choice == "5":
            if not orders:
                print("Görüntülenecek sipariş bulunmamaktadır.")
                continue
            print("\n--- Tüm Siparişler ---")
            for i, order_obj in enumerate(orders):
                # __getattr__ sayesinde doğrudan erişim ve metod çağrıları
                print(f"Sipariş ID: {order_obj.order_id}")
                print(f"  Açıklama: {order_obj.get_description()}")
                print(f"  Toplam Maliyet: {order_obj.get_total_cost():.2f}₺")
                print(f"  Müşteri: {order_obj.customer.name}")
                print(f"  Durum: {order_obj.status.value}")  # Enum'dan value alınmalı
                print("-" * 30)

        elif choice == "6":
            run_product_menu()

        elif choice == "0":
            print("E-Ticaret Platformundan çıkılıyor. Hoşça kalın!")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")


if __name__ == "__main__":
    # Uygulama başlatılırken InventoryManager'a başlangıç ürünleri eklenir
    initial_inventory_manager = InventoryManager.get_instance()
    add_initial_products_to_inventory(initial_inventory_manager)
    main_menu()