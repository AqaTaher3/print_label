import os
import win32print
import win32api
from PyPDF2 import PdfReader
import os
import time


def print_pdf_page_by_page(file_path, printer_name):
    try:
        # بررسی اینکه فایل یک PDF است
        if not file_path.lower().endswith('.pdf'):
            print(f"{file_path} یک فایل PDF نیست.")
            return

        # خواندن فایل PDF
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)

        # تنظیم چاپگر پیش‌فرض
        win32print.SetDefaultPrinter(printer_name)

        # چاپ صفحه به صفحه با تأخیر ۲ ثانیه
        for page_number in range(num_pages):
            # مسیر فایل موقت برای ذخیره هر صفحه
            temp_file_path = f"temp_page_{page_number + 1}.pdf"

            # ذخیره صفحه به صورت یک فایل PDF مجزا
            with open(temp_file_path, "wb") as temp_file:
                writer = PdfReader()
                writer.add_page(reader.pages[page_number])
                writer.write(temp_file)

            print(f"چاپ صفحه {page_number + 1} از {file_path} به چاپگر: {printer_name}")

            # ارسال فایل صفحه به چاپگر
            win32print.StartDocPrinter(printer_name, 1, ("Print Job", None, "RAW"))
            win32print.WritePrinter(printer_name, temp_file_path)
            win32print.EndDocPrinter(printer_name)

            # تاخیر 2 ثانیه
            time.sleep(2)

            # حذف فایل موقت
            os.remove(temp_file_path)

    except Exception as e:
        print(f"خطا در چاپ فایل {file_path}: {e}")

def print_files_in_directory(directory_path, printer_name):
    if not os.path.isdir(directory_path):
        print(f"'{directory_path}' یک پوشه معتبر نیست.")
        return

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            print_pdf_page_by_page(file_path, printer_name)

# نمایش لیست چاپگرها و دریافت نام چاپگر مورد نظر
def list_printers():
    printers = [printer[2] for printer in win32print.EnumPrinters(2)]
    print("لیست چاپگرهای موجود:")
    for i, printer in enumerate(printers):
        print(f"{i + 1}: {printer}")
    return printers

printers = list_printers()
printer_choice = int(input("شماره چاپگر مورد نظر را وارد کنید: ")) - 1
selected_printer = printers[printer_choice]

# دریافت مسیر پوشه و چاپ فایل‌ها
directory_path = input("آدرس پوشه را وارد کنید: ")
print_files_in_directory(directory_path, selected_printer)
