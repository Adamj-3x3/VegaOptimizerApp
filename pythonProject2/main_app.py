import customtkinter as ctk
import threading
import time # For simulation of analysis time
from PIL import Image, ImageTk, ImageFilter
import tkinter as tk
import os
import sys
# Import the real analysis engine
from analysis_engine import run_bullish_analysis, run_bearish_analysis

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# --- Color Palette (matching logo) ---
BG_DARK = "#10131a"         # Deep navy/black background
ACCENT_BLUE = "#1fa2ff"     # Blue gradient from logo
ACCENT_GREEN = "#23d160"    # Green gradient from logo
TEXT_WHITE = "#ffffff"
TEXT_GRAY = "#bfc9d1"

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller .exe
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class GradientBackground(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        # Blue-green flowing gradient
        for i in range(h):
            r = int(16 + (31-16)*i/h)
            g = int(19 + (162-19)*i/h)
            b = int(26 + (255-26)*i/h)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.create_line(0, i, w, i, fill=color)
        # Faint "VE" watermark
        self.create_text(w//2, h//2, text="VE", font=("Segoe UI", int(h*0.25), "bold"), fill="#ffffff10")
        # Optional: flowing wave (abstract)
        self.create_arc(-w//2, h//2, w*1.5, h*1.5, start=0, extent=180, fill="#23d16022", outline="")

# --- Live Analysis Engine Function ---
def live_analysis_engine_run(ticker, min_dte, max_dte, strategy_type):
    """
    The real analysis engine function that calls your live analysis code.
    """
    print(f"Running analysis: {ticker}, {min_dte}, {max_dte}, {strategy_type}")
    try:
        if strategy_type == "Bullish":
            result_text = run_bullish_analysis(ticker, min_dte, max_dte)
        else:  # Bearish
            result_text = run_bearish_analysis(ticker, min_dte, max_dte)
        print("Result text:", result_text)
        sections = parse_analysis_result(result_text)
        print("Parsed sections:", sections)
        return sections
    except Exception as e:
        print("Error in analysis:", e)
        return {
            "summary": f"Analysis Error: {str(e)}",
            "risk": "",
            "pricing_comparison": "",
            "top_5": []
        }

def parse_analysis_result(result_text):
    """
    Parse the analysis result text into structured data for the UI.
    """
    lines = result_text.split('\n')
    
    summary_lines = []
    risk_lines = []
    pricing_lines = []
    top_5_data = []
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect sections
        if "TOP RECOMMENDED TRADE" in line.upper():
            current_section = "summary"
            continue
        elif "STRATEGY OVERVIEW" in line.upper() or "RISK" in line.upper():
            current_section = "risk"
            continue
        elif "PRICING COMPARISON" in line.upper():
            current_section = "pricing"
            continue
        elif "TOP 5 COMBINATIONS" in line.upper():
            current_section = "top5"
            continue
        elif "No valid strategies found" in line:
            return {
                "summary": "No valid strategies found for these parameters.",
                "risk": "",
                "pricing_comparison": "",
                "top_5": []
            }
        
        # Add lines to appropriate section
        if current_section == "summary":
            summary_lines.append(line)
        elif current_section == "risk":
            risk_lines.append(line)
        elif current_section == "pricing":
            pricing_lines.append(line)
        elif current_section == "top5":
            # Parse table data, skip header and separator lines
            if "|" in line and not line.startswith("---"):
                # Skip the header row
                if "RANK" in line.upper() and "EXPIRATION" in line.upper():
                    continue
                parts = [part.strip() for part in line.split("|") if part.strip()]
                if len(parts) >= 7:
                    top_5_data.append(tuple(parts[:7]))  # Rank, Expiration, Strikes, Net Cost, Net Vega, Efficiency, Score
    
    return {
        "summary": "\n".join(summary_lines),
        "risk": "\n".join(risk_lines),
        "pricing_comparison": "\n".join(pricing_lines),
        "top_5": top_5_data
    }

# --- Placeholder for your analysis_engine.py functions ---
# In a real scenario, you would import them like:
# from analysis_engine import analyze_bullish_risk_reversal, analyze_bearish_risk_reversal, format_text_report
# For this skeleton, we'll use a dummy function.

def dummy_analysis_engine_run(ticker, min_dte, max_dte, strategy_type):
    """
    A placeholder function to simulate your analysis_engine.
    In your actual app, this would call your real analysis functions.
    It returns a dictionary structure that can be parsed by display_results.
    """
    time.sleep(2) # Simulate work

    # --- SIMULATED REPORT DATA ---
    # This structure mimics the kind of parsed data you'd get from your
    # analysis_engine.format_text_report()
    # You will need to adapt your parsing logic to produce a similar dict.

    if strategy_type == "Bullish" and ticker == "SRPT":
        summary_text = """
Expiration: 2025-11-21 (151 days)
Strikes: Long Call: $22.50, Short Put: $17.50
Net Cost: $0.20 DEBIT
Breakeven: $22.70
Net Vega: 0.005
Efficiency: -4.0%
"""
        risk_text = """
STRATEGY OVERVIEW & RISK
A Bullish Risk Reversal (Long OTM Call, Short OTM Put) creates a synthetic long stock position with low or zero cost.
The primary risk is the short put. If the stock price falls below $17.50, you may be assigned
100 shares per contract at that price. Maximum loss is up to $17.70 per share if the stock goes to zero.
"""
        pricing_text = """
PRICING COMPARISON (For debugging Robinhood discrepancy)
Current Method (Worst-case): $0.20 DEBIT
Mid-Price Method (Robinhood likely): $-0.10 CREDIT
Bid-Ask Spread: Call:$0.40, Put:$0.30, Total=$0.60
"""
        top_5_data = [
            ("1", "2025-11-21", "$22.50/$17.50", "$0.20 DB", "0.005", "-4.0%", "0.973"),
            ("2", "2026-01-16", "$25.00/$17.50", "$0.30 DB", "0.007", "-8.0%", "0.664"),
            ("3", "2025-11-21", "$25.00/$17.50", "$0.40 CR", "0.005", "5.3%", "0.658"),
            ("4", "2026-02-20", "$22.50/$17.50", "$1.20 DB", "0.006", "-24.0%", "0.639"),
            ("5", "2025-06-20", "$30.00/$17.50", "$0.50 CR", "0.007", "4.0%", "0.634")
        ]
        return {
            "summary": summary_text.strip(),
            "risk": risk_text.strip(),
            "pricing_comparison": pricing_text.strip(),
            "top_5": top_5_data
        }
    else:
        return {
            "summary": "No valid strategies found for these parameters.",
            "risk": "",
            "pricing_comparison": "",
            "top_5": []
        }
# --- End of Placeholder ---

class OptionAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VegaEdge - Option Strategy Analyzer")
        self.geometry("1400x900")  # Wider default window
        self.minsize(1200, 800)
        self.configure(bg=BG_DARK)
        # --- Gradient background ---
        self.bg_canvas = GradientBackground(self, highlightthickness=0, bg=BG_DARK)
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        # --- Main content frame (transparent) ---
        self.content = tk.Frame(self, highlightthickness=0, bg=BG_DARK)
        self.content.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.create_widgets()
        self.setup_layout()
        self.analysis_thread = None

    def create_widgets(self):
        # --- Ribbon/Header ---
        self.ribbon = ctk.CTkFrame(self.content, fg_color="#181d26", corner_radius=0, height=90)
        self.ribbon.pack_propagate(False)
        # Logo (smaller, left-aligned)
        logo_path = resource_path("vegaedge_logo.png")
        logo_img = Image.open(logo_path).convert("RGBA")
        Resampling = getattr(Image, "Resampling", Image)
        resample_filter = getattr(Resampling, "LANCZOS", getattr(Resampling, "BICUBIC"))
        logo_img = logo_img.resize((60, 60), resample_filter)
        self.logo_ctk = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(60, 60))
        self.logo_label = ctk.CTkLabel(self.ribbon, image=self.logo_ctk, text="", bg_color="transparent")
        self.logo_label.pack(side="left", padx=(20, 10), pady=10)
        # App name
        self.app_name_label = ctk.CTkLabel(self.ribbon, text="VegaEdge - Option Strategy Analyzer", font=ctk.CTkFont(size=22, weight="bold"), text_color=ACCENT_BLUE, bg_color="transparent")
        self.app_name_label.pack(side="left", padx=(0, 30), pady=10)
        # Input fields and button in a row (right-aligned)
        self.ribbon_inputs = ctk.CTkFrame(self.ribbon, fg_color="transparent")
        self.ribbon_inputs.pack(side="right", padx=20, pady=10)
        label_font = ctk.CTkFont(size=16, weight="bold")
        entry_font = ctk.CTkFont(size=15)
        # Ticker
        ctk.CTkLabel(self.ribbon_inputs, text="Ticker:", font=label_font, text_color=TEXT_WHITE, bg_color="transparent").pack(side="left", padx=(0, 4))
        self.ticker_entry = ctk.CTkEntry(self.ribbon_inputs, width=80, placeholder_text="SRPT", font=entry_font, fg_color="#232b3a", text_color=TEXT_WHITE)
        self.ticker_entry.pack(side="left", padx=(0, 10))
        self.ticker_entry.insert(0, "SRPT")
        # Min DTE
        ctk.CTkLabel(self.ribbon_inputs, text="Min DTE:", font=label_font, text_color=TEXT_WHITE, bg_color="transparent").pack(side="left", padx=(0, 4))
        self.min_dte_entry = ctk.CTkEntry(self.ribbon_inputs, width=60, placeholder_text="100", font=entry_font, fg_color="#232b3a", text_color=TEXT_WHITE)
        self.min_dte_entry.pack(side="left", padx=(0, 10))
        self.min_dte_entry.insert(0, "100")
        # Max DTE
        ctk.CTkLabel(self.ribbon_inputs, text="Max DTE:", font=label_font, text_color=TEXT_WHITE, bg_color="transparent").pack(side="left", padx=(0, 4))
        self.max_dte_entry = ctk.CTkEntry(self.ribbon_inputs, width=60, placeholder_text="500", font=entry_font, fg_color="#232b3a", text_color=TEXT_WHITE)
        self.max_dte_entry.pack(side="left", padx=(0, 10))
        self.max_dte_entry.insert(0, "500")
        # Strategy
        ctk.CTkLabel(self.ribbon_inputs, text="Strategy:", font=label_font, text_color=TEXT_WHITE, bg_color="transparent").pack(side="left", padx=(0, 4))
        self.strategy_var = ctk.StringVar(value="Bullish")
        ctk.CTkRadioButton(self.ribbon_inputs, text="Bullish", variable=self.strategy_var, value="Bullish", font=entry_font, fg_color=ACCENT_GREEN, hover_color=ACCENT_BLUE, text_color=TEXT_WHITE, bg_color="transparent").pack(side="left", padx=(0, 2))
        ctk.CTkRadioButton(self.ribbon_inputs, text="Bearish", variable=self.strategy_var, value="Bearish", font=entry_font, fg_color=ACCENT_BLUE, hover_color=ACCENT_GREEN, text_color=TEXT_WHITE, bg_color="transparent").pack(side="left", padx=(0, 10))
        # Run Analysis button
        self.run_button = ctk.CTkButton(self.ribbon_inputs, text="Run Analysis", command=self.start_analysis, font=ctk.CTkFont(size=18, weight="bold"), height=40, width=140, fg_color=ACCENT_GREEN, hover_color=ACCENT_BLUE, text_color=TEXT_WHITE, corner_radius=12)
        self.run_button.pack(side="left", padx=(0, 0))
        # --- Error Message (below ribbon) ---
        self.error_var = ctk.StringVar(value="")
        self.error_label = ctk.CTkLabel(self.content, textvariable=self.error_var, text_color=ACCENT_GREEN, font=ctk.CTkFont(size=15, weight="bold"), bg_color="transparent")
        # --- Results Card (moved up) ---
        self.results_card = ctk.CTkFrame(self.content, fg_color="#181d26", corner_radius=30, border_width=2, border_color="#232b3a")
        self.tabview = ctk.CTkTabview(self.results_card, fg_color="transparent")
        self.tabview.pack(fill="both", expand=True, padx=30, pady=30)
        entry_font2 = ctk.CTkFont(size=16)
        self.summary_tab = self.tabview.add("Summary")
        self.top_trade_summary_text = ctk.CTkTextbox(self.summary_tab, height=200, fg_color="#232b3a", text_color=TEXT_WHITE, font=entry_font2)
        self.top_trade_summary_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.risk_tab = self.tabview.add("Risk Analysis")
        self.risk_overview_text = ctk.CTkTextbox(self.risk_tab, height=200, fg_color="#232b3a", text_color=TEXT_WHITE, font=entry_font2)
        self.risk_overview_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.pricing_tab = self.tabview.add("Pricing Comparison")
        self.pricing_comparison_text = ctk.CTkTextbox(self.pricing_tab, height=200, fg_color="#232b3a", text_color=TEXT_WHITE, font=entry_font2)
        self.pricing_comparison_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_tab = self.tabview.add("Top 5 Results")
        table_frame = ctk.CTkFrame(self.results_tab, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        headers = ["Rank", "Expiration", "Strikes", "Net Cost", "Net Vega", "Efficiency", "Score"]
        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=5)
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(header_frame, text=header, font=ctk.CTkFont(size=15, weight="bold"), text_color=ACCENT_GREEN if i==0 else ACCENT_BLUE if i==6 else TEXT_WHITE, width=120 if i < len(headers) - 1 else 80, bg_color="transparent")
            label.grid(row=0, column=i, padx=2, pady=5, sticky="ew")
            header_frame.grid_columnconfigure(i, weight=1)
        self.results_scrollable_frame = ctk.CTkScrollableFrame(table_frame, height=300, fg_color="#232b3a")
        self.results_scrollable_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.result_labels = []
        # --- Status Bar ---
        self.status_bar = ctk.CTkLabel(self.content, text="Ready", font=ctk.CTkFont(size=15), text_color=TEXT_GRAY, bg_color="transparent")

    def setup_layout(self):
        self.ribbon.pack(fill="x", pady=(0, 0))
        self.error_label.pack(pady=(0, 5))
        self.results_card.pack(fill="both", expand=True, padx=80, pady=(10, 20))
        self.status_bar.pack(side="bottom", fill="x", padx=20, pady=8)

    def update_status(self, message, is_error=False):
        if is_error:
            self.status_bar.configure(text=message, text_color=ACCENT_GREEN)
        else:
            self.status_bar.configure(text=message, text_color=TEXT_GRAY)
        self.status_bar.update_idletasks()

    def start_analysis(self):
        ticker = self.ticker_entry.get().strip().upper()
        min_dte = self.min_dte_entry.get().strip()
        max_dte = self.max_dte_entry.get().strip()
        strategy_type = self.strategy_var.get()
        if not ticker:
            self.update_status("Error: Ticker Symbol cannot be empty.", is_error=True)
            return
        try:
            min_dte = int(min_dte)
            max_dte = int(max_dte)
            if not (0 <= min_dte <= max_dte):
                raise ValueError("DTEs must be non-negative and Min DTE <= Max DTE.")
        except ValueError as e:
            self.update_status(f"Error: Invalid DTEs. {e}", is_error=True)
            return
        self.update_status("Analysis Running... Please wait.")
        self.run_button.configure(state="disabled")
        self.clear_results()
        self.analysis_thread = threading.Thread(target=self._run_analysis_thread, args=(ticker, min_dte, max_dte, strategy_type))
        self.analysis_thread.start()

    def _run_analysis_thread(self, ticker, min_dte, max_dte, strategy_type):
        try:
            # For debugging, you can swap the next line:
            # result_data = live_analysis_engine_run(ticker, min_dte, max_dte, strategy_type)
            # with this line to use the dummy engine:
            # result_data = dummy_analysis_engine_run(ticker, min_dte, max_dte, strategy_type)
            result_data = live_analysis_engine_run(ticker, min_dte, max_dte, strategy_type)
            self.after(0, self.display_results, result_data)
            self.after(0, self.update_status, "Analysis completed.")
        except Exception as e:
            self.after(0, lambda: self.update_status(f"Analysis Error: {e}", True))
        finally:
            self.after(0, lambda: self.run_button.configure(state="normal"))

    def clear_results(self):
        self.top_trade_summary_text.delete("0.0", "end")
        self.risk_overview_text.delete("0.0", "end")
        self.pricing_comparison_text.delete("0.0", "end")
        for label in self.result_labels:
            label.destroy()
        self.result_labels.clear()

    def display_results(self, result_data):
        self.top_trade_summary_text.delete("0.0", "end")
        self.risk_overview_text.delete("0.0", "end")
        self.pricing_comparison_text.delete("0.0", "end")
        for label in self.result_labels:
            label.destroy()
        self.result_labels.clear()

        self.top_trade_summary_text.insert("0.0", result_data.get("summary", ""))
        self.risk_overview_text.insert("0.0", result_data.get("risk", ""))
        self.pricing_comparison_text.insert("0.0", result_data.get("pricing_comparison", ""))

        # --- Top 15 Table ---
        all_results = result_data.get("top_5", [])[:15]
        top_5 = all_results[:5]
        next_10 = all_results[5:15]

        # Remove all widgets from the scrollable frame
        for widget in self.results_scrollable_frame.winfo_children():
            widget.destroy()

        # --- Margin Impact Row (IBKR RegT for Risk Reversal) ---
        margin_impact_text = "Margin Impact: N/A"
        margin_note = "(IBKR RegT est. for risk reversal: short call margin)"
        if top_5:
            try:
                # Extract strikes and prices from the top result
                strikes = top_5[0][2]  # e.g., "$25.00/$17.50"
                strike_parts = [float(s.replace("$", "").strip()) for s in strikes.split("/")]
                # Heuristic: higher strike is call, lower is put
                call_strike = max(strike_parts)
                put_strike = min(strike_parts)
                # Try to extract net cost (for premiums)
                # e.g., "$0.20 DB" or "$0.40 CR"
                net_cost_str = top_5[0][3].replace("$", "").replace("DB", "").replace("CR", "").strip()
                net_cost = float(net_cost_str) if net_cost_str else 0.0
                # For this estimate, assume call price = max(0, net_cost) if credit, else 0.0
                # (In reality, you'd want the actual call price, but we use net cost as a proxy)
                # If you have access to the actual call/put prices, use them here.
                # For now, we'll use 0 for both premiums (since they're not available in the table)
                call_price = 0.0
                put_price = 0.0
                # Underlying price: try to extract from summary
                import re
                summary = result_data.get("summary", "")
                underlying_price = None
                m = re.search(r"Breakeven: \$([0-9.]+)", summary)
                if m:
                    # Use breakeven as a proxy for underlying price if available
                    underlying_price = float(m.group(1))
                else:
                    # Fallback: use average of strikes
                    underlying_price = sum(strike_parts) / 2
                # OTM amount for call
                otm_call = max(0, call_strike - underlying_price)
                # IBKR RegT margin formula for short call
                margin_short_call = call_price * 100 + max(
                    (0.20 * underlying_price - otm_call) * 100,
                    0.10 * underlying_price * 100
                )
                margin_impact_text = f"Margin Impact: ${margin_short_call:,.2f} {margin_note}"
            except Exception:
                pass  # Leave as N/A if parsing fails
        margin_label = ctk.CTkLabel(self.results_scrollable_frame, text=margin_impact_text, font=ctk.CTkFont(size=15, weight="bold"), text_color=ACCENT_BLUE, bg_color="transparent")
        margin_label.pack(pady=(0, 8))
        self.result_labels.append(margin_label)

        # Top 5
        for rank, exp, strikes, cost, vega, eff, score in top_5:
            row_frame = ctk.CTkFrame(self.results_scrollable_frame, fg_color="#232b3a")
            row_frame.pack(fill="x", padx=5, pady=2)
            columns = [rank, exp, strikes, cost, vega, eff, score]
            for i, value in enumerate(columns):
                label = ctk.CTkLabel(row_frame, text=value, font=ctk.CTkFont(size=14), text_color=ACCENT_GREEN if i==0 else ACCENT_BLUE if i==6 else TEXT_WHITE, width=120 if i < len(columns) - 1 else 80, bg_color="transparent")
                label.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
                row_frame.grid_columnconfigure(i, weight=1)
                self.result_labels.append(label)

        # Spacer between tables if there are more than 5
        if next_10:
            spacer = ctk.CTkLabel(self.results_scrollable_frame, text="\nNext Best Results:", font=ctk.CTkFont(size=15, weight="bold"), text_color=ACCENT_BLUE, bg_color="transparent")
            spacer.pack(pady=(10, 2))
            # Table headers for next 10
            header_frame = ctk.CTkFrame(self.results_scrollable_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=5, pady=2)
            headers = ["Rank", "Expiration", "Strikes", "Net Cost", "Net Vega", "Efficiency", "Score"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(header_frame, text=header, font=ctk.CTkFont(size=13, weight="bold"), text_color=ACCENT_GREEN if i==0 else ACCENT_BLUE if i==6 else TEXT_WHITE, width=120 if i < len(headers) - 1 else 80, bg_color="transparent")
                label.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
                header_frame.grid_columnconfigure(i, weight=1)
                self.result_labels.append(label)
            # Next 10 (or up to 15 total)
            for rank, exp, strikes, cost, vega, eff, score in next_10:
                row_frame = ctk.CTkFrame(self.results_scrollable_frame, fg_color="#232b3a")
                row_frame.pack(fill="x", padx=5, pady=2)
                columns = [rank, exp, strikes, cost, vega, eff, score]
                for i, value in enumerate(columns):
                    label = ctk.CTkLabel(row_frame, text=value, font=ctk.CTkFont(size=13), text_color=ACCENT_GREEN if i==0 else ACCENT_BLUE if i==6 else TEXT_WHITE, width=120 if i < len(columns) - 1 else 80, bg_color="transparent")
                    label.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
                    row_frame.grid_columnconfigure(i, weight=1)
                    self.result_labels.append(label)

if __name__ == "__main__":
    app = OptionAnalyzerApp()
    app.mainloop()