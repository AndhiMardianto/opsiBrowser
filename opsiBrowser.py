import wx
import webbrowser
import os

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Buka URL atau Pencarian", size=(400, 200))
        
        # Atur posisi frame ke tengah layar
        self.Center()

        # Panel utama
        panel = wx.Panel(self)

        # Sizer untuk tata letak dinamis
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Label untuk instruksi
        label = wx.StaticText(panel, label="Masukkan URL atau kata kunci pencarian:")
        sizer.Add(label, flag=wx.EXPAND | wx.ALL, border=10)

        # Kotak input teks dengan dukungan Enter
        self.url_input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.url_input.Bind(wx.EVT_TEXT_ENTER, self.on_enter_press)
        sizer.Add(self.url_input, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Tombol untuk mencari
        search_button = wx.Button(panel, label="Cari")
        search_button.Bind(wx.EVT_BUTTON, self.on_search_click)
        sizer.Add(search_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Atur sizer ke panel
        panel.SetSizer(sizer)

    def handle_search(self):
        # Ambil input dari pengguna
        input_text = self.url_input.GetValue().strip()

        if not input_text:
            wx.MessageBox("Input tidak boleh kosong!", "Peringatan", wx.ICON_WARNING)
            return

        # Cek apakah input adalah URL
        if input_text.startswith("http://") or input_text.startswith("https://") or "." in input_text:
            # Anggap sebagai URL
            url = input_text
        else:
            # Anggap sebagai pencarian Google
            url = f"https://www.google.com/search?q={input_text.replace(' ', '+')}"

        # Deteksi browser yang tersedia
        available_browsers = self.get_available_browsers()

        if not available_browsers:
            wx.MessageBox("Tidak ada browser yang terdeteksi!", "Peringatan", wx.ICON_WARNING)
            return

        # Pilihan browser
        dialog = wx.SingleChoiceDialog(None, "Pilih browser:", "Browser Options", available_browsers)

        if dialog.ShowModal() == wx.ID_OK:
            choice = dialog.GetStringSelection()

            # Buka URL di browser yang dipilih
            webbrowser.get(choice.lower()).open(url)

        dialog.Destroy()
        self.Close()  # Tutup aplikasi setelah pencarian selesai

    def get_available_browsers(self):
        """
        Mendapatkan daftar browser yang tersedia di sistem.
        """
        # Daftar nama browser yang umum
        common_browsers = ["chrome", "firefox", "edge", "safari", "opera", "default"]
        
        # Memeriksa apakah browser tersedia menggunakan webbrowser.get()
        available_browsers = []
        
        # Daftarkan browser secara eksplisit jika belum terdeteksi
        if self.is_browser_installed("chrome"):
            webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(self.get_browser_path("chrome")))
            available_browsers.append("Chrome")
        if self.is_browser_installed("firefox"):
            webbrowser.register("firefox", None, webbrowser.BackgroundBrowser(self.get_browser_path("firefox")))
            available_browsers.append("Firefox")
        if self.is_browser_installed("edge"):
            webbrowser.register("edge", None, webbrowser.BackgroundBrowser(self.get_browser_path("edge")))
            available_browsers.append("Edge")

        return available_browsers

    def is_browser_installed(self, browser_name):
        """Memeriksa apakah browser terinstal di sistem."""
        return os.path.exists(self.get_browser_path(browser_name))

    def get_browser_path(self, browser_name):
        """Mengembalikan jalur browser berdasarkan nama browser."""
        browser_paths = {
            "chrome": "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
            "firefox": "C:/Program Files/Mozilla Firefox/firefox.exe",
            "edge": "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
        }
        return browser_paths.get(browser_name, "")

    def on_search_click(self, event):
        self.handle_search()

    def on_enter_press(self, event):
        self.handle_search()

# Jalankan aplikasi
if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
