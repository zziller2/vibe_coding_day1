import json
from datetime import datetime
import os

FILE_NAME = "inventory.json"

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        inventory = json.load(f)
else:
    inventory = []

def save_inventory():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)

def show_inventory():
    print("\n📦 현재 재고 목록:")
    if not inventory:
        print("⚠️ 재고가 없습니다.")
        return
    for i, item in enumerate(inventory, 1):
        print(f"{i}. {item['이름']} - 수량: {item['수량']}개, 유통기한: {item['유통기한']}")

def alert_expiry():
    print("\n⏰ 유통기한 경고:")
    today = datetime.today()
    for item in inventory:
        expiry = datetime.strptime(item["유통기한"], "%Y-%m-%d")
        days_left = (expiry - today).days
    if days_left < 0:
        print(f"❌ [기한지남] {item['이름']} - 유통기한 {item['유통기한']} (D+{abs(days_left)} 경과)")
    elif days_left <= 60:
        print(f"⚠️ [임박주의] {item['이름']} - 유통기한 {item['유통기한']} (D-{days_left})")

def add_item():
    print("\n➕ 재고 추가")
    name = input("재료 이름: ")
    if name.lower() == "q":
        return
    try:
        qty = int(input("수량: "))
        expiry = input("유통기한 (YYYY-MM-DD): ")
        datetime.strptime(expiry, "%Y-%m-%d")
    except ValueError:
        print("❌ 잘못된 입력입니다.")
        return
    inventory.append({"이름": name, "수량": qty, "유통기한": expiry})
    print(f"✅ '{name}' 항목이 추가되었습니다.")
    save_inventory()

def delete_item():
    show_inventory()
    if not inventory:
        return
    try:
        num = int(input("\n삭제할 항목 번호를 입력하세요 (취소: 0): "))
        if num == 0:
            print("❎ 삭제 취소")
            return
        removed = inventory.pop(num - 1)
        print(f"🗑️ '{removed['이름']}' 삭제 완료")
        save_inventory()
    except (ValueError, IndexError):
        print("❌ 잘못된 번호입니다.")

def edit_item():
    show_inventory()
    if not inventory:
        return

    try:
        num = int(input("\n수정할 항목 번호를 입력하세요 (취소: 0): "))
        if num == 0:
            print("❎ 수정 취소")
            return
        item = inventory[num - 1]
    except (ValueError, IndexError):
        print("❌ 잘못된 번호입니다.")
        return

    print(f"\n🛠️ '{item['이름']}' 항목 수정")

    new_qty = input(f"수량 수정 (현재: {item['수량']}) → 입력 안하면 유지: ")
    if new_qty.strip():
        try:
            item["수량"] = int(new_qty)
        except ValueError:
            print("❌ 숫자가 아닙니다. 수량 수정은 건너뜁니다.")

    new_expiry = input(f"유통기한 수정 (현재: {item['유통기한']}) → 입력 안하면 유지: ")
    if new_expiry.strip():
        try:
            datetime.strptime(new_expiry, "%Y-%m-%d")
            item["유통기한"] = new_expiry
        except ValueError:
            print("❌ 날짜 형식이 올바르지 않습니다. YYYY-MM-DD")

    save_inventory()
    print(f"✅ '{item['이름']}' 수정 완료")

while True:
    print("\n====== 치과 재고관리 프로그램 ======")
    print("1. 재고 보기")
    print("2. 재고 추가")
    print("3. 재고 삭제")
    print("4. 유통기한 경고 보기")
    print("5. 재고 수정")
    print("6. 종료")

    choice = input("👉 메뉴를 선택하세요: ")

    if choice == "1":
        show_inventory()
    elif choice == "2":
        add_item()
    elif choice == "3":
        delete_item()
    elif choice == "4":
        alert_expiry()
    elif choice == "5":
        edit_item()
    elif choice == "6":
        print("👋 프로그램을 종료합니다.")
        break
    else:
        print("❌ 유효하지 않은 입력입니다.")
