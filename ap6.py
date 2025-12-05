q1  = sorted(['950111'])
q2  = sorted(['950112'])
q3  = sorted(['950113'])
q4  = sorted(['950121'])
q5  = sorted(['950122'])
q6  = sorted(['950123'])
q7  = sorted(['95013'])
q8  = sorted(['950141'])
q9  = sorted(['950142'])
q10 = sorted(['950151'])
q11 = sorted(['950152'])
q12 = sorted(['950153'])
q13 = sorted(['95016'])
q14 = sorted(['950171'])
q15 = sorted(['950172'])
q16 = sorted(['950173'])
q17 = sorted(['950174'])
q18 = sorted(['950175'])
q19 = sorted(['950176'])
q20 = sorted(['95018'])
q21 = sorted(['95019'])
q22 = sorted(['950201'])
q23 = sorted(['950202'])
q24 = sorted(['950211'])
q25 = sorted(['950212'])
q26 = sorted(['950213'])
q27 = sorted(['950221'])
q28 = sorted(['950222'])
q29 = sorted(['950223'])
q30 = sorted(['950231'])
q31 = sorted(['95024'])
q32 = sorted([
    '950111','950112','950113','950121','950122','950123','95013','950141','950142',
    '950151','950152','950153','95016','950171','950172','950173','950174','950175',
    '95018','95019','950201','950202','950211','950212','950213','950221','950222',
    '950223','950231','95024',
])
q33 = sorted([
    '90012','90013','90014','90015','90016','90017','9002','9007','90061','90063','90064',
    '90084','90085','90086','90087','90088','9005','90111','90115','90116','90191','9010',
    '90114','90034','90037','90032','90038','9004','9018','902112','9013',
    '950111','950112','950113','950121','950122','950123','95013','950141','950142',
    '950151','950152','950153','95016','950171','950172','950173','950174','950175',
    '95018','95019','950201','950202','950211','950212','950213','950221','950222',
    '950223','950231','95024',
    '90012','90013','90014','90015','90016','90017','9002','9007','90061','90063','90064',
    '90084','90085','90086','90087','90088','9005','90111','90115','90116','90191','9010',
    '90114','90034','90037','90032','90038','9004','9018','902112','9013',
])
q34 = sorted(['9002'])
q35 = sorted(['90071'])
q36 = sorted(['90072'])
q37 = sorted(['90073'])
q38 = sorted(['90074'])
q39 = sorted(['90061'])
q40 = sorted(['90063'])
q41 = sorted(['90064'])
q42 = sorted(['90084'])
q43 = sorted(['90085'])
q44 = sorted(['90086'])
q45 = sorted(['90087'])
q46 = sorted(['90088'])
q47 = sorted(['9005'])
q48 = sorted(['90111'])
q49 = sorted(['90115'])
q50 = sorted(['90116'])
q51 = sorted(['90191'])
q52 = sorted(['9010'])
q53 = sorted(['90034'])
q54 = sorted(['90037'])
q55 = sorted(['90032'])
q56 = sorted(['90038'])
q57 = sorted(['9004'])
q58 = sorted(['9018'])
q59 = sorted(['902112'])
q60 = sorted(['90114'])
q61 = sorted(['9013'])
q62 = sorted([
    '96010', '96011', '96013','96014','96020',
    '96021','96022',
])
q63 = sorted([
    '90012','90013','90014','90015','90016','90017','9002','9007','90061','90063','90064',
    '90084','90085','90086','90087','90088','9005','90111','90115','90116','90191','9010',
    '90114','90034','90037','90032','90038','9004','9018','902112','9013',
])

# ================= واجهة الاختيار ================= #
print_header()
if sisn:
    print(TEXT + f"Loaded {len(sisn)} sessions from 1.txt" + Style.RESET_ALL)
else:
    print(TEXT + "File 1.txt not found or empty" + Style.RESET_ALL)

print(TEXT + BAR + Style.RESET_ALL)

# قائمة رئيسية بين نوعي البلاغ
print()
print(TITLE + "اختر نوع قائمة البلاغ / Select report list type:" + Style.RESET_ALL)
print(COLOR_EU_TITLE    + " 1) البلاغ الأوروبي   (1 → 32)"  + Style.RESET_ALL)
print(COLOR_BASIC_TITLE + " 2) البلاغ الأساسي    (33 → 63)" + Style.RESET_ALL)
print()

main_choice = input(TEXT + "Enter report group number (1 or 2): " + Style.RESET_ALL).strip()

if main_choice == '1':
    print_eu_menu()
    choice = input(COLOR_EU_TITLE + "أدخل رقم البلاغ الأوروبي (1 → 32): " + Style.RESET_ALL).strip()
elif main_choice == '2':
    print_basic_menu()
    choice = input(COLOR_BASIC_TITLE + "أدخل رقم البلاغ الأساسي (33 → 63): " + Style.RESET_ALL).strip()
else:
    print(RED + "Invalid main choice, using random EU report as default." + RESET)
    choice = '32'  # عشوائي قانون أوروبي

sdsd = []

# ========== نفس منطق التعيين 1 → 63 ==========
if choice == '1':
    sdsd = q1
    print(TURQUOISE + "تم اختيار: المحتوى عبارة عن مادة اعتداء جنسي على الأطفال" + RESET)
elif choice == '2':
    sdsd = q2
    print(TURQUOISE + "تم اختيار: عرض توريد مواد الاعتداء الجنسي على الأطفال وبيعها وتوزيعها" + RESET)
elif choice == '3':
    sdsd = q3
    print(TURQUOISE + "تم اختيار: المحتوى المتعلق باستمالة طفل أو إغواءه جنسيًا" + RESET)
elif choice == '4':
    sdsd = q4
    print(TURQUOISE + "تم اختيار: التهديد بالعنف/التحريض على ارتكاب جريمة إرهابية" + RESET)
elif choice == '5':
    sdsd = q5
    print(TURQUOISE + "تم اختيار: المحتوى المتعلق بالتجنيد والتمويل ودعم الإرهاب" + RESET)
elif choice == '6':
    sdsd = q6
    print(TURQUOISE + "تم اختيار: تعليمات أو تدريب حول كيفية صنع المتفجرات/الأسلحة" + RESET)
elif choice == '7':
    sdsd = q7
    print(TURQUOISE + "تم اختيار: خطاب الكراهية غير القانوني" + RESET)
elif choice == '8':
    sdsd = q8
    print(TURQUOISE + "تم اختيار: تصوير العنف بشع المنظر" + RESET)
elif choice == '9':
    sdsd = q9
    print(TURQUOISE + "تم اختيار: المشاركة في منظمة إجرامية" + RESET)
elif choice == '10':
    sdsd = q10
    print(TURQUOISE + "تم اختيار: انتهاكات الخصوصية القائمة على الصور" + RESET)
elif choice == '11':
    sdsd = q11
    print(TURQUOISE + "تم اختيار: انتحال الهوية بشكل غير قانوني" + RESET)
elif choice == '12':
    sdsd = q12
    print(TURQUOISE + "تم اختيار: انتهاكات أخرى للخصوصية" + RESET)
elif choice == '13':
    sdsd = q13
    print(TURQUOISE + "تم اختيار: مشاركة الصور الحميمة أو الخاصة دون موافقة" + RESET)
elif choice == '14':
    sdsd = q14
    print(TURQUOISE + "تم اختيار: المحتوى المرتبط بالاتجار بالبشر" + RESET)
elif choice == '15':
    sdsd = q15
    print(TURQUOISE + "تم اختيار: الترويج للدعارة/الاستدراج" + RESET)
elif choice == '16':
    sdsd = q16
    print(TURQUOISE + "تم اختيار: إنتاج/بيع/توزيع المخدرات غير المشروعة" + RESET)
elif choice == '17':
    sdsd = q17
    print(TURQUOISE + "تم اختيار: الترويج للصيد الجائر أو الاتجار غير المشروع بالأحياء البرية" + RESET)
elif choice == '18':
    sdsd = q18
    print(TURQUOISE + "تم اختيار: الاتجار غير المشروع بالأسلحة" + RESET)
elif choice == '19':
    sdsd = q19
    print(TURQUOISE + "تم اختيار: سلع غير قانونية أخرى" + RESET)
elif choice == '20':
    sdsd = q20
    print(TURQUOISE + "تم اختيار: المضايقات أو التهديدات" + RESET)
elif choice == '21':
    sdsd = q21
    print(TURQUOISE + "تم اختيار: التشهير" + RESET)
elif choice == '22':
    sdsd = q22
    print(TURQUOISE + "تم اختيار: خرق قانون المستهلك" + RESET)
elif choice == '23':
    sdsd = q23
    print(TURQUOISE + "تم اختيار: المنتجات/البضائع غير الآمنة أو الخطرة" + RESET)
elif choice == '24':
    sdsd = q24
    print(TURQUOISE + "تم اختيار: التضليل الجنائي" + RESET)
elif choice == '25':
    sdsd = q25
    print(TURQUOISE + "تم اختيار: ازدراء المحكمة أو خرق أمر المحكمة" + RESET)
elif choice == '26':
    sdsd = q26
    print(TURQUOISE + "تم اختيار: التشجيع أو التعليمات على الانتحار" + RESET)
elif choice == '27':
    sdsd = q27
    print(TURQUOISE + "تم اختيار: الاحتيال" + RESET)
elif choice == '28':
    sdsd = q28
    print(TURQUOISE + "تم اختيار: غسيل الأموال" + RESET)
elif choice == '29':
    sdsd = q29
    print(TURQUOISE + "تم اختيار: الابتزاز/الرشوة" + RESET)
elif choice == '30':
    sdsd = q30
    print(TURQUOISE + "تم اختيار: الجرائم المتعلقة بالأمن القومي" + RESET)
elif choice == '31':
    sdsd = q31
    print(TURQUOISE + "تم اختيار: محتوى غير قانوني آخر" + RESET)
elif choice == '32':
    sdsd = q32
    print("\033[36m" + "تم اختيار: عشوائي قانون أوروبي" + RESET)
elif choice == '33':
    sdsd = q33
    print("\033[33;1m" + "تم اختيار: بلاغ النسر (NASR MIX)" + RESET)
elif choice == '34':
    sdsd = q34
    print(GREEN + "تم اختيار: الكراهية والسلوكيات البغيضة" + RESET)
elif choice == '35':
    sdsd = q35
    print(GREEN + "تم اختيار: لقد تعرضت بنفسي للتنمر أو المضايقة" + RESET)
elif choice == '36':
    sdsd = q36
    print(GREEN + "تم اختيار: تعرض شخص أعرفه للتنمر أو المضايقة" + RESET)
elif choice == '37':
    sdsd = q37
    print(GREEN + "تم اختيار: تعرض أحد المشاهير أو المسؤولين للتنمر أو المضايقة" + RESET)
elif choice == '38':
    sdsd = q38
    print(GREEN + "تم اختيار: تعرض آخرين للتنمر أو المضايقة" + RESET)
elif choice == '39':
    sdsd = q39
    print(GREEN + "تم اختيار: الانتحار وإيذاء النفس" + RESET)
elif choice == '40':
    sdsd = q40
    print(GREEN + "تم اختيار: اضطرابات الأكل وصورة الجسم غير الصحية" + RESET)
elif choice == '41':
    sdsd = q41
    print(GREEN + "تم اختيار: الأنشطة والتحديات الخطرة" + RESET)
elif choice == '42':
    sdsd = q42
    print(GREEN + "تم اختيار: النشاط الجنسي للشباب والاستدراج والاستغلال" + RESET)
elif choice == '43':
    sdsd = q43
    print(GREEN + "تم اختيار: السلوك الموحي جنسيًا بواسطة الشباب" + RESET)
elif choice == '44':
    sdsd = q44
    print(GREEN + "تم اختيار: النشاط الجنسي للبالغين والخدمات الجنسية" + RESET)
elif choice == '45':
    sdsd = q45
    print(GREEN + "تم اختيار: عُري البالغين" + RESET)
elif choice == '46':
    sdsd = q46
    print(GREEN + "تم اختيار: اللغة الجنسية الفاحشة" + RESET)
elif choice == '47':
    sdsd = q47
    print(GREEN + "تم اختيار: المحتوى الصادم وبشع المنظر" + RESET)
elif choice == '48':
    sdsd = q48
    print(GREEN + "تم اختيار: معلومات خاطئة عن الانتخابات" + RESET)
elif choice == '49':
    sdsd = q49
    print(GREEN + "تم اختيار: معلومات ضارة مضللة" + RESET)
elif choice == '50':
    sdsd = q50
    print(GREEN + "تم اختيار: التزييف العميق والوسائط التركيبية" + RESET)
elif choice == '51':
    sdsd = q51
    print(GREEN + "تم اختيار: التفاعل الزائف" + RESET)
elif choice == '52':
    sdsd = q52
    print(GREEN + "تم اختيار: مزعج" + RESET)
elif choice == '53':
    sdsd = q53
    print(GREEN + "تم اختيار: المقامرة" + RESET)
elif choice == '54':
    sdsd = q54
    print(GREEN + "تم اختيار: الكحول والتبغ والمخدرات" + RESET)
elif choice == '55':
    sdsd = q55
    print(GREEN + "تم اختيار: الأسلحة النارية والأسلحة الخطرة" + RESET)
elif choice == '56':
    sdsd = q56
    print(GREEN + "تم اختيار: تجارة سلع/خدمات خاضعة لتنظيم" + RESET)
elif choice == '57':
    sdsd = q57
    print(GREEN + "تم اختيار: الغش والاحتيال" + RESET)
elif choice == '58':
    sdsd = q58
    print(GREEN + "تم اختيار: مشاركة المعلومات الشخصية" + RESET)
elif choice == '59':
    sdsd = q59
    print(GREEN + "تم اختيار: انتهاك الملكية الفكرية" + RESET)
elif choice == '60':
    sdsd = q60
    print(GREEN + "تم اختيار: محتوى مرتبط بعلامة تجارية غير معلن عنه" + RESET)
elif choice == '61':
    sdsd = q61
    print(GREEN + "تم اختيار: آخر (عام)" + RESET)
elif choice == '62':
    sdsd = q62
    print("\033[92m" + "تم اختيار: بلاغ خاص في الأعلانات" + RESET)
elif choice == '63':
    unique_codes = sorted(set(q63))
    picked = random.choice(unique_codes)
    sdsd = [picked]
    print("\033[91m" + f"تم اختيار: عشوائي عربي | الكود المختار: {picked}" + RESET)
else:
    print(RED + "Invalid report number, using random EU report as default." + RESET)
    sdsd = q32

print(TEXT + BAR + Style.RESET_ALL)
print(TEXT + "Report code list (sdsd) is ready. Continue to your main sending module." + Style.RESET_ALL)
tr,fa,er=0,0,0
class ttsign:
    def __init__(self, params: str, data: str, cookies: str) -> None:
        self.params = params
        self.data = data
        self.cookies = cookies
    def hash(self, data: str) -> str:
        return str(hashlib.md5(data.encode()).hexdigest())
    def get_base_string(self) -> str:
        base_str = self.hash(self.params)
        base_str = (
            base_str + self.hash(self.data) if self.data else base_str + str("0" * 32)
        )
        base_str = (
            base_str + self.hash(self.cookies)
            if self.cookies
            else base_str + str("0" * 32)
        )
        return base_str
    def get_value(self) -> json:
        return self.encrypt(self.get_base_string())
    def encrypt(self, data: str) -> json:
        unix = time.time()
        len = 0x14
        key = [

            0xDF,
            0x77,
            0xB9,
            0x40,
            0xB9,
            0x9B,
            0x84,
            0x83,
            0xD1,
            0xB9,
            0xCB,
            0xD1,
            0xF7,
            0xC2,
            0xB9,
            0x85,
            0xC3,
            0xD0,
            0xFB,
            0xC3,
        ]
        param_list = []
        for i in range(0, 12, 4):
            temp = data[8 * i : 8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2 : (j + 1) * 2], 16)
                param_list.append(H)
        param_list.extend([0x0, 0x6, 0xB, 0x1C])
        H = int(hex(int(unix)), 16)
        param_list.append((H & 0xFF000000) >> 24)
        param_list.append((H & 0x00FF0000) >> 16)
        param_list.append((H & 0x0000FF00) >> 8)
        param_list.append((H & 0x000000FF) >> 0)
        eor_result_list = []
        for A, B in zip(param_list, key):
            eor_result_list.append(A ^ B)
        for i in range(len):
            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % len]
            E = C ^ D
            F = self.rbit_algorithm(E)
            H = ((F ^ 0xFFFFFFFF) ^ len) & 0xFF
            eor_result_list[i] = H
        result = ""
        for param in eor_result_list:
            result += self.hex_string(param)
        return {
            "x-ss-req-ticket": str(int(unix * 1000)),
            "x-khronos": str(int(unix)),
            "x-gorgon": ("0404b0d30000" + result),
        }

    def rbit_algorithm(self, num):
        result = ""
        tmp_string = bin(num)[2:]
        while len(tmp_string) < 8:
            tmp_string = "0" + tmp_string
        for i in range(0, 8):
            result = result + tmp_string[7 - i]
        return int(result, 2)

    def hex_string(self, num):
        tmp_string = hex(num)[2:]
        if len(tmp_string) < 2:
            tmp_string = "0" + tmp_string
        return tmp_string

    def reverse(self, num):
        tmp_string = self.hex_string(num)
        return int(tmp_string[1:] + tmp_string[:1], 16)
P = '\x1b[1;97m'
B = '\x1b[1;94m'
O = '\x1b[1;96m'
Z = "\033[1;30m"
X = '\033[1;33m' 
F = '\033[2;32m'
Z = '\033[1;31m' 
L = "\033[1;95m"  
C = '\033[2;35m' 
A = '\033[2;39m' 
P = "\x1b[38;5;231m" 
J = "\x1b[38;5;208m" 
J1='\x1b[38;5;202m'
J2='\x1b[38;5;203m' 
J21='\x1b[38;5;204m'
J22='\x1b[38;5;209m'
F1='\x1b[38;5;76m'
C1='\x1b[38;5;120m'
P1='\x1b[38;5;150m'
P2='\x1b[38;5;190m'
def clear():
            import os
from termcolor import colored
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
print(colored("[3]  أبدء البلاغ", "cyan"))
Get_aobsh = "3"
print(colored(f"تم اختيار رقم {Get_aobsh} تلقائياً ✅", "green"))
clear()
if Get_aobsh in '3':
 import requests
import os
import threading
import time
import json
import sys
import re
import datetime