import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model
import random
from itertools import cycle

# Load the saved model
model = load_model('Classfication_model.h5')

# Define class labels for both languages
class_labels = {
    "english": ["Healthy", "Pneumonia"],
    "russian": ["Здоров", "Пневмония"]
}

# Function to preprocess the input image
def preprocess_image(image):
    img = image.resize((224, 224))
    img = np.array(img)
    img = img / 255.0  # Normalize the image
    img = np.expand_dims(img, axis=-1)  # Add channel dimension
    img = np.repeat(img, 3, axis=-1)  # Repeat grayscale image to have 3 channels
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Function to make predictions
def predict_image(model, image):
    preprocessed_img = preprocess_image(image)
    prediction = model.predict(preprocessed_img)
    return prediction

# Function to get predicted class and probability
def get_predicted_class(prediction, lang):
    predicted_class_index = np.argmax(prediction)
    predicted_class = class_labels[lang][predicted_class_index]
    probability = prediction[0][predicted_class_index]
    return predicted_class, probability

# Function to open file dialog and make prediction
def upload_predict():
    filename = filedialog.askopenfilename()
    if filename:
        # Clear previous prediction
        result_label.config(text="")
        recommendation_label.config(text="")
        # Display the image preview
        img_preview = Image.open(filename)
        img_preview = img_preview.resize((200, 200), Image.LANCZOS)
        img_preview = ImageTk.PhotoImage(img_preview)
        img_label.config(image=img_preview)
        img_label.image = img_preview
        # Show progress bar
        progress_bar.pack(pady=10)
        # Make prediction
        progress_bar["value"] = 0  # Reset progress bar
        root.update_idletasks()  # Update GUI to show progress bar reset
        progress_bar["maximum"] = 100  # Set maximum value for progress bar
        progress_step = 100 / 10  # Define step for updating progress bar
        for i in range(10):
            progress_bar["value"] += progress_step
            root.update_idletasks()  # Update GUI to show progress
            # Simulate some processing time (you can replace this with actual prediction)
            root.after(100)  # Pause for 100 milliseconds
        image = Image.open(filename)
        prediction = predict_image(model, image)
        lang = language_var.get()
        predicted_class, probability = get_predicted_class(prediction, lang)
        # Update result label with predicted class and probability
        if lang == "english":
            result_label.config(text=f"Class: {predicted_class}, Probability: {probability:.2f}",
                                foreground="green" if predicted_class == "Healthy" else "red")
        else:
            result_label.config(text=f"Класс: {predicted_class}, Вероятность: {probability:.2f}",
                                foreground="green" if predicted_class == "Здоров" else "red")
        # Display funny message
        if predicted_class == "Pneumonia":
            recommendation_label.config(text="Recommendation: Consult a healthcare professional for treatment.")
        elif predicted_class == "Healthy":
            funny_messages = [
                "You're as healthy as a horse!",
                "Congratulations! You've won the health lottery!",
                "Keep up the good work!",
                "No pneumonia here, just good vibes!",
                "Looks like you're all clear! Time to celebrate!"
            ]
            random_message = random.choice(funny_messages)
            recommendation_label.config(text=random_message)
        # Hide progress bar
        progress_bar.pack_forget()

# Function to update text according to selected language
def update_language(*args):
    lang = language_var.get()
    if lang == "english":
        upload_button.config(text="Choose Image")
        english_radio.config(text="English")
        russian_radio.config(text="Russian")
    else:
        upload_button.config(text="Выберите изображение")
        english_radio.config(text="Английский")
        russian_radio.config(text="Русский")

# Function to toggle between dark and light themes
def toggle_theme():
    current_theme = root.tk.call("ttk::style", "theme", "use")
    if current_theme == "clam":
        root.tk.call("ttk::style", "theme", "use", "alt")
        root.configure(bg='black')  # Set the background color to black
    else:
        root.tk.call("ttk::style", "theme", "use", "clam")
        root.configure(bg='white')  # Set the background color to white

# Function to display information about the program
def about_program():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_label = ttk.Label(about_window, text="This program was developed by RMT Products.")
    about_label.pack(padx=20, pady=20)

# Create GUI
root = tk.Tk()
root.title("Detect Pneumonia | RMT product")
root.geometry('800x500')  # Set the window size

# Language selection and theme toggle
lang_theme_frame = ttk.Frame(root, style="TFrame")
lang_theme_frame.pack(pady=10, padx=10, side="left", fill="y")

language_var = tk.StringVar()
language_var.set("english")  # Default language is English
language_var.trace("w", update_language)  # Bind update_language to language selection change

english_radio = ttk.Radiobutton(lang_theme_frame, text="English", variable=language_var, value="english", style="TRadiobutton")
english_radio.pack(side="top", padx=5, pady=5, fill="x")
russian_radio = ttk.Radiobutton(lang_theme_frame, text="Russian", variable=language_var, value="russian", style="TRadiobutton")
russian_radio.pack(side="top", padx=5, pady=5, fill="x")

theme_button = ttk.Button(lang_theme_frame, text="Toggle Theme", command=toggle_theme)
theme_button.pack(fill="both", padx=10, pady=10)

about_button = ttk.Button(lang_theme_frame, text="About", command=about_program)
about_button.pack(fill="both", padx=10, pady=10)

upload_button = ttk.Button(root, text="Choose Image", command=upload_predict)
upload_button.pack(pady=20, padx=10, side="top", fill="x")

# Label for displaying image preview
img_label = ttk.Label(root)
img_label.pack(padx=10, side="top", fill="both")

# Progress bar
progress_bar = ttk.Progressbar(root, mode='determinate', length=300)
progress_bar.pack(pady=10, padx=10, side="top", fill="x")

# Label for displaying prediction result
result_label = ttk.Label(root)
result_label.pack(pady=10, padx=10, side='top', fill="both")

# Label for displaying recommendation or advice
recommendation_label = ttk.Label(root, wraplength=700)
recommendation_label.pack(pady=10, padx=10, side='bottom', fill="both")

root.mainloop()
