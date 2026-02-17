# order_console.py
import uuid  # UUID modülünü import et
from typing import List, Tuple, Optional
from inventorymanager import InventoryManager
from customer import Customer
from product import Product, PhysicalProduct  # Product ve PhysicalProduct'ı import et
from order_factory import OrderFactory
from order import Order, OrderStatus  # Order ve OrderStatus enum'ını import et
from order_decorator import BaseOrder, FragileDecorator, InsuranceDecorator, GiftWrapDecorator, OrderComponent
from shippingstrategy import FastShipping, CheapShipping, DroneShipping  # ShippingStrategy'leri import et
from shipping_selector import choose_optimal_shipping_strategy  # Yeni otomatik kargo seçimi fonksiyonu


def create_order_interactive(customer: Customer) -> Optional[OrderComponent]:
    """
    Kullanıcı etkileşimi ile bir sipariş oluşturur.
    Müşteri parametre olarak alınır. Ürünler envanterden seçilir.
    Dönen değer bir BaseOrder veya dekore edilmiş bir OrderDecorator nesnesidir.
    """
    print("\n--- Sipariş Oluşturma ---")
    inventory = InventoryManager.get_instance()
    sepettekiler: List[Tuple[Product, int]] = []  # (ürün nesnesi, adet) tuple'ları

    print("\nMevcut Ürünler:")
    inventory.get_stock_info()  # Envanterdeki ürünleri görüntüler

    while True:
        try:
            urun_id_input = input("Eklemek istediğiniz ürün ID'si (bitirmek için 'q'): ").strip()
            if urun_id_input.lower() == "q":
                break

            urun_id = int(urun_id_input)
            quantity = int(input("Adet: ").strip())

            if quantity <= 0:
                print("Adet 0'dan büyük olmalıdır.")
                continue

            product_to_add = inventory.get_product(urun_id)

            if product_to_add:
                # Fiziksel ürünler için stok kontrolü
                if isinstance(product_to_add, PhysicalProduct):
                    if product_to_add.stock < quantity:
                        print(f"Yeterli stok yok! Mevcut stok: {product_to_add.stock} adet.")
                        continue
                sepettekiler.append((product_to_add, quantity))
                print(f"'{product_to_add.name}' ürününden {quantity} adet sepete eklendi.")
            else:
                print("Ürün bulunamadı. Lütfen geçerli bir ID girin.")
        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı veya 'q' girin.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    if not sepettekiler:
        print("Sepete ürün eklenmedi. Sipariş oluşturma iptal edildi.")
        return None

    # Sipariş türü seçimi
    print("\n--- Sipariş Türü Seçimi ---")
    print("1. Standart Sipariş")
    print("2. Hızlı Sipariş")
    print("3. Abonelik Siparişi")
    print("4. Ön Sipariş")
    print("5. Hediye Siparişi")
    print("6. Toplu Sipariş")
    order_type_choice = input("Sipariş türünü seçin (numara): ").strip()
    order_type_map = {
        "1": "standard", "2": "express", "3": "subscription",
        "4": "preorder", "5": "gift", "6": "bulk"
    }
    selected_order_type = order_type_map.get(order_type_choice, "standard")
    kwargs = {}
    if selected_order_type == "preorder":
        kwargs["expected_delivery_date"] = input("Tahmini teslim tarihi girin (örn: 2025-12-31): ").strip()
    elif selected_order_type == "gift":
        kwargs["gift_note"] = input("Hediye notu girin: ").strip()

    # Sipariş oluşturma (Factory Method)
    try:
        new_order_base = OrderFactory.create_order(selected_order_type, customer, sepettekiler, **kwargs)
        print(f"Sipariş {new_order_base.order_id} başarıyla oluşturuldu. Temel Maliyet: {new_order_base.total:.2f}₺")

        # Otomatik kargo stratejisi seçimi (Strategy Pattern)
        selected_shipping_strategy = choose_optimal_shipping_strategy(new_order_base)
        new_order_base.set_shipping_strategy(selected_shipping_strategy)
        print(f"Kargo maliyeti ({selected_shipping_strategy.get_name()}): {new_order_base.get_shipping_cost():.2f}₺")

        # Siparişi bir BaseOrder objesine sararak dekoratör zinciri başlatılır
        decorated_order: OrderComponent = BaseOrder(new_order_base)

        # Ek hizmetler (Decorator Pattern)
        print("\n--- Ek Hizmetler (Evet için 'e' yazın) ---")
        if input("Kırılabilir etiketi ister misiniz? (e/h): ").lower() == "e":
            decorated_order = FragileDecorator(decorated_order)

        if input("Sigortalı gönderim ister misiniz? (e/h): ").lower() == "e":
            decorated_order = InsuranceDecorator(decorated_order)

        if input("Hediye paketi ister misiniz? (e/h): ").lower() == "e":
            decorated_order = GiftWrapDecorator(decorated_order)

        print("\n--- Sipariş Özeti ---")
        print("Açıklama: ", decorated_order.get_description())
        print("Toplam ödenecek: ", decorated_order.get_total_cost(), "₺")

        return decorated_order

    except ValueError as e:
        print(f"Sipariş oluşturma hatası: {e}")
        return None
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        return None


def update_order_status(order_to_update: OrderComponent):
    """
    Bir siparişin durumunu günceller.
    order_to_update bir BaseOrder veya Decorator objesi olabilir.
    """
    # __getattr__ sayesinde doğrudan erişim
    print(f"\nSipariş #{order_to_update.order_id} mevcut durumu: {order_to_update.status.value}")

    print("\n--- Sipariş Durumları ---")
    for i, status_enum in enumerate(OrderStatus):
        print(f"{i + 1}. {status_enum.value}")

    while True:
        try:
            status_choice = int(input("Yeni durumu seçin (numara): ").strip())
            if 1 <= status_choice <= len(OrderStatus._member_names_):
                new_status_enum = list(OrderStatus)[status_choice - 1]
                order_to_update.update_status(new_status_enum)  # update_status OrderStatus objesi bekler
                print(f"Sipariş durumu '{new_status_enum.value}' olarak güncellendi.")
                break
            else:
                print("Geçersiz numara. Lütfen listeden bir numara seçin.")
        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin.")
        except Exception as e:
            print(f"Durum güncelleme hatası: {e}")