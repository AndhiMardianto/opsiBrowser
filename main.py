import wx
import webbrowser

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Buka URL atau Pencarian", size=(400, 200))

        # Panel utama
        panel = wx.Panel(self)

        # Label untuk instruksi
        label = wx.StaticText(panel, label="Masukkan URL atau kata kunci pencarian:", pos=(20, 20))

        # Kotak input teks
        self.url_input = wx.TextCtrl(panel, pos=(20, 50), size=(250, -1))

        # Tombol untuk mencari
        search_button = wx.Button(panel, label="Cari", pos=(280, 50))
        search_button.Bind(wx.EVT_BUTTON, self.on_search_click)

        # Daftarkan browser dengan jalur manual
        self.register_browsers()

    def register_browsers(self):
        # Ganti dengan path browser yang sesuai
        webbrowser.register("chrome", None, webbrowser.BackgroundBrowser("c:\Program Files (x86)\Google\Chrome\Application\chrome.exe"))
        webbrowser.register("firefox", None, webbrowser.BackgroundBrowser("c:/Program Files/Mozilla Firefox/firefox.exe"))
        webbrowser.register("edge", None, webbrowser.BackgroundBrowser("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"))

    def on_search_click(self, event):
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

        # Pilihan browser
        browser_choices = ["Chrome", "Firefox", "Edge"]
        dialog = wx.SingleChoiceDialog(None, "Pilih browser:", "Browser Options", browser_choices)

        if dialog.ShowModal() == wx.ID_OK:
            choice = dialog.GetStringSelection()

            # Buka URL di browser yang dipilih
            if choice == "Chrome":
                webbrowser.get("chrome").open(url)
            elif choice == "Firefox":
                webbrowser.get("firefox").open(url)
            elif choice == "Edge":
                webbrowser.get("edge").open(url)

        dialog.Destroy()
        self.Close()  # Tutup aplikasi setelah pencarian selesai

# Jalankan aplikasi
if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
