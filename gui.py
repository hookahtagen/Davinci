import tkinter as tk
import openai
from fpdf import FPDF
import tkinter.filedialog as filedialog

# Replace YOUR_API_KEY with your actual API key
openai.api_key = "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"

def send_message():
    # Get the message from the entry field
    message = entry.get()
    
    # Send the message to the OpenAI API and get the response
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=message,
    max_tokens=1024,
    temperature=0.5,
    top_p=1,
    presence_penalty=0.65,
    frequency_penalty=0.34,
    best_of=1
    )
    
    response = response["choices"][0]["text"]
    print(response)
    print("*******************************************\n\n")
    # Display the response in the text box
    text.insert(tk.END, response)

def print_pdf():
    # Create a PDF object
    pdf = FPDF()
    
    # Add a page to the PDF
    pdf.add_page()
    
    # Set the font and size
    pdf.set_font("Arial", size=12)
    
    # Get the response text from the text box
    response_text = text.get("1.0", "end")
    
    # Write the response text to the PDF
    pdf.multi_cell(0, 10, txt=response_text)
    
    # Prompt the user to select a file path to save the PDF
    filepath = filedialog.asksaveasfilename(defaultextension=".pdf")
    
    # Save the PDF to the selected file path
    pdf.output(name=filepath)

def save_text():
    # Get the message from the entry field
    message = entry.get()
    
    # Get the response text from the text box
    response_text = text.get("1.0", "end")
    
    # Concatenate the prompt and response text
    output_text = "Prompt:\n" + message + "\n\nResponse:\n" + response_text
    
    # Prompt the user to select a file path to save the text file
    filepath = filedialog.asksaveasfilename(defaultextension=".txt")
    
    # Write the output text to the file
    with open(filepath, "w") as f:
        f.write(output_text)

# Create the GUI
root = tk.Tk()
root.title("OpenAI API")

# Create the entry field and send button
entry = tk.Entry(root, width=50)
entry.pack()

button = tk.Button(root, text="Send", command=send_message)
button.pack()

# Create the text box for displaying the response
text = tk.Text(root, width=50, height=10)
text.pack()

# Create the print PDF button
pdf_button = tk.Button(root, text="Print PDF", command=print_pdf)
pdf_button.pack()

# Create the save text button
text_button = tk.Button(root, text="Save Text", command=save_text)
text_button.pack()

root.mainloop()
