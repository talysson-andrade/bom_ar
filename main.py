def main():
    temp = get_temperature()
    if temp > 20:
        start_ar()

def get_temperature():
    return 22.5

def start_ar():
    print("Ar condicionado foi ligado")


if __name__ == "__main__":
    main()
