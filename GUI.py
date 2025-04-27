import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from SQL_CON import SQL

class GameAdderGUI:
    def __init__(self,root):
        self.sql = SQL()
        self.root= root
        self.root.title("Add New Game")


        
        self.genres = self.sql.list_genres()
        self.consoles = self.sql.list_consoles()
        self.company = self.sql.list_company()
        self.region = self.sql.list_region()

        self.width = 40
        
        self.build_gui()

    def build_gui(self):
        #Game Title
        ttk.Label(self.root, text="Game Title",).grid(row=0,column=0)
        self.title_entry = ttk.Entry(self.root, width=self.width + 3,)
        self.title_entry.grid(row=0,column=1, sticky="W",pady= 4,)

        #genre dropdown
        ttk.Label(self.root,text="Genre").grid(row=1,column=0)
        self.genre_var = tk.StringVar()
        self.genre_dropdown = ttk.Combobox(self.root, textvariable=self.genre_var, values=[genre[1] for genre in self.genres],width=self.width,state="readonly"  )
        self.genre_dropdown.grid(row=1,column=1,sticky="W",pady= 2)

        #console drop down
        ttk.Label(self.root,text="Console").grid(row=2,column=0)
        self.console_var = tk.StringVar()
        self.console_dropdown = ttk.Combobox(self.root,textvariable= self.console_var, values=[console[1] for console in self.consoles],width=self.width,state="readonly"   )
        self.console_dropdown.grid(row=2,column=1,sticky="W",pady= 2)

        #company
        ttk.Label(self.root,text="Company").grid(row=3,column=0)
        self.company_var = tk.StringVar()
        self.company_dropdown = ttk.Combobox(self.root,textvariable=self.company_var,values=[comp[1] for comp in self.company],width=self.width,state="readonly"   )
        self.company_dropdown.grid(row=3,column=1,sticky="W",pady= 2)
        
        #region dropdown
        ttk.Label(self.root,text='Region').grid(row=4, column=0,pady= 2)
        self.region_var = tk.StringVar()
        self.region_dropdown = ttk.Combobox(self.root, textvariable= self.region_var, values=[reg[1] for reg in self.region],width=self.width,state="readonly"  )
        self.region_dropdown.grid(row=4,column=1,sticky="W",pady= 2)

        #Year Entry
        ttk.Label(self.root,text="Year").grid(row=5,column=0)
        self.year_entry = ttk.Entry(self.root, width=self.width+3)
        self.year_entry.grid(row=5,column=1,sticky="W",pady= 2)

        #Played checkbox
        # Label first
        self.played_label = ttk.Label(self.root, text="Played")
        self.played_label.grid(row=6, column=0)

        # Then checkbox after
        self.played_var = tk.BooleanVar()
        self.played_check = ttk.Checkbutton(self.root, variable=self.played_var)
        self.played_check.grid(row=6, column=1, sticky="w")

        #submit button
        self.submit_btn = tk.Button(self.root,text="Submit",relief="solid",borderwidth=2,command=self.on_submit_btn)
        self.submit_btn.grid(row=7,column=0,pady=4)

        #treeview
        self.tree = ttk.Treeview(self.root, columns=("ID","Title","Played","Genre","Console","Completed","Publisher","Company","Year","Region"), show="headings")
        self.tree.grid(row=8, column=0,columnspan=2, sticky="nsew",pady=10)

        #define tree headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Played", text="Played")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Console", text="Console")
        self.tree.heading("Completed", text="Completed")
        self.tree.heading("Publisher",text="Publisher")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Region", text="Region")
        
        

        #adjust column width
        for col in ("ID","Title","Played", "Genre", "Console","Completed", "Publisher","Company","Year","Region"):
            self.tree.column(col, width=100, anchor="center")

        #scrollbar for tree view
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=8,column=2,sticky="ns")

        # stretch the tree view when resizing
        self.root.grid_rowconfigure(8, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.refresh_game_tree()


    def refresh_game_tree(self):
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch fresh data from SQL
        games = self.sql.list_games()

        # Insert data into the tree
        for game in games:
            self.tree.insert("", "end", values=game)

    def on_submit_btn(self):


        self.submited_title = self.title_entry.get().strip()
        
        selected_genre_name = self.genre_var.get()
        self.submited_genre = next((genre[0] for genre in self.genres if genre[1] == selected_genre_name), None)

        selected_console_name = self.console_var.get()
        self.submited_console = next((console[0] for console in self.consoles if console[1]== selected_console_name), None)
        
        selected_company_name = self.company_var.get()
        self.submited_company = next((comp[0] for comp in self.company if comp[1]== selected_company_name), None)
        
        selected_region_name = self.region_var.get()
        self.submited_region = next((reg[0] for reg in self.region if reg[1] == selected_region_name),None)
        self.submited_year = self.year_entry.get()
        self.submited_played = self.played_var.get()

        if not self.submited_title or not selected_genre_name or not selected_console_name \
        or not selected_company_name or not selected_region_name or not (self.submited_year.isdigit() and len(self.submited_year) == 4):
            messagebox.showerror( "Error", "You are missing a field")
            return
        self.insert_game()

    def insert_game(self):
         #valid year
            year_value = int(self.submited_year)
            print("Valid Year:", year_value)

            print(f'Title:{self.submited_title}, Genre:{self.submited_genre}'
              f'Console:{self.submited_console}, Company:{self.submited_company}'
              f'Region:{self.submited_region}, Year:{year_value}, Played?: {self.submited_played}')
        
            self.submitted_values =[
            self.submited_title,self.submited_genre,self.submited_console,
            self.submited_company,self.submited_region,year_value,self.submited_played
             ]
            
            self.sql.insert_game(self.submited_title, self.submited_genre, self.submited_console,
                                 self.submited_company,self.submited_region, year_value, self.submited_played)
            messagebox.showinfo("Game Added","The game was added successfully")
            self.sql.list_games()
            self.refresh_game_tree()
            self.clear_fields()

            
    def clear_fields(self):
        #clear the form fields
            self.title_entry.delete(0,tk.END)
            self.genre_var.set('')
            self.console_var.set('')
            self.company_var.set('')
            self.region_var.set('')
            self.year_entry.delete(0,tk.END)
            self.played_var.set(False)





if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x300")
    app = GameAdderGUI(root)
    root.mainloop()