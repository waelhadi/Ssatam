import sys
import time


def print_slow(text, delay=0.04):
  """دالة لكتابة النص ببطء لإعطاء مظهر جمالي"""
  for char in text:
    sys.stdout.write(char)
    sys.stdout.flush()
    time.sleep(delay)
  print()


def main():
  # طباعة الديكور (الشعار والمعلومات)
  print(
      "\033[1;31m    ██████  ██▀███  \n ██ ▀█   █ ▒████▄    ▒██    ▒ ▓██ ▒"
      " ██▒\n▓██  ▀█ ██▒▒██  ▀█▄  ░ ▓██▄   ▓██ ░▄█ ▒\n▓██▒  ▐▌██▒░██▄▄▄▄██  "
      " ▒   ██▒▒██▀▀█▄  \n▒██░   ▓██░ ▓█   ▓██▒▒██████▒▒░██▓ ▒██▒\n░ ▒░   ▒"
      " ▒  ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░░ ▒▓ ░▒▓░\033[0m"
  )
  print("\033[1;36m═══  QA4 - V100 ═══\033[0m")
  print("\033[1;32m[ Developer: NASR ]\033[0m  \033[1;33m[ Status: Connected ]\033[0m")
  print()

  # رسالة التحديث بخط الفيروزي وبشكل تدريجي جميل
  turquoise_color = "\033[1;36m"
  reset_color = "\033[0m"

  message = (
      f"{turquoise_color}يوجد تحديث جديد الرجاء سحب التحديثات من"
      f" السيرفر{reset_color}"
  )
  print_slow(message, delay=0.05)

  print()
  # طلب الضغط على الرقم 1
  choice = input(
      "\033[1;33mأضغط رقم 1 للأنتقال إلى المشغل: \033[0m"
  ).strip()

  if choice == "1":
    print("\033[1;32mجاري الانتقال إلى المشغل...\033[0m")
    # ضع هنا الأوامر أو الدوال التي تود تنفيذها بعد الانتقال للمشغل
  else:
    print("\033[1;31mالرقم المدخل غير صحيح، يرجى المحاولة لاحقاً.\033[0m")


if __name__ == "__main__":
  main()
