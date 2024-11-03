import json, os
from tkinter import *
from tkinter import messagebox, simpledialog, ttk
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def aes_gcm_siv_encrypt(plaintext, associated_data=None):
    key = os.urandom(32)
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
    return key.hex(),nonce.hex(),ciphertext.hex()

def aes_gcm_siv_decrypt(key, nonce, ciphertext, associated_data=None):
    key = bytes.fromhex(key)
    nonce = bytes.fromhex(nonce)
    ciphertext = bytes.fromhex(ciphertext)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
    return plaintext.decode("utf-8")

root = Tk()
root.title("Spigt")
screenw = 340
screenh = 300
root.geometry(f"{screenw}x{screenh}")
root.resizable(False, False)

button_width_px = 160 
button_height_px = 180 

def check(directory, extension):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                return True
    return False

def check2(directory, file):
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f == file:
                return True, os.path.join(root, f)
    return False, None

def show_progress_window(root:Tk=Tk(), update_interval=100):
    def update_progress(value, opration):
        progress_var.set(value)
        text_var.set(opration)
        if value < 100:
            root.after(update_interval, update_progress, value + 1)
        else:
            text_var.set(find("operatingCompleted"))

    frame = Frame(root)
    frame.pack(padx=20, pady=20)

    progress_var = IntVar()
    progress = ttk.Progressbar(frame, variable=progress_var, maximum=100)
    progress.pack(fill=X, padx=10, pady=10)

    text_var = StringVar()
    text_label = Label(frame, textvariable=text_var)
    text_label.pack(pady=10)

    update_progress(0)

def start_progress():
    new_root = Toplevel()  # 使用Toplevel创建一个新的顶层窗口
    show_progress_window(new_root)

def find(key):
    textdict = {
        "lang":{
            "ch":"语言",
            "en":"Language",
            "ru":"Язык"
        },
        "install":{
            "ch":"安装",
            "en":"Install",
            "ru":"Установить"
        },
        "generate":{
            "ch":"生成",
            "en":"Generate",
            "ru":"Сгенерировать"
        },
        "input":{
            "ch":"输入目录(路径):",
            "en":"Enter the directory(path):",
            "ru":"Введите директорию (путь):"
        },
        "input2":{
            "ch":"输入补丁文件路径:",
            "en":"Enter the patch file path:",
            "ru":"Введите путь к файлу патча:"
        },
        "Ask":{
            "ch":"是否要安装补丁?",
            "en":"Do you want to install the patch?",
            "ru":"Хотите установить патч?"
        },
        "warning":{
            "ch":"安装补丁原有文件将被覆盖，补丁可能会危害你的计算机，是否继续？",
            "en":"Installing the patch will overwrite the existing files, the patch may harm your computer, do you want to continue?",
            "ru":"Установка патча перезапишет существующие файлы, патч может повредить ваш компьютер, вы хотите продолжить?"
        },
        "operatingCompleted":{
            "ch":"操作完成！",
            "en":"Operation completed!",
            "ru":"Операция завершена!"
        },
        "askNonce":{
            "ch":"请输入nonce:",
            "en":"Please enter the nonce:",
            "ru":"Пожалуйста, введите nonce:"
        },
        "askKey":{
            "ch":"请输入密钥:",
            "en":"Please enter the key:",
            "ru":"Пожалуйста, введите ключ:"
        }
    }
    return textdict[key].get(selected_language.get())

selected_language = StringVar(root)
selected_language.set("en")

language_menu = OptionMenu(root, selected_language, "ch", "en", "ru")
language_menu.pack()

def update_button_texts():
    Install.config(text=find("install"))
    Generate.config(text=find("generate"))

selected_language.trace("w", lambda *args: update_button_texts())

def install():
    direct = simpledialog.askstring("Input", find("input"))
    Pass=Check=Check2Pass=patchNotEmpty=patchPass=False
    if direct:
        exist = os.path.exists(direct)
        isdir = os.path.isdir(direct)
        if not exist:
            messagebox.showerror("Error", "Err: Directory does not exist.")
        elif not isdir:
            messagebox.showerror("Error", "Err: Path is not a directory.")
        elif exist and isdir:
            Pass = True
        else:
            messagebox.showerror("Error", "Err: Unknown error (0).")
    if Pass:
        if check(direct, ".spt"):
            Check = True
        else:
            messagebox.showerror("Error", "Err: Spigt is not supported by the software.")
    if Check:
        Check2 = check2(direct, "version.json")
        if Check2[0]:
            Check2Pass = True
        else:
            messagebox.showerror("Error", "Error: Directory does not contain a version.json file.")
    if Check2Pass:
        version = Check2[1]["ver"]
        patch = simpledialog.askstring("Input", find("input2"))
        if patch:
            patchNotEmpty = True
        else:
            messagebox.showerror("Error", "Err: patch file path is empty.")
    if patchNotEmpty:
        exist = os.path.exists(patch)
        isfile = os.path.isfile(patch)
        if not exist:
            messagebox.showerror("Error", "Err: Patch file does not exist.")
        elif not isfile:
            messagebox.showerror("Error", "Err: Path is not a file.")
        elif exist and isfile:
            if patch.endswith(".csp"):
                patchType = "csp"
                patchPass = True
            elif patch.endswith(".sp"):
                patchType = "sp"
                patchPass = True
            else:
                messagebox.showerror("Error", "Err: Patch file is not a valid Spigt patch file.")
        else:
            messagebox.showerror("Error", "Err: Unknown error (1).")
    if patchPass:
        with open(patch, "r") as f:
            if patchType == "csp":
                text = f.read()
                key = simpledialog.askstring("Input", find("askKey"))
                nonce = simpledialog.askstring("Input", find("askNonce"))
                patch_read = aes_gcm_siv_decrypt(key.encode(), nonce.encode(), text.encode())
            elif patchType == "sp":
                patch_read = json.load(f.read())
            else:
                messagebox.showerror("Error", "Err: Unknown error (2).")
        response = messagebox.askquestion("Ask", find("Ask"))
        if response == "yes":
            response = messagebox.askyesno("Warning", find("warning"))
            version_fit = version in patch_read
            if not version_fit:
                messagebox.showerror("Error", "Err: Patch version is not supported by the software.")
            elif version_fit and response:
                patch_read = patch_read[version]
                for file in patch_read:
                    original = json.load(open(os.path.join(direct, file), "r").read())
                    fileSlicing = []
                    for i in range(len(patch_read[file])):
                        opr= patch_read[file][i]
                        action = opr["action"]
                        location = opr["location"]
                        charactor = opr["charactor"]
                        #显示进度条
                        #修改原始文件
                        #切片
                        fileSlicing.append(original[:])
                        #标记
                    for i in range(len(patch_read[file])):
                        opr= patch_read[file][i]
                        action = opr["action"]
                        location = opr["location"]
                        charactor = opr["charactor"]
                        #替换
                        original
                    with open(os.path.join(direct, file), "w") as f:
                        f.write()
            else:
                messagebox.showerror("Error", "Err: Unknown error (2).")
def generate():
    #用户输入旧目录
    #检查新目录是否存在
    #用户输入新目录（>=1）
    #检查新目录是否存在
    #检查.spt、version.json是否存在
    #检查version.json版本号是否变化
    #检测是否有文件被删除，若有，将操作添加进更改数据
    #逐一获取文件，新旧版本比较，提取相同部分，根据相同部分定位不同部分，并根据曾经内容确定操作
    #""->"string" add "string"->"string" replace "string"->"" delete
    #询问用户需要的类型：一个旧版本一个文件，多个旧版本一个文件，csp文件或sp文件
    #csp: 随机生成nonce，获取aad，加密文件内容，写入。
    #sp: 将操作写入。
    pass

Install = Button(root, text=find("install"), command=install, width=button_width_px, height=button_height_px)
Generate = Button(root, text=find("generate"), command=generate, width=button_width_px, height=button_height_px)

x1 = (screenw / 4) - (button_width_px / 2)  
y1 = (screenh / 2) - (button_height_px / 2)

x2 = (screenw * 3 / 4) - (button_width_px / 2)  
y2 = (screenh / 2) - (button_height_px / 2)

Install.place(x=x1, y=y1, width=button_width_px, height=button_height_px)
Generate.place(x=x2, y=y2, width=button_width_px, height=button_height_px)

root.mainloop()
