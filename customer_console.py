# customer_console.py
import uuid
from customer import Customer

# Bu liste, uygulamanın çalıştığı sürece müşteri verilerini tutar.
customer_list: list[Customer] = []

def create_customer() -> Customer:
    """
    Kullanıcıdan bilgi alarak yeni bir müşteri oluşturur ve listeye ekler.
    """
    print("\n--- Yeni Müşteri Kaydı ---")
    name = input("İsim-soyisim: ").strip()
    email = input("E-posta: ").strip()

    if not name or not email:
        print("İsim ve E-posta boş bırakılamaz.")
        return None

    # Daha robust bir benzersiz ID üretimi için UUID kullanıldı
    customer_id = str(uuid.uuid4())
    new_customer = Customer(customer_id, name, email)
    customer_list.append(new_customer)
    print(f"'{name}' başarıyla kayıt edildi. Müşteri ID: {customer_id}")
    return new_customer

def show_customer_profile(customer: Customer):
    """
    Belirtilen müşterinin profilini ve sipariş geçmişini görüntüler.
    """
    if customer:
        customer.display_profile()
        customer.display_order_history()
    else:
        print("Müşteri bulunamadı.")