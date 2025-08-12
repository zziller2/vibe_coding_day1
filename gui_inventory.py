import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
from datetime import datetime

FILE_NAME = "inventory.json"

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        inventory = json.load(f)
else:
    inventory = []

def save_inventory():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2)

def refresh_listbox():
    listbox.delete(0, tk.END)
    today = datetime.today()

    for i, item in enumerate(inventory):
        expiry = datetime.strptime(item["유통기한"], "%Y-%m-%d")
        days_left = (expiry - today).days
        qty = item["수량"]

        display = f"{item['이름']} - {qty}개 ({item['유통기한']})"

        if days_left < 0:
            display = f"❌ {display}"
            listbox.insert(tk.END, display)
            listbox.itemconfig(i, foreground="red")

        elif days_left <= 60:
            display = f"⚠️ {display}"
            listbox.insert(tk.END, display)
            listbox.itemconfig(i, foreground="red")

        elif qty <= 2:
            display = f"⚠️ {display}"
            listbox.insert(tk.END, display)
            listbox.itemconfig(i, foreground="orange")

        else:
            listbox.insert(tk.END, display)

def show_inventory():
    result_text.delete("1.0", tk.END)
    if not inventory:
        result_text.insert(tk.END, "📭 재고가 없습니다.\n")
        return
    for i, item in enumerate(inventory, 1):
        result_text.insert(tk.END, f"{i}. {item['이름']} - 수량: {item['수량']}개, 유통기한: {item['유통기한']}\n")

def add_item():
    name = simpledialog.askstring("재료 이름", "재료 이름을 입력하세요:")
    if not name:
        return
    try:
        qty = int(simpledialog.askstring("수량", "수량을 입력하세요:"))
        expiry = simpledialog.askstring("유통기한", "YYYY-MM-DD 형식으로 입력:")
        datetime.strptime(expiry, "%Y-%m-%d")  
    except:
        messagebox.showerror("입력 오류", "입력값이 올바르지 않습니다.")
        return

    inventory.append({"이름": name, "수량": qty, "유통기한": expiry})
    save_inventory()
    messagebox.showinfo("추가 완료", f"{name} 재료가 추가되었습니다.")
    show_inventory()

def delete_item():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("선택 없음", "삭제할 항목을 선택하세요.")
        return
    index = selected[0]
    name = inventory[index]["이름"]
    del inventory[index]
    save_inventory()
    refresh_listbox()
    messagebox.showinfo("삭제 완료", f"'{name}' 항목이 삭제되었습니다.")

def edit_item():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("선택 없음", "수정할 항목을 선택하세요.")
        return
    index = selected[0]
    item = inventory[index]

    new_qty = simpledialog.askstring("수정 - 수량", f"현재 수량: {item['수량']} → 새 수량:")
    new_expiry = simpledialog.askstring("수정 - 유통기한", f"현재 유통기한: {item['유통기한']} → 새 날짜 (YYYY-MM-DD):")


    if new_qty:
        try:
            item["수량"] = int(new_qty)
        except ValueError:
            messagebox.showerror("입력 오류", "수량은 숫자여야 합니다.")
    if new_expiry:
        try:
            datetime.strptime(new_expiry, "%Y-%m-%d")
            item["유통기한"] = new_expiry
        except:
            messagebox.showerror("입력 오류", "날짜 형식이 잘못되었습니다.")

    save_inventory()
    refresh_listbox()
    messagebox.showinfo("수정 완료", f"'{item['이름']}' 항목이 수정되었습니다.")

window = tk.Tk()
window.title("치과 재고관리 프로그램 (GUI v2)")

frame = tk.Frame(window)
frame.pack(pady=10)

btn_add = tk.Button(frame, text="➕ 재고 추가", command=add_item, width=20)
btn_edit = tk.Button(frame, text="✏️ 재고 수정", command=edit_item, width=20)
btn_delete = tk.Button(frame, text="🗑️ 재고 삭제", command=delete_item, width=20)

btn_add.grid(row=0, column=0, padx=5, pady=5)
btn_edit.grid(row=0, column=1, padx=5, pady=5)
btn_delete.grid(row=0, column=2, padx=5, pady=5)

listbox = tk.Listbox(window, width=60, height=15)
listbox.pack(padx=10, pady=10)

refresh_listbox()
window.mainloop()

