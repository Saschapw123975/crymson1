import customtkinter as ctk
import requests
import json
import webbrowser
import time
import threading
import tkinter as tk
from datetime import datetime
import hashlib
import platform
import uuid

class AboutWindow:
    def __init__(self, parent):
        self.popup = ctk.CTkToplevel(parent)
        self.popup.title("About Crymson")
        self.popup.geometry("500x600")
        self.popup.transient(parent)
        self.popup.grab_set()
        
        self.colors = {
            "crimson": "#DC143C",
            "dark_grey": "#1A1A1A",
            "light_grey": "#2D2D2D",
            "text_grey": "#E6E6E6",
            "accent": "#FF1F4D"
        }
        
        self.popup.configure(fg_color=self.colors["dark_grey"])
        
        logo_frame = ctk.CTkFrame(self.popup, fg_color=self.colors["dark_grey"])
        logo_frame.pack(fill="x", pady=(20, 0))
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text="CRYMSON",
            font=("Segoe UI", 32, "bold"),
            text_color=self.colors["accent"]
        )
        title_label.pack(pady=(0, 5))
        
        version_label = ctk.CTkLabel(
            logo_frame,
            text=f"Version 1.1.0 ({platform.system()} Build)",
            font=("Segoe UI", 12),
            text_color=self.colors["text_grey"]
        )
        version_label.pack(pady=(0, 20))
        
        current_year = datetime.now().year
        copyright_text = f"""
© {current_year} Crymson Steam Browser
All Rights Reserved

SOFTWARE LICENSE AGREEMENT

This software is protected under international
copyright laws and treaties. This software is
licensed, not sold. 

TERMS OF USE:
1. You may not modify, decompile, or reverse
   engineer this software.
2. You may not redistribute this software.
3. You may not use this software for any
   illegal purposes.

This application is not affiliated with, endorsed by,
or sponsored by Valve Corporation. Steam and the
Steam logo are trademarks of Valve Corporation.

This software uses the following open-source components:
- CustomTkinter (MIT License)
- Requests (Apache 2.0 License)

Created with ♥ by the Crymson Team
Build ID: {hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:8]}
        """
        
        copyright_box = ctk.CTkTextbox(
            self.popup,
            width=400,
            height=350,
            font=("Segoe UI", 12),
            fg_color=self.colors["light_grey"],
            text_color=self.colors["text_grey"],
            border_width=1,
            border_color=self.colors["accent"]
        )
        copyright_box.pack(padx=20, pady=10)
        copyright_box.insert("1.0", copyright_text)
        copyright_box.configure(state="disabled")
        
        close_btn = ctk.CTkButton(
            self.popup,
            text="Close",
            command=self.popup.destroy,
            fg_color=self.colors["accent"],
            hover_color="#FF0F3D",
            font=("Segoe UI", 12, "bold"),
            height=35,
            corner_radius=10
        )
        close_btn.pack(pady=20)

class GameInfoPopup:
    def __init__(self, parent, game_data, details_data):
        self.popup = ctk.CTkToplevel(parent)
        self.popup.title(game_data["name"])
        self.popup.geometry("900x700")
        self.popup.transient(parent)
        self.popup.grab_set()
        
        self.colors = {
            "crimson": "#DC143C",
            "dark_grey": "#1A1A1A",
            "light_grey": "#2D2D2D",
            "text_grey": "#E6E6E6",
            "accent": "#FF1F4D"
        }
        
        self.popup.configure(fg_color=self.colors["dark_grey"])
        
        self.main_container = ctk.CTkScrollableFrame(self.popup)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.title_label = ctk.CTkLabel(
            self.main_container,
            text=game_data["name"],
            font=("Segoe UI", 28, "bold"),
            text_color=self.colors["accent"]
        )
        self.title_label.pack(pady=(0, 20))
        
        header_url = details_data.get("header_image", "")
        if header_url:
            html_frame = tk.Frame(self.main_container, bg=self.colors["dark_grey"])
            html_frame.pack(fill="x", pady=(0, 20))
            
            webview = tk.Label(
                html_frame,
                text="[Game Image]",
                bg=self.colors["dark_grey"],
                fg=self.colors["text_grey"]
            )
            webview.pack(pady=10)
            
            view_image_btn = ctk.CTkButton(
                html_frame,
                text="View Full Size Image",
                command=lambda: webbrowser.open(header_url),
                fg_color=self.colors["accent"],
                hover_color="#FF0F3D"
            )
            view_image_btn.pack(pady=(0, 10))
        
        self.create_info_section("About", details_data.get("short_description", "No description available."))
        
        price = game_data.get("price", {}).get("final", 0) / 100
        price_text = f"${price:.2f}" if price > 0 else "Free"
        release_date = details_data.get("release_date", {}).get("date", "N/A")
        self.create_info_section("Release & Price", f"Price: {price_text}\nRelease Date: {release_date}")
        
        dev_pub_info = (
            f"Developers: {', '.join(details_data.get('developers', ['N/A']))}\n"
            f"Publishers: {', '.join(details_data.get('publishers', ['N/A']))}"
        )
        self.create_info_section("Development", dev_pub_info)
        
        screenshots = details_data.get("screenshots", [])
        if screenshots:
            self.create_section_title("Screenshots")
            screenshots_frame = ctk.CTkFrame(self.main_container)
            screenshots_frame.pack(fill="x", pady=(0, 20))
            
            for i, screenshot in enumerate(screenshots[:4]):
                screenshot_label = ctk.CTkLabel(
                    screenshots_frame,
                    text=f"[Screenshot {i+1}]",
                    text_color=self.colors["text_grey"]
                )
                screenshot_label.pack(pady=5)
                
                view_btn = ctk.CTkButton(
                    screenshots_frame,
                    text=f"View Screenshot {i+1}",
                    command=lambda url=screenshot["path"]: webbrowser.open(url),
                    fg_color=self.colors["accent"],
                    hover_color="#FF0F3D"
                )
                view_btn.pack(pady=(0, 10))
        
        categories = ", ".join(cat["description"] for cat in details_data.get("categories", []))
        genres = ", ".join(genre["description"] for genre in details_data.get("genres", []))
        self.create_info_section("Categories & Genres", f"Categories:\n{categories}\n\nGenres:\n{genres}")
        
        if "pc_requirements" in details_data:
            req_text = details_data["pc_requirements"].get("minimum", "Not specified")
            self.create_info_section("System Requirements", req_text)
        
        buttons_frame = ctk.CTkFrame(self.main_container)
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        store_btn = ctk.CTkButton(
            buttons_frame,
            text="View on Steam",
            command=lambda: webbrowser.open(f"https://store.steampowered.com/app/{game_data['id']}"),
            fg_color=self.colors["accent"],
            hover_color="#FF0F3D"
        )
        store_btn.pack(side="left", padx=5)
        
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="Close",
            command=self.popup.destroy,
            fg_color=self.colors["light_grey"],
            hover_color="#303030"
        )
        close_btn.pack(side="right", padx=5)
    
    def create_section_title(self, title):
        title_label = ctk.CTkLabel(
            self.main_container,
            text=title,
            font=("Segoe UI", 18, "bold"),
            text_color=self.colors["accent"]
        )
        title_label.pack(pady=(20, 5), anchor="w")
    
    def create_info_section(self, title, content):
        self.create_section_title(title)
        
        content_box = ctk.CTkTextbox(
            self.main_container,
            height=100,
            wrap="word",
            font=("Segoe UI", 12)
        )
        content_box.pack(fill="x", pady=(0, 10))
        content_box.insert("1.0", content)
        content_box.configure(state="disabled")

class SteamLookup:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Crymson")
        self.app.geometry("1200x800")
        
        self.colors = {
            "crimson": "#DC143C",
            "dark_grey": "#1A1A1A",
            "light_grey": "#2D2D2D",
            "text_grey": "#E6E6E6",
            "accent": "#FF1F4D"
        }
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.current_page = 1
        self.items_per_page = 50
        self.total_results = 0
        self.current_games = []
        self.transition_active = False
        
        self.setup_gui()
    
    def setup_gui(self):
        self.app.configure(fg_color=self.colors["dark_grey"])
        
        menu_frame = ctk.CTkFrame(self.app, fg_color=self.colors["light_grey"])
        menu_frame.pack(fill="x", padx=10, pady=5)
        
        title_label = ctk.CTkLabel(
            menu_frame,
            text="CRYMSON",
            font=("Segoe UI", 16, "bold"),
            text_color=self.colors["accent"]
        )
        title_label.pack(side="left", padx=10)
        
        about_button = ctk.CTkButton(
            menu_frame,
            text="About",
            width=80,
            command=self.show_about,
            fg_color=self.colors["light_grey"],
            hover_color="#303030"
        )
        about_button.pack(side="right", padx=5)
        
        self.main_container = ctk.CTkFrame(self.app)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.search_frame = ctk.CTkFrame(self.main_container)
        self.search_frame.pack(fill="x", padx=10, pady=10)
        
        self.search_entry = ctk.CTkEntry(self.search_frame, 
                                       placeholder_text="Enter game name (leave empty to browse all)...",
                                       width=400)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_game())
        
        self.search_button = ctk.CTkButton(self.search_frame, 
                                         text="Search",
                                         command=self.search_game)
        self.search_button.pack(side="left", padx=5)
        
        self.results_container = ctk.CTkFrame(self.main_container)
        self.results_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.games_frame = ctk.CTkScrollableFrame(self.results_container, width=300)
        self.games_frame.pack(side="left", fill="y", padx=5)
        
        self.details_frame = ctk.CTkFrame(self.results_container)
        self.details_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        self.title_frame = ctk.CTkFrame(self.details_frame)
        self.title_frame.pack(fill="x", padx=10, pady=5)
        
        self.game_title = ctk.CTkLabel(self.title_frame, 
                                     text="Select a game to view details",
                                     font=("Segoe UI", 24, "bold"))
        self.game_title.pack(side="left", pady=10)
        
        self.app_id_label = ctk.CTkLabel(self.title_frame,
                                        text="",
                                        font=("Segoe UI", 16))
        self.app_id_label.pack(side="right", pady=10)
        
        self.game_details = ctk.CTkTextbox(self.details_frame, 
                                         width=600, 
                                         height=500,
                                         font=("Segoe UI", 12))
        self.game_details.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.buttons_frame = ctk.CTkFrame(self.details_frame)
        self.buttons_frame.pack(fill="x", padx=10, pady=5)
        
        self.store_button = ctk.CTkButton(self.buttons_frame,
                                        text="Open Store Page",
                                        command=self.open_store_page)
        self.store_button.pack(side="left", padx=5)
        self.store_button.pack_forget()
        
        self.nav_frame = ctk.CTkFrame(self.main_container)
        self.nav_frame.pack(fill="x", padx=10, pady=10)
        
        self.prev_button = ctk.CTkButton(self.nav_frame,
                                       text="Previous",
                                       command=self.prev_page)
        self.prev_button.pack(side="left", padx=5)
        
        self.page_label = ctk.CTkLabel(self.nav_frame,
                                     text="Page 1",
                                     font=("Segoe UI", 12))
        self.page_label.pack(side="left", padx=20)
        
        self.next_button = ctk.CTkButton(self.nav_frame,
                                       text="Next",
                                       command=self.next_page)
        self.next_button.pack(side="left", padx=5)
        
        self.theme_button = ctk.CTkButton(self.main_container,
                                        text="Toggle Theme",
                                        command=self.toggle_theme)
        self.theme_button.pack(pady=10)
        
        self.current_store_url = None
        
        self.game_title.configure(text_color=self.colors["accent"])
        self.app_id_label.configure(text_color=self.colors["text_grey"])
        self.game_details.configure(fg_color=self.colors["light_grey"],
                                  text_color=self.colors["text_grey"])
        
        button_style = {
            "fg_color": self.colors["accent"],
            "hover_color": "#FF0F3D",
            "text_color": "white"
        }
        
        self.search_button.configure(**button_style)
        self.store_button.configure(**button_style)
        self.prev_button.configure(**button_style)
        self.next_button.configure(**button_style)
        self.theme_button.configure(**button_style)
        
        self.search_game()
    
    def fade_text(self, widget, new_text):
        if isinstance(widget, ctk.CTkLabel):
            for alpha in range(100, 0, -10):
                widget.configure(text_color=f"gray{alpha}")
                self.app.update()
                time.sleep(0.01)
            
            widget.configure(text=new_text)
            
            for alpha in range(0, 100, 10):
                widget.configure(text_color=f"gray{alpha}")
                self.app.update()
                time.sleep(0.01)
        else:
            widget.configure(state="normal")
            for alpha in range(100, 0, -10):
                widget.configure(text_color=f"gray{alpha}")
                self.app.update()
                time.sleep(0.01)
            
            widget.delete("1.0", "end")
            widget.insert("1.0", new_text)
            
            for alpha in range(0, 100, 10):
                widget.configure(text_color=f"gray{alpha}")
                self.app.update()
                time.sleep(0.01)
    
    def create_ascii_box(self, text, width=60, style="single"):
        lines = text.split('\n')
        
        if style == "double":
            box_chars = {
                "top_left": "╔", "top_right": "╗", "bottom_left": "╚", "bottom_right": "╝",
                "horizontal": "═", "vertical": "║"
            }
        else:
            box_chars = {
                "top_left": "┌", "top_right": "┐", "bottom_left": "└", "bottom_right": "┘",
                "horizontal": "─", "vertical": "│"
            }
        
        box_top = (f"{box_chars['top_left']}"
                  f"{box_chars['horizontal'] * (width + 2)}"
                  f"{box_chars['top_right']}")
        
        box_bottom = (f"{box_chars['bottom_left']}"
                     f"{box_chars['horizontal'] * (width + 2)}"
                     f"{box_chars['bottom_right']}")
        
        box_content = []
        for line in lines:
            if line.strip():
                while len(line) > width:
                    split_at = line[:width].rfind(' ')
                    if split_at == -1:
                        split_at = width
                    box_content.append(f"{box_chars['vertical']} {line[:split_at].ljust(width)} {box_chars['vertical']}")
                    line = line[split_at:].strip()
                box_content.append(f"{box_chars['vertical']} {line.ljust(width)} {box_chars['vertical']}")
            else:
                box_content.append(f"{box_chars['vertical']} {' ' * width} {box_chars['vertical']}")
        
        return "\n".join([box_top] + box_content + [box_bottom])
    
    def search_game(self):
        self.current_page = 1
        self.fetch_games()
    
    def fetch_games(self):
        query = self.search_entry.get()
        
        for widget in self.games_frame.winfo_children():
            widget.destroy()
        
        try:
            search_url = "https://store.steampowered.com/api/storesearch"
            params = {
                "term": query,
                "l": "english",
                "cc": "US",
                "page": self.current_page,
                "count": self.items_per_page
            }
            
            response = requests.get(search_url, params=params)
            data = response.json()
            
            self.total_results = data.get("total", 0)
            self.current_games = data.get("items", [])
            
            if self.current_games:
                self.display_games_list()
                self.update_navigation()
            else:
                self.display_error("No games found!")
        except Exception as e:
            self.display_error(f"Error: {str(e)}")
    
    def display_games_list(self):
        for game in self.current_games:
            game_frame = ctk.CTkFrame(self.games_frame)
            game_frame.pack(fill="x", padx=5, pady=2)
            
            name = game.get("name", "Unknown Game")
            price = game.get("price", {}).get("final", 0) / 100
            price_text = f"${price:.2f}" if price > 0 else "Free"
            
            button_frame = ctk.CTkFrame(game_frame)
            button_frame.pack(fill="x", padx=5, pady=2)
            
            game_button = ctk.CTkButton(
                button_frame,
                text=f"{name} - {price_text}",
                command=lambda g=game: self.show_game_details(g),
                fg_color=self.colors["accent"],
                hover_color="#FF0F3D"
            )
            game_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            info_button = ctk.CTkButton(
                button_frame,
                text="ℹ",
                width=30,
                command=lambda g=game: self.show_game_popup(g),
                fg_color=self.colors["light_grey"],
                hover_color="#303030"
            )
            info_button.pack(side="right")
    
    def show_game_details(self, game):
        if self.transition_active:
            return
        
        self.transition_active = True
        threading.Thread(target=self._show_game_details_with_transition, args=(game,)).start()
    
    def _show_game_details_with_transition(self, game):
        self.app.after(0, lambda: self.fade_text(self.game_title, game["name"]))
        self.app.after(0, lambda: self.fade_text(self.app_id_label, f"App ID: {game['id']}"))
        
        try:
            app_id = game['id']
            details_url = f"https://store.steampowered.com/api/appdetails"
            params = {
                "appids": app_id,
                "cc": "US",
                "l": "english"
            }
            response = requests.get(details_url, params=params)
            details = response.json()[str(app_id)]['data']
            
            price_box = self.create_ascii_box(f"""
Price: ${game.get('price', {}).get('final', 0)/100:.2f}
Release Date: {details.get('release_date', {}).get('date', 'N/A')}
""", style="double")
            
            dev_box = self.create_ascii_box(f"""
Developers: {', '.join(details.get('developers', ['N/A']))}
Publishers: {', '.join(details.get('publishers', ['N/A']))}
""")
            
            desc_box = self.create_ascii_box(f"""
Description:
{details.get('short_description', 'No description available.')}
""", style="double")
            
            categories_box = self.create_ascii_box(f"""
Categories:
{', '.join(cat['description'] for cat in details.get('categories', []))}
""")
            
            genres_box = self.create_ascii_box(f"""
Genres:
{', '.join(genre['description'] for genre in details.get('genres', []))}
""", style="double")
            
            tags_box = self.create_ascii_box(f"""
Tags:
{', '.join(tag['description'] for tag in details.get('categories', [])[:5])}
""")
            
            info_text = "\n\n".join([
                price_box,
                dev_box,
                desc_box,
                categories_box,
                genres_box,
                tags_box
            ])
            
            self.app.after(0, lambda: self.fade_text(self.game_details, info_text))
            
        except Exception as e:
            info_text = self.create_ascii_box(f"""
App ID: {game['id']}
Price: ${game.get('price', {}).get('final', 0)/100:.2f}
Release Date: {game.get('release_date', {}).get('date', 'N/A')}
""", style="double")
            self.app.after(0, lambda: self.fade_text(self.game_details, info_text))
        
        self.current_store_url = f"https://store.steampowered.com/app/{game['id']}"
        self.app.after(0, self.store_button.pack, {"side": "left", "padx": 5})
        self.transition_active = False
    
    def show_game_popup(self, game):
        try:
            app_id = game['id']
            details_url = f"https://store.steampowered.com/api/appdetails"
            params = {
                "appids": app_id,
                "cc": "US",
                "l": "english"
            }
            response = requests.get(details_url, params=params)
            details = response.json()[str(app_id)]['data']
            
            GameInfoPopup(self.app, game, details)
            
        except Exception as e:
            self.display_error(f"Error loading game details: {str(e)}")
    
    def update_navigation(self):
        total_pages = (self.total_results + self.items_per_page - 1) // self.items_per_page
        self.page_label.configure(text=f"Page {self.current_page} of {total_pages}")
        
        self.prev_button.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_button.configure(state="normal" if self.current_page < total_pages else "disabled")
    
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.fetch_games()
    
    def next_page(self):
        self.current_page += 1
        self.fetch_games()
    
    def display_error(self, message):
        self.game_title.configure(text="Error")
        self.app_id_label.configure(text="")
        self.game_details.delete("1.0", "end")
        self.game_details.insert("1.0", self.create_ascii_box(message))
        self.store_button.pack_forget()
    
    def open_store_page(self):
        if self.current_store_url:
            webbrowser.open(self.current_store_url)
    
    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
    
    def show_about(self):
        AboutWindow(self.app)
    
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = SteamLookup()
    app.run() 