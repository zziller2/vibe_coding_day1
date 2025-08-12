import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def select_image():
    filepath = filedialog.askopenfilename(
        title="이미지 선택",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if not filepath:
        return

    try:
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img, lang="eng+kor")

        lines = text.splitlines()
        name = None
        qty = None
        expiry = None

        for line in lines:
            if "이름" in line:
                name = line.split(":")[-1].strip()
            elif "수량" in line:
                try:
                    qty = int(line.split(":")[-1].strip())
                except:
                    qty = None
            elif "유통기한" in line:
                expiry = line.split(":")[-1].strip()

        if name and qty and expiry:
            inventory.append({"이름": name, "수량": qty, "유통기한": expiry})
            save_inventory()
            refresh_listbox()
            messagebox.showinfo("추가 완료", f"OCR 인식 결과:\n{name} ({qty}개, {expiry})\n재고로 등록되었습니다.")
        else:
            messagebox.showwarning("정보 부족", "텍스트 인식은 되었지만 필요한 항목(이름/수량/유통기한)이 완전하지 않습니다.")

    except Exception as e:
        messagebox.showerror("에러", f"OCR 실패: {e}")

window = tk.Tk()
window.title("🧠 OCR 재고 인식 테스트")

btn = tk.Button(window, text="📸 이미지 불러오기", command=select_image, width=30)
btn.pack(pady=10)

output_text = tk.Text(window, height=20, width=70)
output_text.pack(padx=10, pady=10)

window.mainloop()
