import tkinter as tk
from tkinter import messagebox
import MySQLdb


#Class: Login Page
#Task: Login to the system
class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Yammy Pizza Login")

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.grid(row=2, column=1)

        self.db_connect()

    def db_connect(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="softdevdb")
        self.cursor = self.conn.cursor()

    #Function: Login
    #Task: Login
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = self.cursor.fetchone()

        if result:
            self.master.withdraw()
            main_app = tk.Toplevel(self.master)
            app = YammyPizzaApp(main_app) # Connecting to the next page
            main_app.protocol("Login Close", app.close_app)
            main_app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid login credentials")


#PIZZA CLASS
class YammyPizzaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Yammy Pizza Information")

        self.insert_button = tk.Button(self.master, text="Add New Pizza", command=self.add_new_pizza)
        self.insert_button.grid(row=0, column=0)

        self.search_label = tk.Label(self.master, text="Pizza Type")
        self.search_label.grid(row=0, column=1)
        self.search_entry = tk.Entry(self.master)
        self.search_entry.grid(row=0, column=2)
        self.search_button = tk.Button(self.master, text="Search Pizza", command=self.search_pizza)
        self.search_button.grid(row=0, column=3)

        self.pizza_label = tk.Label(self.master, text="Pizza Name:")
        self.pizza_label.grid(row=1, column=0)
        self.pizza_entry = tk.Entry(self.master)
        self.pizza_entry.grid(row=1, column=1)

        self.pizza_topping_label = tk.Label(self.master, text="Pizza Topping:")
        self.pizza_topping_label.grid(row=2, column=0)
        self.pizza_topping_entry = tk.Entry(self.master)
        self.pizza_topping_entry.grid(row=2, column=1)

        self.pizza_size_label = tk.Label(self.master, text="Size:")
        self.pizza_size_label.grid(row=3, column=0)
        self.pizza_size_entry = tk.Entry(self.master)
        self.pizza_size_entry.grid(row=3, column=1)

        self.pizza_sauce_label = tk.Label(self.master, text="Sauce:")
        self.pizza_sauce_label.grid(row=4, column=0)
        self.pizza_sauce_entry = tk.Entry(self.master)
        self.pizza_sauce_entry.grid(row=4, column=1)
        
        self.pizza_price_label = tk.Label(self.master, text="Price:")
        self.pizza_price_label.grid(row=5, column=0)
        self.pizza_price_entry = tk.Entry(self.master)
        self.pizza_price_entry.grid(row=5, column=1)

        self.pizza_side_label = tk.Label(self.master, text="Pizza Side:")
        self.pizza_side_label.grid(row=6, column=0)
        self.pizza_side_entry = tk.Entry(self.master)
        self.pizza_side_entry.grid(row=6, column=1)

        self.update_button = tk.Button(self.master, text="Update Pizza", command=self.update_pizza)
        self.update_button.grid(row=7, column=1)

        self.fetch_button = tk.Button(self.master, text="Show Detail", command=self.show_detailed_pizza_info)
        self.fetch_button.grid(row=7, column=2)

        self.delete_button = tk.Button(self.master, text="Delete", command=self.delete_pizza)
        self.delete_button.grid(row=7, column=3)

        self.db_connect()

    def db_connect(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="softdevdb")
        self.cursor = self.conn.cursor()


    #Fucntion: add_new_pizza
    #Task: Adding a new pizza
    def add_new_pizza(self):
        pizzaname   = self.pizza_entry.get()
        topping     = self.pizza_topping_entry.get()
        size        = self.pizza_size_entry.get()
        sauce       = self.pizza_sauce_entry.get()
        price       = self.pizza_price_entry.get()
        side        = self.pizza_side_entry.get()

        try:
            self.cursor.execute("INSERT INTO pizza (pizzaname , pizzatopping , pizzasize, pizzasauce, pizzaprice, pizzasides) VALUES (%s, %s, %s, %s, %s, %s)", (pizzaname, topping, size, sauce, price, side))
            self.conn.commit()

            messagebox.showinfo("Success", "Pizza inserted successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    #Fucntion: search_pizza
    #Task: Searching a pizza
    def search_pizza(self):
        pizzaname = self.search_entry.get()
        
        try:
            self.cursor.execute("SELECT * FROM pizza WHERE pizzaname=%s", (pizzaname,))
            result = self.cursor.fetchone()
            
            
            if result:
                self.pizza_entry.delete(0, tk.END)
                self.pizza_entry.insert(tk.END, result[1])
                self.pizza_topping_entry.delete(0, tk.END)
                self.pizza_topping_entry.insert(tk.END, result[2])
                self.pizza_size_entry.delete(0, tk.END)
                self.pizza_size_entry.insert(tk.END, result[3])
                self.pizza_sauce_entry.delete(0, tk.END)
                self.pizza_sauce_entry.insert(tk.END, result[4])
                self.pizza_price_entry.delete(0, tk.END)
                self.pizza_price_entry.insert(tk.END, result[5])
                self.pizza_side_entry.delete(0, tk.END)
                self.pizza_side_entry.insert(tk.END, result[6])
            else:
                messagebox.showerror("Error", "No record found for search: " + pizzaname)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))


    #Fucntion: update_pizza
    #Task: Updating a pizza
    def update_pizza(self):
        pizzaname   = self.pizza_entry.get()
        topping     = self.pizza_topping_entry.get()
        size        = self.pizza_size_entry.get()
        sauce       = self.pizza_sauce_entry.get()
        price       = self.pizza_price_entry.get()
        side        = self.pizza_side_entry.get()
        
        try:
            self.cursor.execute("UPDATE pizza SET pizzaname=%s, pizzatopping=%s, pizzasize=%s, pizzasauce=%s, pizzaprice=%s, pizzasides=%s WHERE pizzaname=%s",
            (pizzaname, topping, size, sauce, price, side, pizzaname))
            self.conn.commit()

            messagebox.showinfo("Success", "Pizza updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    #Fucntion: show_detailed_pizza_info
    #Task: Showing detail of a pizza
    def show_detailed_pizza_info(self):
        pizzaname = self.pizza_entry.get()
        try:
            self.cursor.execute("SELECT * FROM pizza WHERE pizzaname=%s", (pizzaname,))
            result = self.cursor.fetchone()

            if result:
                display_window = tk.Toplevel(self.master)
                display_window.title(f"{result[1]} Detail")

                pizza_label = tk.Label(display_window,
                text=f"Pizza Information: {result[1]}, {result[2]}, {result[3]}, {result[4]}, {result[5]}, {result[6]}")
                pizza_label.pack()

                close_button = tk.Button(display_window, text="Close", command=display_window.destroy)
                close_button.pack()
            else:
                messagebox.showerror("Error", "No record found for pizza: " + pizzaname)

        except Exception as e:
            messagebox.showerror("Error", str(e))


    #Fucntion: delete_pizza
    #Task: Deleting a pizza
    def delete_pizza(self):
        pizzaname = self.pizza_entry.get()

        try:
            self.cursor.execute("DELETE FROM pizza WHERE pizzaname=%s", (pizzaname,))
            self.conn.commit()

            # Clear the fields after deletion
            self.pizza_entry.delete(0, tk.END)
            self.pizza_topping_entry.delete(0, tk.END)
            self.pizza_size_entry.delete(0, tk.END)
            self.pizza_sauce_entry.delete(0, tk.END)
            self.pizza_price_entry.delete(0, tk.END)
            self.pizza_side_entry.delete(0, tk.END)

            messagebox.showinfo("Success", "Pizza deleted successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def close_app(self):
        self.conn.close()
        self.master.quit()

#Main Class
#Task: To start the program
if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginPage(login_root)
    login_root.mainloop() 
    