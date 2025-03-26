import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timedelta
import calendar

class ModernClockCalendar:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("iOS Clock & Calendar")
        self.root.geometry("400x600")
        self.root.configure(bg='#FFFFFF')
        
        # Configure style for iOS-like appearance
        self.style = ttk.Style()
        self.style.configure('iOS.TLabel', 
                           background='#FFFFFF',
                           foreground='#000000',
                           font=('SF Pro Display', 48))
        
        self.style.configure('iOS.TFrame', background='#FFFFFF')
        
        # Create main container
        self.container = ttk.Frame(self.root, style='iOS.TFrame')
        self.container.pack(expand=True, fill='both')
        
        # Clock display
        self.time_label = ttk.Label(self.container, 
                                  style='iOS.TLabel', 
                                  anchor='center')
        self.time_label.pack(pady=20)
        
        # Date display
        self.style.configure('Date.TLabel', 
                           background='#FFFFFF',
                           foreground='#FF9F0A',
                           font=('SF Pro Display', 20))
        self.date_label = ttk.Label(self.container, 
                                  style='Date.TLabel', 
                                  anchor='center')
        self.date_label.pack(pady=10)
        
        # Calendar widget
        self.cal_frame = ttk.Frame(self.container, style='iOS.TFrame')
        self.cal_frame.pack(pady=20, padx=20)
        
        # Configure calendar styles
        self.style.configure('Cal.TButton', 
                           background='#F2F2F7',
                           foreground='#000000',
                           font=('SF Pro Display', 12))
        
        # Add month navigation frame
        self.nav_frame = ttk.Frame(self.container, style='iOS.TFrame')
        self.nav_frame.pack(pady=5)
        
        # Configure navigation button style
        self.style.configure('Nav.TButton',
                           background='#FFFFFF',
                           foreground='#FF9F0A',
                           font=('SF Pro Display', 12, 'bold'),
                           padding=5)
        
        # Add navigation buttons and month label
        self.prev_button = ttk.Button(self.nav_frame,
                                    text="<",
                                    style='Nav.TButton',
                                    command=self.prev_month)
        self.prev_button.pack(side='left', padx=10)
        
        self.month_label = ttk.Label(self.nav_frame,
                                   style='Date.TLabel',
                                   anchor='center')
        self.month_label.pack(side='left', padx=20)
        
        self.next_button = ttk.Button(self.nav_frame,
                                    text=">",
                                    style='Nav.TButton',
                                    command=self.next_month)
        self.next_button.pack(side='left', padx=10)
        
        # Add current date tracking
        self.current_date = datetime.now()
        self.displayed_date = self.current_date
        
        self.create_calendar()
        self.update_clock()
        
    def prev_month(self):
        # Move to previous month
        if self.displayed_date.month == 1:
            self.displayed_date = self.displayed_date.replace(year=self.displayed_date.year-1, month=12)
        else:
            self.displayed_date = self.displayed_date.replace(month=self.displayed_date.month-1)
        self.update_calendar()
    
    def next_month(self):
        # Move to next month
        if self.displayed_date.month == 12:
            self.displayed_date = self.displayed_date.replace(year=self.displayed_date.year+1, month=1)
        else:
            self.displayed_date = self.displayed_date.replace(month=self.displayed_date.month+1)
        self.update_calendar()
    
    def update_calendar(self):
        # Clear existing calendar
        for widget in self.cal_frame.winfo_children():
            widget.destroy()
        self.create_calendar()
    
    def create_calendar(self):
        # Update month label
        month_year = self.displayed_date.strftime('%B %Y')
        if hasattr(self, 'month_label'):
            self.month_label.config(text=month_year)
        
        # Get calendar for displayed month
        cal = calendar.monthcalendar(self.displayed_date.year, self.displayed_date.month)
        
        # Day headers with improved styling
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            self.style.configure('DayHeader.TLabel',
                               background='#FFFFFF',
                               foreground='#FF9F0A',
                               font=('SF Pro Display', 14, 'bold'))
            label = ttk.Label(self.cal_frame,
                            text=day,
                            style='DayHeader.TLabel')
            label.grid(row=0, column=i, pady=10, padx=5)
        
        # Calendar days with improved layout
        current_date = datetime.now()
        for week_num, week in enumerate(cal, 1):
            for day_num, day in enumerate(week):
                if day != 0:
                    btn = ttk.Button(self.cal_frame,
                                   text=str(day),
                                   style='Cal.TButton')
                    
                    # Highlight current day only if we're in current month and year
                    if (day == current_date.day and 
                        self.displayed_date.month == current_date.month and 
                        self.displayed_date.year == current_date.year):
                        btn.configure(style='Current.TButton')
                    
                    btn.grid(row=week_num,
                            column=day_num,
                            padx=3,
                            pady=3,
                            sticky='nsew')
                else:
                    # Empty button for days not in month
                    btn = ttk.Button(self.cal_frame,
                                   text="",
                                   style='Cal.TButton',
                                   state='disabled')
                    btn.grid(row=week_num,
                            column=day_num,
                            padx=3,
                            pady=3,
                            sticky='nsew')
        
        # Make grid cells expand uniformly
        for i in range(7):
            self.cal_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.cal_frame.grid_rowconfigure(i, weight=1)
    
    def update_clock(self):
        # Update time
        current_time = time.strftime('%H:%M:%S')
        self.time_label.config(text=current_time)
        
        # Update date
        current_date = datetime.now().strftime('%B %d, %Y')
        self.date_label.config(text=current_date)
        
        # Schedule next update
        self.root.after(1000, self.update_clock)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernClockCalendar()
    app.run()
