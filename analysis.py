import pandas as pd
from tkinter import Tk, filedialog, Label, Button, Listbox, Scrollbar, END, messagebox
import matplotlib.pyplot as plt
import numpy as np

# Function to load the CSV file
def load_file():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return
    global data
    data = pd.read_csv(filepath)
    label_status.config(text=f"Loaded {len(data)} responses")
    display_data()

# Function to display the data in the listbox
def display_data():
    listbox_data.delete(0, END)
    for index, row in data.iterrows():
        listbox_data.insert(END, f"{index}: {row['Name']} ({row['Age']} {row['Gender']})")

# Function to analyze and display the response of one person as a pie chart
def show_individual_response():
    if data is None:
        label_status.config(text="No data loaded")
        return
    
    selected_index = listbox_data.curselection()
    if not selected_index:
        messagebox.showwarning("Selection Error", "Please select a person from the list.")
        return
    
    # Get the selected person's index and data
    selected_index = int(selected_index[0])
    person = data.iloc[selected_index]

    # Extract questions and responses for the selected person
    questions = data.columns[3:]  # Assuming first 3 columns are Name, Age, and Gender
    responses = person[3:]  # Responses for the selected person

    # Convert responses to numeric, coercing errors to NaN
    responses_numeric = pd.to_numeric(responses, errors='coerce')

    # Filter out NaN values to avoid plotting non-numeric responses
    valid_mask = responses_numeric.notna()
    valid_questions = questions[valid_mask]
    valid_responses = responses_numeric[valid_mask]

    if valid_responses.empty:
        messagebox.showinfo("No Data", "No valid responses to display.")
        return

    # Plot the responses as a pie chart
    plt.figure(figsize=(12, 12))
    plt.pie(valid_responses, labels=valid_questions, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    
    # Display the name, age, and gender as a title above the pie chart
    title_text = f"Responses for {person['Name']} ({person['Age']} {person['Gender']})"
    plt.title(title_text, fontsize=16)

    plt.show()

# Initialize the Tkinter application
root = Tk()
root.title("Mental Health Survey Analysis")

data = None

# Create GUI Elements
label_title = Label(root, text="Mental Health Survey Analyzer", font=("Arial", 16))
label_title.pack(pady=10)

btn_load = Button(root, text="Load Survey Data", command=load_file)
btn_load.pack(pady=5)

btn_show = Button(root, text="Show Individual Response", command=show_individual_response)
btn_show.pack(pady=5)

label_status = Label(root, text="No data loaded", fg="red")
label_status.pack(pady=5)

scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")

listbox_data = Listbox(root, yscrollcommand=scrollbar.set, width=80, height=20)
listbox_data.pack(pady=10)

scrollbar.config(command=listbox_data.yview)

# Run the Tkinter event loop
root.mainloop()
