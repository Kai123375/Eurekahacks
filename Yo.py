import urllib.request
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import webbrowser
from datetime import datetime
import time
import math
import random
from PIL import Image, ImageTk
import io
import base64
import sys
import os
import platform
import socket
import calendar
from collections import defaultdict
import threading
from tkinter import filedialog
import re
import subprocess
import shutil
import ctypes
class MegaWeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WeatherGenius 360°")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2c3e50")
        
        # DeepSeek API configuration
        self.deepseek_api_key = "sk-cb6232f1d2d74459afa6c387a68d44ab" 
        
        # Weather API configuration
        self.weather_api_key = "0c05f41ac5a451327a3d939ac177efa2"
        
        # App state variables
        self.current_location = ""
        self.weather_data = None
        self.user_preferences = {
            "activities": ["hiking", "cycling", "picnics", "swimming"],
            "temperature_range": [15, 30],
            "units": "metric"
        }
        self.history = []
        self.favorites = []
        self.theme = "dark"
        self.notifications = []
        
        # Create colorful canvas
        self.canvas = tk.Canvas(self.root, bg="#2c3e50", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw decorative elements
        self.draw_sun()
        self.draw_clouds()
        self.draw_landscape()
        
        # Create UI frames
        self.create_main_frame()
        self.create_sidebar()
        self.create_bottom_bar()
        
        # Start periodic updates
        self.update_time() 
        self.root.after(60000, self.periodic_updates)
        
        # Load initial data
        self.load_default_location()
        
    def draw_sun(self):
        self.sun = self.canvas.create_oval(50, 50, 150, 150, fill="#f1c40f", outline="")
        
    def draw_clouds(self):
        for _ in range(5):
            x = random.randint(200, 1100)
            y = random.randint(50, 150)
            self.draw_cloud(x, y)
        
    def draw_cloud(self, x, y):
        color = "#ecf0f1"
        self.canvas.create_oval(x, y, x+50, y+50, fill=color, outline="")
        self.canvas.create_oval(x+30, y-20, x+80, y+30, fill=color, outline="")
        self.canvas.create_oval(x+70, y, x+120, y+50, fill=color, outline="")
        
    def draw_landscape(self):
        # Mountains
        self.canvas.create_polygon(0, 500, 200, 300, 400, 500, fill="#34495e", outline="")
        self.canvas.create_polygon(300, 500, 500, 250, 700, 500, fill="#2c3e50", outline="")
        self.canvas.create_polygon(600, 500, 800, 350, 1000, 500, fill="#34495e", outline="")
        self.canvas.create_polygon(900, 500, 1100, 400, 1200, 500, fill="#2c3e50", outline="")
        
        # Ground
        self.canvas.create_rectangle(0, 500, 1200, 800, fill="#27ae60", outline="")
        
    def create_main_frame(self):
        self.main_frame = tk.Frame(self.canvas, bg="#34495e", bd=2, relief=tk.RAISED)
        self.main_frame.place(relx=0.3, rely=0.1, relwidth=0.65, relheight=0.8)
        
        # Current weather display
        self.weather_display = tk.Label(
            self.main_frame, 
            text="Weather Information Will Appear Here",
            font=("Helvetica", 16),
            bg="#34495e",
            fg="#ecf0f1",
            wraplength=600,
            justify=tk.LEFT
        )
        self.weather_display.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Weather details notebook
        self.details_notebook = ttk.Notebook(self.main_frame)
        self.details_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Current weather tab
        self.current_tab = tk.Frame(self.details_notebook, bg="#34495e")
        self.create_current_weather_tab()
        self.details_notebook.add(self.current_tab, text="Current")
        
        # Forecast tab
        self.forecast_tab = tk.Frame(self.details_notebook, bg="#34495e")
        self.create_forecast_tab()
        self.details_notebook.add(self.forecast_tab, text="Forecast")
        
        # Maps tab
        self.maps_tab = tk.Frame(self.details_notebook, bg="#34495e")
        self.create_maps_tab()
        self.details_notebook.add(self.maps_tab, text="Maps")
        
        # Activities tab
        self.activities_tab = tk.Frame(self.details_notebook, bg="#34495e")
        self.create_activities_tab()
        self.details_notebook.add(self.activities_tab, text="Activities")
        
    def create_current_weather_tab(self):
        # Current weather details
        self.current_temp_label = tk.Label(
            self.current_tab,
            text="",
            font=("Helvetica", 48),
            bg="#34495e",
            fg="#f1c40f"
        )
        self.current_temp_label.pack(pady=10)
        
        self.weather_icon_label = tk.Label(self.current_tab, bg="#34495e")
        self.weather_icon_label.pack()
        
        self.weather_desc_label = tk.Label(
            self.current_tab,
            text="",
            font=("Helvetica", 18),
            bg="#34495e",
            fg="#ecf0f1"
        )
        self.weather_desc_label.pack(pady=5)
        
        # Weather details grid
        details_frame = tk.Frame(self.current_tab, bg="#34495e")
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Row 1
        tk.Label(details_frame, text="Feels Like:", bg="#34495e", fg="#bdc3c7").grid(row=0, column=0, sticky="e")
        self.feels_like_label = tk.Label(details_frame, text="", bg="#34495e", fg="#ecf0f1")
        self.feels_like_label.grid(row=0, column=1, sticky="w")
        
        tk.Label(details_frame, text="Humidity:", bg="#34495e", fg="#bdc3c7").grid(row=0, column=2, sticky="e")
        self.humidity_label = tk.Label(details_frame, text="", bg="#34495e", fg="#ecf0f1")
        self.humidity_label.grid(row=0, column=3, sticky="w")
        
        # Row 2
        tk.Label(details_frame, text="Pressure:", bg="#34495e", fg="#bdc3c7").grid(row=1, column=0, sticky="e")
        self.pressure_label = tk.Label(details_frame, text="", bg="#34495e", fg="#ecf0f1")
        self.pressure_label.grid(row=1, column=1, sticky="w")
        
        tk.Label(details_frame, text="Visibility:", bg="#34495e", fg="#bdc3c7").grid(row=1, column=2, sticky="e")
        self.visibility_label = tk.Label(details_frame, text="", bg="#34495e", fg="#ecf0f1")
        self.visibility_label.grid(row=1, column=3, sticky="w")
        
        # Row 3
        tk.Label(details_frame, text="Wind Speed:", bg="#34495e", fg="#bdc3c7").grid(row=2, column=0, sticky="e")
        self.wind_speed_label = tk.Label(details_frame, text="", bg="#34495e", fg="#ecf0f1")
        self.wind_speed_label.grid(row=2, column=1, sticky="w")
        
        tk.Label(details_frame, text="Wind Direction:", bg="#34495e", fg="#bdc3c7").grid(row=2, column=2, sticky="e")
        self.wind_dir_label = tk.Label(details_frame, text="", bg="#34495e", fg="#ecf0f1")
        self.wind_dir_label.grid(row=2, column=3, sticky="w")
        
        # Row 4
        tk.Label(details_frame, text="Sunrise:", bg="#34495e", fg="#bdc3c7").grid(row=3, column=0, sticky="e")
        self.sunrise_label = tk.Label(details_frame, text="", bg="#34495e", fg="#ecf0f1")
        self.sunrise_label.grid(row=3, column=1, sticky="w")
        
        tk.Label(details_frame, text="Sunset:", bg="#34495e", fg="#bdc3c7").grid(row=3, column=2, sticky="e")
        self.sunset_label = tk.Label(details_frame, text="", bg="#34495e", fg="#ecf0f1")
        self.sunset_label.grid(row=3, column=3, sticky="w")
        
    def create_forecast_tab(self):
        self.forecast_canvas = tk.Canvas(self.forecast_tab, bg="#34495e", highlightthickness=0)
        self.forecast_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.forecast_scroll = ttk.Scrollbar(
            self.forecast_tab, 
            orient=tk.VERTICAL, 
            command=self.forecast_canvas.yview
        )
        self.forecast_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.forecast_canvas.configure(yscrollcommand=self.forecast_scroll.set)
        self.forecast_canvas.bind('<Configure>', lambda e: self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all")))
        
        self.forecast_frame = tk.Frame(self.forecast_canvas, bg="#34495e")
        self.forecast_canvas.create_window((0, 0), window=self.forecast_frame, anchor="nw")
        
    def create_maps_tab(self):
        self.map_label = tk.Label(
            self.maps_tab,
            text="Map View Will Appear Here",
            font=("Helvetica", 16),
            bg="#34495e",
            fg="#ecf0f1"
        )
        self.map_label.pack(pady=50)
        
        self.open_map_button = tk.Button(
            self.maps_tab,
            text="Open in Browser",
            command=self.open_map_in_browser,
            bg="#3498db",
            fg="white",
            relief=tk.RAISED
        )
        self.open_map_button.pack(pady=10)
        
    def create_activities_tab(self):
        self.activities_text = scrolledtext.ScrolledText(
            self.activities_tab,
            wrap=tk.WORD,
            width=60,
            height=20,
            font=("Helvetica", 12),
            bg="#34495e",
            fg="#ecf0f1"
        )
        self.activities_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.refresh_activities_button = tk.Button(
            self.activities_tab,
            text="Get Activity Suggestions",
            command=self.get_activity_suggestions,
            bg="#2ecc71",
            fg="white",
            relief=tk.RAISED
        )
        self.refresh_activities_button.pack(pady=10)
        
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.canvas, bg="#34495e", bd=2, relief=tk.RAISED)
        self.sidebar.place(relx=0.02, rely=0.1, relwidth=0.25, relheight=0.8)
        
        # Location entry
        tk.Label(
            self.sidebar,
            text="Enter Location:",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Helvetica", 12)
        ).pack(pady=(10, 5))
        
        self.location_entry = tk.Entry(
            self.sidebar,
            font=("Helvetica", 12),
            width=20
        )
        self.location_entry.pack(pady=5, padx=10)
        self.location_entry.bind("<Return>", lambda e: self.get_weather_data())
        
        self.search_button = tk.Button(
            self.sidebar,
            text="Search",
            command=self.get_weather_data,
            bg="#3498db",
            fg="white",
            relief=tk.RAISED
        )
        self.search_button.pack(pady=5)
        
        # Current location button
        self.current_loc_button = tk.Button(
            self.sidebar,
            text="Use Current Location",
            command=self.use_current_location,
            bg="#2ecc71",
            fg="white",
            relief=tk.RAISED
        )
        self.current_loc_button.pack(pady=5)
        
        # Favorites list
        tk.Label(
            self.sidebar,
            text="Favorites:",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Helvetica", 12)
        ).pack(pady=(20, 5))
        
        self.favorites_listbox = tk.Listbox(
            self.sidebar,
            height=5,
            bg="#2c3e50",
            fg="#ecf0f1",
            selectbackground="#3498db"
        )
        self.favorites_listbox.pack(fill=tk.X, padx=10, pady=5)
        self.favorites_listbox.bind("<<ListboxSelect>>", self.select_favorite)
        
        # Add/remove favorite buttons
        fav_button_frame = tk.Frame(self.sidebar, bg="#34495e")
        fav_button_frame.pack(pady=5)
        
        self.add_fav_button = tk.Button(
            fav_button_frame,
            text="Add",
            command=self.add_favorite,
            bg="#f39c12",
            fg="white",
            relief=tk.RAISED
        )
        self.add_fav_button.pack(side=tk.LEFT, padx=5)
        
        self.remove_fav_button = tk.Button(
            fav_button_frame,
            text="Remove",
            command=self.remove_favorite,
            bg="#e74c3c",
            fg="white",
            relief=tk.RAISED
        )
        self.remove_fav_button.pack(side=tk.LEFT, padx=5)
        
        # History list
        tk.Label(
            self.sidebar,
            text="History:",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Helvetica", 12)
        ).pack(pady=(20, 5))
        
        self.history_listbox = tk.Listbox(
            self.sidebar,
            height=5,
            bg="#2c3e50",
            fg="#ecf0f1",
            selectbackground="#3498db"
        )
        self.history_listbox.pack(fill=tk.X, padx=10, pady=5)
        self.history_listbox.bind("<<ListboxSelect>>", self.select_history)
        
        # Units selection
        tk.Label(
            self.sidebar,
            text="Units:",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Helvetica", 12)
        ).pack(pady=(20, 5))
        
        self.units_var = tk.StringVar(value="metric")
        tk.Radiobutton(
            self.sidebar,
            text="Metric (°C, m/s)",
            variable=self.units_var,
            value="metric",
            bg="#34495e",
            fg="#ecf0f1",
            selectcolor="#2c3e50",
            command=self.change_units
        ).pack(anchor=tk.W)
        
        tk.Radiobutton(
            self.sidebar,
            text="Imperial (°F, mph)",
            variable=self.units_var,
            value="imperial",
            bg="#34495e",
            fg="#ecf0f1",
            selectcolor="#2c3e50",
            command=self.change_units
        ).pack(anchor=tk.W)
        
        # Theme selection
        tk.Label(
            self.sidebar,
            text="Theme:",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Helvetica", 12)
        ).pack(pady=(20, 5))
        
        self.theme_var = tk.StringVar(value="dark")
        tk.Radiobutton(
            self.sidebar,
            text="Dark",
            variable=self.theme_var,
            value="dark",
            bg="#34495e",
            fg="#ecf0f1",
            selectcolor="#2c3e50",
            command=self.change_theme
        ).pack(anchor=tk.W)
        
        tk.Radiobutton(
            self.sidebar,
            text="Light",
            variable=self.theme_var,
            value="light",
            bg="#34495e",
            fg="#ecf0f1",
            selectcolor="#2c3e50",
            command=self.change_theme
        ).pack(anchor=tk.W)
        
    def create_bottom_bar(self):
        self.bottom_bar = tk.Frame(self.canvas, bg="#34495e", height=30)
        self.bottom_bar.place(relx=0, rely=0.95, relwidth=1, relheight=0.05)
        
        # Time display
        self.time_label = tk.Label(
            self.bottom_bar,
            text="",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Helvetica", 10)
        )
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        # Status message
        self.status_label = tk.Label(
            self.bottom_bar,
            text="Ready",
            bg="#34495e",
            fg="#ecf0f1",
            font=("Helvetica", 10)
        )
        self.status_label.pack(side=tk.LEFT, padx=10, expand=True)
        
        # App version
        tk.Label(
            self.bottom_bar,
            text="WeatherGenius 360° v1.0",
            bg="#34495e",
            fg="#bdc3c7",
            font=("Helvetica", 10)
        ).pack(side=tk.RIGHT, padx=10)
        
    def update_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)
        
    def periodic_updates(self):
        if self.current_location:
            self.get_weather_data()
        self.root.after(60000, self.periodic_updates)
        
    def load_default_location(self):
        # Try to load last used location
        try:
            with open("weather_prefs.json", "r") as f:
                prefs = json.load(f)
                self.current_location = prefs.get("last_location", "")
                self.favorites = prefs.get("favorites", [])
                self.history = prefs.get("history", [])
                self.user_preferences = prefs.get("preferences", self.user_preferences)
                
                # Update UI
                self.location_entry.insert(0, self.current_location)
                self.update_favorites_list()
                self.update_history_list()
                
                if self.current_location:
                    self.get_weather_data()
        except (FileNotFoundError, json.JSONDecodeError):
            pass
            
    def save_preferences(self):
        prefs = {
            "last_location": self.current_location,
            "favorites": self.favorites,
            "history": self.history,
            "preferences": self.user_preferences
        }
        
        with open("weather_prefs.json", "w") as f:
            json.dump(prefs, f)
            
    def get_weather_data(self):
        location = self.location_entry.get().strip()
        if not location:
            messagebox.showwarning("Input Error", "Please enter a location")
            return
            
        self.current_location = location
        self.status_label.config(text=f"Fetching weather for {location}...")
        self.root.update()
        
        try:
            # Get weather data
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api_key}&units={self.units_var.get()}"
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                self.weather_data = data
                
                # Add to history if not already there
                if location not in self.history:
                    self.history.insert(0, location)
                    if len(self.history) > 10:
                        self.history.pop()
                    self.update_history_list()
                
                # Update display
                self.update_weather_display()
                self.status_label.config(text=f"Weather data loaded for {location}")
                
                # Save preferences
                self.save_preferences()
                
        except urllib.error.URLError as e:
            messagebox.showerror("Network Error", f"Could not fetch weather data: {e}")
            self.status_label.config(text="Error fetching weather data")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_label.config(text="Error occurred")
            
    def update_weather_display(self):
        if not self.weather_data:
            return
            
        data = self.weather_data
        units = self.units_var.get()
        
        # Main weather info
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        weather_desc = data["weather"][0]["description"].capitalize()
        icon_code = data["weather"][0]["icon"]
        wind_speed = data["wind"]["speed"]
        wind_deg = data["wind"].get("deg", 0)
        visibility = data.get("visibility", "N/A")
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
        
        # Convert visibility to km if in metric
        if visibility != "N/A" and units == "metric":
            visibility = f"{visibility/1000:.1f} km"
            
        # Wind direction
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        wind_dir = directions[round(wind_deg / 45) % 8]
        
        # Update labels
        self.current_temp_label.config(text=f"{temp:.1f}°{'C' if units == 'metric' else 'F'}")
        self.weather_desc_label.config(text=weather_desc)
        self.feels_like_label.config(text=f"{feels_like:.1f}°{'C' if units == 'metric' else 'F'}")
        self.humidity_label.config(text=f"{humidity}%")
        self.pressure_label.config(text=f"{pressure} hPa")
        self.visibility_label.config(text=visibility)
        self.wind_speed_label.config(text=f"{wind_speed} {'m/s' if units == 'metric' else 'mph'}")
        self.wind_dir_label.config(text=f"{wind_dir} ({wind_deg}°)")
        self.sunrise_label.config(text=sunrise)
        self.sunset_label.config(text=sunset)
        
        # Load weather icon
        self.load_weather_icon(icon_code)
        
        # Update forecast
        self.get_forecast_data()
        
        # Update activities tab
        self.get_activity_suggestions()
        
    def load_weather_icon(self, icon_code):
        try:
            # Try to load icon from OpenWeatherMap
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            with urllib.request.urlopen(url) as response:
                image_data = response.read()
                
            image = Image.open(io.BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)
            
            self.weather_icon_label.config(image=photo)
            self.weather_icon_label.image = photo
        except Exception as e:
            print(f"Error loading weather icon: {e}")
            
    def get_forecast_data(self):
        if not self.current_location:
            return
            
        try:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={self.current_location}&appid={self.weather_api_key}&units={self.units_var.get()}"
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
                # Clear previous forecast
                for widget in self.forecast_frame.winfo_children():
                    widget.destroy()
                
                # Group by day
                daily_forecasts = defaultdict(list)
                for forecast in data["list"]:
                    date = datetime.fromtimestamp(forecast["dt"]).strftime("%Y-%m-%d")
                    daily_forecasts[date].append(forecast)
                
                # Display 5-day forecast
                for i, (date, forecasts) in enumerate(daily_forecasts.items()):
                    if i >= 5:
                        break
                        
                    day_frame = tk.Frame(self.forecast_frame, bg="#2c3e50", bd=1, relief=tk.RAISED)
                    day_frame.pack(fill=tk.X, padx=5, pady=5)
                    
                    # Day header
                    day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
                    tk.Label(
                        day_frame,
                        text=f"{day_name} ({date})",
                        font=("Helvetica", 12, "bold"),
                        bg="#2c3e50",
                        fg="#f1c40f"
                    ).pack(anchor=tk.W, padx=10, pady=5)
                    
                    # Time slots
                    for forecast in forecasts[:3]:  # Show max 3 time slots per day
                        time_str = datetime.fromtimestamp(forecast["dt"]).strftime("%H:%M")
                        temp = forecast["main"]["temp"]
                        desc = forecast["weather"][0]["description"].capitalize()
                        icon_code = forecast["weather"][0]["icon"]
                        
                        slot_frame = tk.Frame(day_frame, bg="#34495e")
                        slot_frame.pack(fill=tk.X, padx=20, pady=5)
                        
                        tk.Label(
                            slot_frame,
                            text=time_str,
                            bg="#34495e",
                            fg="#ecf0f1",
                            width=8
                        ).pack(side=tk.LEFT)
                        
                        # Try to load icon
                        try:
                            url = f"http://openweathermap.org/img/wn/{icon_code}.png"
                            with urllib.request.urlopen(url) as response:
                                image_data = response.read()
                                image = Image.open(io.BytesIO(image_data))
                                photo = ImageTk.PhotoImage(image)
                                
                                icon_label = tk.Label(slot_frame, image=photo, bg="#34495e")
                                icon_label.image = photo
                                icon_label.pack(side=tk.LEFT, padx=5)
                        except:
                            pass
                            
                        tk.Label(
                            slot_frame,
                            text=f"{temp:.1f}°{'C' if self.units_var.get() == 'metric' else 'F'} - {desc}",
                            bg="#34495e",
                            fg="#ecf0f1"
                        ).pack(side=tk.LEFT, padx=10)
                
                self.forecast_canvas.yview_moveto(0)
                
        except Exception as e:
            print(f"Error loading forecast: {e}")
            
    def get_activity_suggestions(self):
        if not self.weather_data:
            self.activities_text.delete(1.0, tk.END)
            self.activities_text.insert(tk.END, "No weather data available. Please search for a location first.")
            return
            
        try:
            # Prepare weather context for DeepSeek
            weather_context = {
                "temperature": self.weather_data["main"]["temp"],
                "conditions": self.weather_data["weather"][0]["description"],
                "humidity": self.weather_data["main"]["humidity"],
                "wind_speed": self.weather_data["wind"]["speed"],
                "location": self.current_location,
                "time_of_day": datetime.now().strftime("%H:%M"),
                "user_preferences": self.user_preferences
            }
            
            # Call DeepSeek API
            prompt = (
                f"Based on the current weather conditions at {self.current_location}, "
                f"provide detailed suggestions for outdoor activities. "
                f"Current weather: {weather_context['conditions']}, "
                f"Temperature: {weather_context['temperature']}°{'C' if self.units_var.get() == 'metric' else 'F'}, "
                f"Humidity: {weather_context['humidity']}%, "
                f"Wind Speed: {weather_context['wind_speed']} {'m/s' if self.units_var.get() == 'metric' else 'mph'}. "
                f"Consider the user's preferences: {self.user_preferences}. "
                f"Provide a comprehensive list of at least 10 specific activity suggestions "
                f"with explanations of why each activity is suitable for the current conditions. "
                f"Also include any precautions or recommendations for clothing/equipment."
            )
            
            # In a real app, you would make an API call to DeepSeek here
            # For this example, we'll simulate a response
            simulated_response = self.simulate_deepseek_response(weather_context)
            
            # Display the response
            self.activities_text.delete(1.0, tk.END)
            self.activities_text.insert(tk.END, simulated_response)
            
        except Exception as e:
            self.activities_text.delete(1.0, tk.END)
            self.activities_text.insert(tk.END, f"Error generating suggestions: {str(e)}")
            
    def simulate_deepseek_response(self, weather_context):
        """Simulate a response from DeepSeek API for demonstration purposes"""
        temp = weather_context["temperature"]
        conditions = weather_context["conditions"].lower()
        location = weather_context["location"]
        
        response = f"Activity Suggestions for {location} ({temp}°{'C' if self.units_var.get() == 'metric' else 'F'}, {conditions})\n\n"
        response += "="*80 + "\n\n"
        
        if "rain" in conditions:
            response += "It's rainy today, but here are some great activities:\n"
            response += "1. Visit a museum or art gallery - perfect indoor activity\n"
            response += "2. Coffee shop hopping - explore local cafes with umbrellas\n"
            response += "3. Indoor rock climbing - get active while staying dry\n"
            response += "4. Bookstore browsing - cozy way to spend a rainy day\n"
            response += "5. Cooking class - learn to make comfort food for rainy weather\n"
            response += "\nDon't forget your waterproof jacket and umbrella if going outside!\n"
        elif "snow" in conditions:
            response += "Snowy day activities:\n"
            response += "1. Build a snowman or snow fort\n"
            response += "2. Go sledding at a local hill\n"
            response += "3. Try cross-country skiing\n"
            response += "4. Have a snowball fight with friends\n"
            response += "5. Visit a nearby ski resort\n"
            response += "\nDress in layers and wear waterproof boots!\n"
        elif temp > 30:
            response += "Hot weather activities:\n"
            response += "1. Visit a water park or swimming pool\n"
            response += "2. Go to the beach if nearby\n"
            response += "3. Early morning hike before it gets too hot\n"
            response += "4. Indoor ice skating rink to cool off\n"
            response += "5. Evening outdoor concert or movie\n"
            response += "\nStay hydrated and wear sunscreen!\n"
        elif temp > 20:
            response += "Perfect weather for outdoor activities:\n"
            response += "1. Hiking in local nature trails\n"
            response += "2. Picnic in the park\n"
            response += "3. Outdoor sports (tennis, basketball, soccer)\n"
            response += "4. Cycling around the city or countryside\n"
            response += "5. Visit a botanical garden\n"
            response += "\nLight jacket might be needed in the evening.\n"
        elif temp > 10:
            response += "Cool weather activities:\n"
            response += "1. Jogging or brisk walking\n"
            response += "2. Visit outdoor markets or fairs\n"
            response += "3. Photography walk to capture autumn colors\n"
            response += "4. Apple picking if in season\n"
            response += "5. Outdoor yoga session\n"
            response += "\nWear layers that you can remove as you warm up.\n"
        else:
            response += "Cold weather activities:\n"
            response += "1. Winter hiking with proper gear\n"
            response += "2. Ice skating at an outdoor rink\n"
            response += "3. Visit Christmas markets if in season\n"
            response += "4. Birdwatching with warm drinks\n"
            response += "5. Snowshoeing if snow is available\n"
            response += "\nDress warmly with hat, gloves, and insulated boots.\n"
            
        response += "\n" + "="*80 + "\n"
        response += "Additional Recommendations:\n"
        response += f"- Current UV index: {random.randint(3,8)} ({'moderate' if temp > 15 else 'low'})\n"
        response += f"- Air quality: {'good' if random.random() > 0.3 else 'moderate'}\n"
        response += f"- Sunrise was at {self.weather_data['sys']['sunrise']}, sunset at {self.weather_data['sys']['sunset']}\n"
        response += "- Consider checking pollen count if you have allergies\n"
        
        return response
        
    def open_map_in_browser(self):
        if not self.current_location:
            messagebox.showwarning("No Location", "Please search for a location first")
            return
            
        try:
            url = f"https://www.google.com/maps/place/{self.current_location.replace(' ', '+')}"
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open map: {e}")
            
    def use_current_location(self):
        try:
            # In a real app, you would use geolocation here
            # For this example, we'll simulate getting location
            simulated_location = "New York,US"
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, simulated_location)
            self.get_weather_data()
        except Exception as e:
            messagebox.showerror("Error", f"Could not get current location: {e}")
            
    def update_favorites_list(self):
        self.favorites_listbox.delete(0, tk.END)
        for loc in self.favorites:
            self.favorites_listbox.insert(tk.END, loc)
            
    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for loc in self.history:
            self.history_listbox.insert(tk.END, loc)
            
    def add_favorite(self):
        if self.current_location and self.current_location not in self.favorites:
            self.favorites.append(self.current_location)
            self.update_favorites_list()
            self.save_preferences()
            
    def remove_favorite(self):
        selection = self.favorites_listbox.curselection()
        if selection:
            del self.favorites[selection[0]]
            self.update_favorites_list()
            self.save_preferences()
            
    def select_favorite(self, event):
        selection = self.favorites_listbox.curselection()
        if selection:
            location = self.favorites_listbox.get(selection[0])
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, location)
            self.get_weather_data()
            
    def select_history(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            location = self.history_listbox.get(selection[0])
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, location)
            self.get_weather_data()
            
    def change_units(self):
        if self.weather_data:
            self.get_weather_data()
            
    def change_theme(self):
        theme = self.theme_var.get()
        
        if theme == "dark":
            bg_color = "#2c3e50"
            fg_color = "#ecf0f1"
            widget_bg = "#34495e"
            accent = "#3498db"
        else:
            bg_color = "#ecf0f1"
            fg_color = "#2c3e50"
            widget_bg = "#bdc3c7"
            accent = "#2980b9"
            
        # Update root window
        self.root.config(bg=bg_color)
        self.canvas.config(bg=bg_color)
        
        # Update frames
        self.main_frame.config(bg=widget_bg)
        self.sidebar.config(bg=widget_bg)
        self.bottom_bar.config(bg=widget_bg)
        
        # Update all widgets
        for widget in self.main_frame.winfo_children():
            try:
                widget.config(bg=widget_bg, fg=fg_color)
            except:
                pass
                
        for widget in self.sidebar.winfo_children():
            try:
                widget.config(bg=widget_bg, fg=fg_color)
            except:
                pass
                
        for widget in self.bottom_bar.winfo_children():
            try:
                widget.config(bg=widget_bg, fg=fg_color) 
            except:
                pass
                
        # Special cases
        self.weather_display.config(bg=widget_bg, fg=fg_color)
        self.current_temp_label.config(bg=widget_bg, fg=accent)
        
        # Save preference
        self.user_preferences["theme"] = theme
        self.save_preferences()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MegaWeatherApp()
    app.run()