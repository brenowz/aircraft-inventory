import admin as adm


def main():

    print(
        "1. Administrator login\n"
        "2. Register administrator\n"
        "3. View aircraft catalog\n"
        "0. Exit"
    )

    option = int(input("Choose an option: "))

    if option == 1:
        adm.Admin().login()

    elif option == 2:
        adm.Admin().register()

    elif option == 3:
        adm.Aircraft().list_aircraft()

    elif option == 0:
        print("Program closed.")

    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()