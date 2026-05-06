import os

from tkinter import *
win = Tk()
win.title("Bank")
win.geometry("434x250")
win.attributes("-topmost", True)

win.config(bg="#1e1e1e")

#WINDOW FUNCTIONS --------------------------------------------------------
def Exit(event):
    win.destroy()
win.bind("<Escape>", Exit)

def ClearMain():
    for widget in win.winfo_children():
        widget.destroy()


#FRONT-END FUNCTIONS ------------------------------------------


def UpdateCurDisplay(newDisplay):
    global currentDisplay

    Current.config(text=f"Current: {newDisplay}$")

def ErrorStable(error, position = 6):
    global Err

    Err = Label(win, text=f"Invalid: {error}", fg="Red")
    Err.grid(row=position, column=0, columnspan=10, sticky="ew")


def get_user_filepath(name):
    if not name:
        return None
    name = name.strip()
    if not name or name in (".", ".."):
        return None
    if any(c in name for c in ("/", "\\")):
        return None
    return os.path.join("USERS", f"{name}.py")


def load_user_account(name):
    path = get_user_filepath(name)
    if not path or not os.path.exists(path):
        raise FileNotFoundError

    account = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key == "amount":
                account["amount"] = int(value)
            elif key == "password":
                account["password"] = value.strip('"').strip("'")

    if "amount" not in account or "password" not in account:
        raise ValueError("Invalid account file")

    return account


def save_user_account(name, amount, password):
    os.makedirs("USERS", exist_ok=True)
    path = get_user_filepath(name)
    if not path:
        raise ValueError("Invalid username")

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"amount = {amount}\npassword = \"{password}\"")


#BACK-END FUNCTIONS --------------------------------------------

def GetIn():
    global Amount
    return Amount.get()

def Cret():
    global Name
    global Amount

    name = Name.get()
    amount = int(Amount.get())


    with open(f"USERS/{name}.py", "w") as cret:
        cret.write(f"amount = {amount}")


def Depo():
    global Err
    amount = GetIn()

    try:
        userAcc = load_user_account(Name)
        curAmount = userAcc["amount"]
        userPass = userAcc["password"]

        Err.destroy()

        if int(amount) < 0:
            ErrorStable("Negative numbers are not allowed as a request!")
            return

        curAmount += int(amount)
        save_user_account(Name, curAmount, userPass)

        UpdateCurDisplay(curAmount)

    except ValueError:
        ErrorStable("Needs to be valid number/amount!")
    except FileNotFoundError:
        ErrorStable("Account file not found.")


def Withdraw():
    global Err
    global Name
    amount = GetIn()

    try:
        userAcc = load_user_account(Name)
        curAmount = userAcc["amount"]
        userPass = userAcc["password"]

        Err.destroy()

        if int(amount) < 0:
            ErrorStable("Negative numbers are not allowed as a request!")
            return

        if (curAmount - int(amount)) >= 0:
            curAmount -= int(amount)
        
        save_user_account(Name, curAmount, userPass)

        UpdateCurDisplay(curAmount)

    except ValueError:
        ErrorStable("Needs to be valid number/amount!")
    except FileNotFoundError:
        ErrorStable("Account file not found.")


def LogCheck():
    global UserPassIn
    global UserNameIn
    global Err

    Err = Label(win)

    name = UserNameIn.get().strip()
    PassInCompare = UserPassIn.get()

    try:
        userAccount = load_user_account(name)
        getPass = userAccount["password"]
        Err.destroy()

        if PassInCompare == getPass:
            AccountCurrentAmmount = userAccount["amount"]
            ClearMain()
            Main(name, AccountCurrentAmmount)
        else:
            ErrorStable("Please Check Password.", 5)
    except FileNotFoundError:
        ErrorStable("Please Check Username.", 5)
    except Exception:
        ErrorStable("Could not load account.", 5)


def CreateAccount():
    global UserNameInReg
    global UserPassInReg
    global StartAmountIn
    global Err

    name = UserNameInReg.get().strip()
    password = UserPassInReg.get()
    try:
        amount = int(StartAmountIn.get())
    except ValueError:
        ErrorStable("Starting amount must be a number.", 5)
        return

    if not name:
        ErrorStable("Username cannot be empty.", 5)
        return
    if not password:
        ErrorStable("Password cannot be empty.", 5)
        return
    if amount < 0:
        ErrorStable("Starting amount cannot be negative.", 5)
        return

    if not get_user_filepath(name):
        ErrorStable("Invalid username. Do not use / or \\.", 5)
        return

    user_file = get_user_filepath(name)
    if os.path.exists(user_file):
        ErrorStable("Username already exists.", 5)
        return

    save_user_account(name, amount, password)

    ClearMain()
    Main(name, amount)


def Register():
    win.columnconfigure(1, weight=1)

    global UserNameInReg
    global UserPassInReg
    global StartAmountIn
    global Err

    Err = Label(win)

    RegHead = Label(win, text="Register New Account", padx=160, bg="#0D1A63", fg="white", font=("Times", 18, "italic"), pady=10)
    RegHead.grid(row=0, column=0, columnspan=2, sticky="ew")

    NameLabel = Label(win, text="Username:", bg="#1e1e1e", fg="white")
    NameLabel.grid(row=1, column=0, sticky="ew")
    UserNameInReg = Entry(win, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
    UserNameInReg.grid(row=1, column=1, sticky="ew")

    PassLabel = Label(win, text="Password:", bg="#1e1e1e", fg="white")
    PassLabel.grid(row=2, column=0, sticky="ew")
    UserPassInReg = Entry(win, show="*", highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
    UserPassInReg.grid(row=2, column=1, sticky="ew")

    AmountLabel = Label(win, text="Starting Amount:", bg="#1e1e1e", fg="white")
    AmountLabel.grid(row=3, column=0, sticky="ew")
    StartAmountIn = Entry(win, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
    StartAmountIn.grid(row=3, column=1, sticky="ew")

    RegisterBut = Button(win, text="Create Account", command=CreateAccount)
    RegisterBut.grid(row=4, column=0, columnspan=2, sticky="ew")

    BackBut = Button(win, text="Back", command=lambda: [ClearMain(), Log()])
    BackBut.grid(row=5, column=0, columnspan=2, sticky="ew")

    UserNameInReg.focus_set()


#PAGES ------------------------------------------------------------------------------------------------------

def Log():

    win.columnconfigure(1, weight=1)

    global UserNameIn
    global UserPassIn

    Err = Label(win)

    LogHead = Label(win, text="FranzExpress", padx=193, bg="#0D1A63", fg="white", font=("Times", 20, "italic"), pady=10)
    LogHead.grid(row=0, column=0, columnspan=2, sticky="ew", )

    NameLabel = Label(win, text="Username:", bg="#1e1e1e", fg="white")
    NameLabel.grid(row=2, column=0,sticky="ew")
    UserNameIn = Entry(win, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
    UserNameIn.grid(row=2, column=1, sticky="ew")

    PassLabel = Label(win, text="Password:", bg="#1e1e1e", fg="white")
    PassLabel.grid(row=3, column=0,sticky="ew")
    UserPassIn = Entry(win, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e", fg="white")
    UserPassIn.grid(row=3, column=1, sticky="ew")

    EnterBut = Button(win, text="Enter", command=LogCheck)   
    EnterBut.grid(row=4, column=0, columnspan=2, sticky="ew")

    RegisterBut = Button(win, text="Register", command=lambda: [ClearMain(), Register()])
    RegisterBut.grid(row=5, column=0, columnspan=2, sticky="ew")

    UserNameIn.focus_set()





def Main(user, amount):

    win.columnconfigure(1, weight=1)

    global currentDisplay
    global head
    global tex1
    global tex2
    global Amount
    global Dep
    global Wit
    global Current
    global Err
    global Name

    Name = user



    currentDisplay = amount

    head = Label(win, text=f"Welcome, {Name}!", padx=193, bg="#0D1A63", fg="white", font=("Times", 20, "italic"), pady=10)
    head.grid(row=0, column=0, columnspan=2, sticky="ew")

    tex2 = Label(win, text="Amount:", bg="#1e1e1e", fg="white")
    tex2.grid(row=1, column=0, sticky="ew")

    Amount = Entry(win, highlightthickness=2, highlightbackground="grey", bg="#1e1e1e")
    Amount.grid(row=1, column=1, sticky="ew")

    Dep = Button(win, text="Deposit", command=Depo)
    Dep.grid(row=2, column=0, sticky="ew", columnspan=2)

    Wit = Button(win, text="Withdraw", command=Withdraw)
    Wit.grid(row=3, column=0, sticky="ew", columnspan=2)

    Current = Label(win, text=f"Current: {currentDisplay}$", highlightthickness=1, highlightbackground="Green", padx=170)
    Current.grid(row=4, column=0, columnspan=2, sticky="ew")

    Err = Label(win)

    Amount.focus_set()






#SYSTEM STARTS ----------------------------------------------------------------------***********



Log()










            



win.mainloop()





