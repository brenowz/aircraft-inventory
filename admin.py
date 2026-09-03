import pymysql.cursors


class Admin:

    def __init__(self):
        pass

    def connect(self):

        try:
            self.database = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                db="aircraft_inventory",
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )

            print("Connected to database.")

        except:
            print("Error connecting to database.")

    def login(self):

        self.connect()

        email = input("Email: ")
        password = input("Password: ")

        authenticated = False

        try:
            with self.database.cursor() as cursor:
                cursor.execute("SELECT * FROM admins")
                results = cursor.fetchall()

        except:
            print("Error querying administrators.")
            return

        for administrator in results:

            if (
                email == administrator["email"]
                and password == administrator["password"]
            ):
                authenticated = True
                break

        if authenticated:
            self.admin_menu()

        else:
            print("Incorrect credentials. Try again.")
            self.login()

    def check_email(self, email):

        self.connect()

        try:
            with self.database.cursor() as cursor:
                cursor.execute("SELECT * FROM admins")
                results = cursor.fetchall()

        except:
            print("Error querying administrators.")
            return 0

        for administrator in results:

            if email == administrator["email"]:
                return 1

        return 0

    def register(self):

        verification_code = 123

        code = int(
            input("Enter the verification code: ")
        )

        if code == verification_code:

            name = input("Name: ")
            email = input("Email: ")
            password = input("Password: ")

            data = [
                name,
                email,
                password,
                1
            ]

            self.connect()

            email_exists = self.check_email(email)

            if email_exists == 1:

                print(
                    "Email already registered. "
                    "Try logging in."
                )

                self.login()

            else:

                with self.database.cursor() as cursor:

                    sql = """
                    INSERT INTO admins
                    (name, email, password, status)
                    VALUES (%s, %s, %s, %s)
                    """

                    cursor.execute(sql, data)
                    self.database.commit()

                    print("Administrator registered.")

                    self.login()

        else:
            print("Invalid verification code.")

    def admin_menu(self):

        print(
            "\n1. Register new aircraft"
            "\n2. Update aircraft"
            "\n3. Delete aircraft"
            "\n4. List aircraft"
            "\n0. Exit"
        )

        option = int(input("Choose an option: "))

        if option == 0:
            return

        elif option == 1:

            model = input("Model: ")
            year = int(input("Year: "))
            color = input("Color: ")

            aircraft_type = int(
                input(
                    "Type "
                    "(1. Airplane | "
                    "2. Helicopter | "
                    "3. Drone): "
                )
            )

            aircraft_data = [
                model,
                year,
                color,
                aircraft_type
            ]

            Aircraft(
                aircraft_data
            ).register_aircraft()

        elif option == 2:
            Aircraft().update_aircraft()

        elif option == 3:
            Aircraft().delete_aircraft()

        elif option == 4:
            Aircraft().list_aircraft()
            self.admin_menu()

        else:
            print("Invalid option.")
            self.admin_menu()


class Aircraft(Admin):

    def __init__(self, aircraft_data=None):
        self.aircraft_data = aircraft_data

    def register_aircraft(self):

        self.connect()

        try:
            with self.database.cursor() as cursor:

                sql = """
                INSERT INTO aircraft
                (model, year, color, type)
                VALUES (%s, %s, %s, %s)
                """

                cursor.execute(
                    sql,
                    self.aircraft_data
                )

                self.database.commit()

                print("Aircraft registered.")

        except:
            print("Error registering aircraft.")

        self.admin_menu()

    def list_aircraft(self):

        self.connect()

        try:
            with self.database.cursor() as cursor:

                cursor.execute(
                    "SELECT * FROM aircraft"
                )

                results = cursor.fetchall()

            if len(results) == 0:

                print("No aircraft registered.")

            else:

                print("\n--- AIRCRAFT ---")

                for aircraft in results:

                    print(
                        f"\nID: {aircraft['id']}"
                    )

                    print(
                        f"Model: {aircraft['model']}"
                    )

                    print(
                        f"Year: {aircraft['year']}"
                    )

                    print(
                        f"Color: {aircraft['color']}"
                    )

                    print(
                        f"Type: {aircraft['type']}"
                    )

        except:
            print("Error listing aircraft.")

    def delete_aircraft(self):

        self.list_aircraft()

        aircraft_id = int(
            input(
                "\nEnter the ID of the aircraft "
                "you want to delete: "
            )
        )

        self.connect()

        try:
            with self.database.cursor() as cursor:

                sql = """
                DELETE FROM aircraft
                WHERE id = %s
                """

                cursor.execute(
                    sql,
                    (aircraft_id,)
                )

                self.database.commit()

                if cursor.rowcount > 0:
                    print("Aircraft deleted.")

                else:
                    print("Aircraft not found.")

        except:
            print("Error deleting aircraft.")

        self.admin_menu()

    def update_aircraft(self):

        self.list_aircraft()

        aircraft_id = int(
            input(
                "\nEnter the ID of the aircraft "
                "you want to update: "
            )
        )

        model = input("New model: ")
        year = int(input("New year: "))
        color = input("New color: ")

        aircraft_type = int(
            input(
                "New type "
                "(1. Airplane | "
                "2. Helicopter | "
                "3. Drone): "
            )
        )

        self.connect()

        try:
            with self.database.cursor() as cursor:

                sql = """
                UPDATE aircraft
                SET model = %s,
                    year = %s,
                    color = %s,
                    type = %s
                WHERE id = %s
                """

                data = [
                    model,
                    year,
                    color,
                    aircraft_type,
                    aircraft_id
                ]

                cursor.execute(sql, data)

                self.database.commit()

                if cursor.rowcount > 0:
                    print("Aircraft updated.")

                else:
                    print(
                        "Aircraft not found or "
                        "no data was changed."
                    )

        except:
            print("Error updating aircraft.")

        self.admin_menu()