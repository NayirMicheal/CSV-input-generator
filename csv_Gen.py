
# Created by Nayir Labib at 12/09/2024

# Feature: CSV Generator for INPUT2OUTPUT mapping

# Steps:
# Enter the number of inputs and the number of outputs
# Enter the title and the name of each input and the number of variants it has
# Enter the title and the name of each output
# Enter the variant names for Each input
# Generate the CSV file

from tkinter import *
from tkinter import messagebox
import csv

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 900
LABEL_FONT = ("Helvetica", 8)
BUTTON_FONT = ("Helvetica", 10)
GEN_CSV_FONT = ("Helvetica", 16)
ENTRY_WIDTH = 150
ENTRY_HEIGHT_OFFSET = 25

# Widget Positions
LABEL_X = 20
SPINBOX_X = 100
BUTTON_NEXT_X = 150
BUTTON_FILL_X = 350
BUTTON_FILL_Y = 60
GEN_BTN_X = 325
GEN_BTN_Y = 350
INPUT_Y_OFFSET = 50

# Label Texts
LABEL_INPUT_TEXT = "Enter Number of inputs"
LABEL_OUTPUT_TEXT = "Enter Number of outputs"
LABEL_TITLE_TEXT = "Set the title of the column and the name of the instance"
LABEL_COLUMN_TITLE = "Title of the column:"
LABEL_INSTANCE_NAME = "Name of the instance:"
LABEL_NUM_INPUTS = "Num of the variants:"

class InputArea:
    def __init__(self, window):
        """Handles creation and management of input fields dynamically."""
        self.window = window
        self.entries_created = []

    def fill_input_area(self, num_of_input):
        """Fills the input area with Entry widgets based on the number of inputs required."""
        self.entries_created.clear()
        offset = 0
        for _ in range(num_of_input):
            entry = Entry(self.window)
            entry.place(x=ENTRY_WIDTH, y=INPUT_Y_OFFSET + offset)
            self.entries_created.append(entry)
            offset += ENTRY_HEIGHT_OFFSET

    def get_inputs(self):
        """Retrieves the data from all created Entry widgets."""
        return [entry.get() for entry in self.entries_created]
        
    def destroy_entries(self):
        """Destroy created entries"""
        for entry in self.entries_created:
            entry.destroy()

class CSVGenerator:
    def __init__(self):
        """Handles logic related to managing and generating CSV data."""
        self.big_list = []
        self.input_list = []
        self.num_of_items = 0

    def gen_csv(self, header_list, input_list, filename):
        """Simulates generating a CSV file with the given headers and input data."""
         # Initialize the CSV output in-memory (instead of file for demonstration purposes)
        csv_output = []
        # Extract headers (first elements) and subheaders (second elements) from header_list
        headers = [header[0] for header in header_list]
        subheaders = [header[1] for header in header_list]
        
        # Add headers and subheaders to the CSV output
        csv_output.append(headers)
        csv_output.append(subheaders)
        
        # Create groups of inputs based on the number of items for each subheader
        input_groups = []
        input_index = 0
        for header in header_list:
            num_items = header[2]
            input_groups.append(input_list[input_index:input_index + num_items])
            input_index += num_items
    
        # Now generate the rows based on these input groups
        def recursive_generate(current_row):
            """Recursive function to generate rows."""
            if len(current_row) == len(input_groups):
                # Add the current row with the correct number of columns
                csv_output.append(current_row + [""] * (len(headers) - len(current_row)))
                return
    
            # Generate the next part of the row by iterating over the current input group
            group = input_groups[len(current_row)]  # Get the current group to process
            if not group:  # Handle the case when there are no items for a header
                recursive_generate(current_row + [""])
            else:
                for item in group:
                    recursive_generate(current_row + [item])
    
        # Start the recursive generation process with an empty row
        recursive_generate([])

        # Write the result to a CSV file
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_output)

        print(f"CSV file '{filename}' has been created.")
            
    def add_item(self, title, name, num_inputs):
        """Adds an item to the big_list representing a CSV column."""
        self.big_list.append([title, name, num_inputs])

    def get_max_value(self):
        """Returns the maximum input value in the big_list."""
        return max([sublist[-1] for sublist in self.big_list])

class MainWindow:
    def __init__(self, window):
        """Initializes the main application window and its components."""
        self.window = window
        self.csv_gen = CSVGenerator()
        self.input_area = InputArea(window)

        self.create_initial_widgets()

        self.INPUTnum = 0
        self.OUTPUTnum = 0
        self.num_of_items = 0
        self.txt_title = ""
        self.txt_item_name = ""

    def create_initial_widgets(self):
        """Creates the initial input fields and widgets for INPUT and OUTPUT entry."""
        self.lbl_input = Label(self.window, text=LABEL_INPUT_TEXT, fg='black', font=LABEL_FONT)
        self.lbl_input.place(x=LABEL_X, y=INPUT_Y_OFFSET)

        self.spnbx_input = Spinbox(self.window, from_=0, to=10)
        self.spnbx_input.place(x=SPINBOX_X, y=INPUT_Y_OFFSET + 40)

        self.lbl_output = Label(self.window, text=LABEL_OUTPUT_TEXT, fg='black', font=LABEL_FONT)
        self.lbl_output.place(x=LABEL_X, y=INPUT_Y_OFFSET + 100)

        self.spnbx_output = Spinbox(self.window, from_=0, to=10)
        self.spnbx_output.place(x=SPINBOX_X, y=INPUT_Y_OFFSET + 140)

        self.btn_next = Button(self.window, text="Next", fg='black', font=BUTTON_FONT, command=self.on_next_click)
        self.btn_next.place(x=BUTTON_NEXT_X, y=INPUT_Y_OFFSET + 200)

    def on_next_click(self):
        """Handles the click event for the Next button, initiates the next steps."""
        self.INPUTnum = int(self.spnbx_input.get())
        self.OUTPUTnum = int(self.spnbx_output.get())
        self.num_of_items = self.INPUTnum + self.OUTPUTnum
        if self.INPUTnum > 0 and self.OUTPUTnum > 0:
            self.hide_initial_widgets()
            self.create_new_area()
        else:
            messagebox.showerror('Wrong numbers', 'Error: OUTPUT and INPUT numbers shall be more than 0')

    def hide_initial_widgets(self):
        """Hides the initial widgets after the first user input step."""
        self.lbl_input.destroy()
        self.spnbx_input.destroy()
        self.lbl_output.destroy()
        self.spnbx_output.destroy()
        self.btn_next.destroy()

    def create_new_area(self):
        """Creates the new area for column title and instance name input."""
        self.lbl_title = Label(self.window, text=LABEL_TITLE_TEXT, fg='black')
        self.lbl_title.place(x=LABEL_X, y=INPUT_Y_OFFSET)

        self.lbl_col_title = Label(self.window, text=LABEL_COLUMN_TITLE, fg='black')
        self.lbl_col_title.place(x=LABEL_X, y=INPUT_Y_OFFSET + 50)

        self.entry_col_title = Entry(self.window)
        self.entry_col_title.place(x=ENTRY_WIDTH, y=INPUT_Y_OFFSET + 50)

        self.lbl_instance_name = Label(self.window, text=LABEL_INSTANCE_NAME, fg='black')
        self.lbl_instance_name.place(x=LABEL_X, y=INPUT_Y_OFFSET + 100)

        self.entry_instance_name = Entry(self.window)
        self.entry_instance_name.place(x=ENTRY_WIDTH, y=INPUT_Y_OFFSET + 100)

        self.lbl_num_inputs = Label(self.window, text=LABEL_NUM_INPUTS, fg='black')
        self.lbl_num_inputs.place(x=LABEL_X, y=INPUT_Y_OFFSET + 150)

        self.entry_num_inputs = Entry(self.window)
        self.entry_num_inputs.place(x=ENTRY_WIDTH, y=INPUT_Y_OFFSET + 150)

        self.btn_next_item = Button(self.window, text="Next item", fg='black', font=BUTTON_FONT, command=self.on_next_item_click)
        self.btn_next_item.place(x=BUTTON_NEXT_X, y=INPUT_Y_OFFSET + 200)

    def on_next_item_click(self):
        """Handles the click event for 'Next item' button and processes the inputs."""
        if self.entry_col_title.get() and self.entry_instance_name.get() \
        and self.entry_num_inputs.get() and self.entry_num_inputs.get().isdigit() and \
        int(self.entry_num_inputs.get()) > 0:
            
            self.txt_title = self.entry_col_title.get()
            self.txt_item_name = self.entry_instance_name.get()
            num_of_input = int(self.entry_num_inputs.get() if self.num_of_items > self.OUTPUTnum else 0)
            
            self.csv_gen.add_item(self.txt_title, self.txt_item_name, num_of_input)
            self.num_of_items -= 1
            
            if self.num_of_items == self.OUTPUTnum:
                self.lbl_num_inputs.place_forget()
                self.entry_num_inputs["state"] = "disabled"
                self.entry_num_inputs.place_forget()
                
            if self.num_of_items > 0:
                self.clear_entries()
            else:
                self.complete_input()
        else:
            messagebox.showerror('Wrong input', 'wrong input or empty')

    def clear_entries(self):
        """Clears the input fields for the next item."""
        self.entry_col_title.delete(0, 'end')
        self.entry_instance_name.delete(0, 'end')
        if self.num_of_items > self.OUTPUTnum:
            self.entry_num_inputs.delete(0, 'end')

    def complete_input(self):
        """Finalizes the input process and sets up the input area for data entry."""
        self.lbl_title.destroy()
        self.lbl_col_title.destroy()
        self.entry_col_title.destroy()
        self.lbl_instance_name.destroy()
        self.entry_instance_name.destroy()
        self.lbl_num_inputs.destroy()
        self.entry_num_inputs.destroy()
        self.btn_next_item.destroy()

        self.num_of_items = self.INPUTnum
        
        next_input_num = int(self.csv_gen.big_list[self.INPUTnum - self.num_of_items][2])
        self.input_area.fill_input_area(next_input_num)

        self.btn_fill_inputs = Button(self.window, text="Fill input", fg='black', font=BUTTON_FONT, command=self.fill_inputs)
        max_val = self.csv_gen.get_max_value()
        self.btn_fill_inputs.place(x=BUTTON_FILL_X, y=BUTTON_FILL_Y)

    def fill_inputs(self):
        """Fills the inputs and proceeds with CSV generation."""
        inputs = self.input_area.get_inputs()
        if not (any(not subinput for subinput in inputs)):
            self.csv_gen.input_list.extend(inputs)
            self.input_area.destroy_entries()
            self.num_of_items -= 1

            if self.num_of_items > 0:
                next_input_num = int(self.csv_gen.big_list[self.INPUTnum - self.num_of_items][2])
                self.input_area.fill_input_area(next_input_num)
            else:
                self.btn_fill_inputs.destroy()
                self.btn_gen_csv = Button(self.window, text="Gen CSV", fg='black', font=GEN_CSV_FONT, command=self.generate_csv)
                self.btn_gen_csv.place(x=GEN_BTN_X, y=GEN_BTN_Y)
        else:
            messagebox.showerror('Wrong input', 'Error: one or more input is empty')

    def generate_csv(self):
        """Generates the CSV using the collected data."""
        self.csv_gen.gen_csv(self.csv_gen.big_list, self.csv_gen.input_list, "output.csv")


# Main application window configuration
window = Tk()
app = MainWindow(window)
window.title('CSV File Generator')
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.mainloop()