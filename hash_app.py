import sys
import os
import hashlib
import datetime
import cv2
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                             QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, 
                             QAbstractItemView, QLabel, QStatusBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QColor, QBrush
from tinytag import TinyTag

# --- SIRALAMA İÇİN ÖZEL HÜCRE ---
class NumericTableWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            return float(self.text().split()[0]) < float(other.text().split()[0])
        except ValueError:
            return super().__lt__(other)

# --- ARKA PLAN İŞÇİSİ ---
class AnalysisWorker(QThread):
    finished_signal = pyqtSignal(int, int, str)

    def __init__(self, file_path, row_index):
        super().__init__()
        self.file_path = file_path
        self.row_index = row_index

    def run(self):
        # 1. MD5
        md5_val = self.calculate_md5()
        self.finished_signal.emit(self.row_index, 4, md5_val)
        # 2. SÜRE
        duration_val = self.calculate_duration()
        self.finished_signal.emit(self.row_index, 1, duration_val)

    def calculate_md5(self):
        hash_md5 = hashlib.md5()
        try:
            with open(self.file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except: return "Hata"

    def calculate_duration(self):
        duration = None
        try:
            tag = TinyTag.get(self.file_path)
            if tag.duration: duration = tag.duration
        except: pass

        if duration is None:
            try:
                ext = os.path.splitext(self.file_path)[1].lower()
                if ext in ['.mts', '.mkv', '.avi', '.mov', '.mp4', '.flv']:
                    cap = cv2.VideoCapture(self.file_path)
                    if cap.isOpened():
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                        if fps > 0: duration = count / fps
                        cap.release()
            except: pass
        return self.format_seconds(duration)

    def format_seconds(self, seconds):
        if not seconds: return "-"
        try:
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            if h > 0: return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
            else: return f"{int(m):02d}:{int(s):02d}"
        except: return "-"

class HashUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Hash Analiz") 
        self.resize(1200, 600)
        self.threads = []

        # --- RENK YÖNETİMİ ---
        self.hash_color_map = {} 
        self.palette = [
            QColor("#FFF0F5"), # Lavender Blush
            QColor("#F0FFF0"), # Honeydew
            QColor("#F0F8FF"), # Alice Blue
            QColor("#FFFFE0"), # Light Yellow
            QColor("#FFF5EE"), # Seashell
            QColor("#E6E6FA"), # Lavender
            QColor("#FFEFD5"), # Papaya Whip
            QColor("#FFE4E1"), # Misty Rose
            QColor("#D3FFCE"), # Pastel Yeşilimsi
            QColor("#FFD1DC"), # Pastel Pembemsi
        ]
        self.color_index = 0

        # --- TASARIM ---
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f2f5; }
            QTableWidget { 
                background-color: #ffffff; 
                gridline-color: #d1d5db;
                font-size: 13px;
                border: 1px solid #d1d5db;
                color: #1f2937;
            }
            QTableWidget::item { padding: 5px; }
            QTableWidget::item:selected {
                background-color: #3b82f6;
                color: white;
            }
            QHeaderView::section {
                background-color: #e5e7eb;
                color: #111827;
                padding: 6px;
                font-weight: bold;
                border: 1px solid #c5c5c5;
            }
            /* STATUS BAR TASARIMI (DÜZELTİLDİ) */
            QStatusBar {
                background-color: #d1d5db; /* Daha belirgin gri */
                border-top: 1px solid #9ca3af;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(15, 15, 15, 15) 

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        headers = ["Dosya Adı", "Süre", "Boyut", "Tarih", "MD5 Değeri"]
        self.table.setHorizontalHeaderLabels(headers)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 140)

        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.setAcceptDrops(True)
        self.table.setAcceptDrops(False)
        self.layout.addWidget(self.table)

        # --- STATUS BAR & SAYAÇ ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.count_label = QLabel("0 Dosya")
        # BURASI DÜZELTİLDİ: Rengi siyah ve kalın yaptık
        self.count_label.setStyleSheet("""
            color: black; 
            font-weight: bold; 
            font-size: 12px; 
            padding-left: 10px;
        """) 
        self.status_bar.addWidget(self.count_label)
        # ---------------------------

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()

    def dropEvent(self, event: QDropEvent):
        self.table.setSortingEnabled(False)
        urls = event.mimeData().urls()
        for url in urls:
            path = url.toLocalFile()
            if os.path.isdir(path): self.add_folder_contents(path)
            elif os.path.isfile(path): self.add_file_to_table(path)
        self.table.setSortingEnabled(True)

    def add_folder_contents(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                self.add_file_to_table(os.path.join(root, file))

    def update_file_count(self):
        """Tablodaki satır sayısını okuyup alt çubuğa yazar."""
        count = self.table.rowCount()
        self.count_label.setText(f"{count} Dosya")

    def add_file_to_table(self, file_path):
        file_name = os.path.basename(file_path)
        try:
            size_mb = f"{os.path.getsize(file_path) / (1024*1024):.2f} MB"
            ts = os.path.getmtime(file_path)
            date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
        except:
            size_mb = "0.00 MB"
            date_str = "-"

        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(file_name))
        self.table.setItem(row, 2, NumericTableWidgetItem(size_mb))
        self.table.setItem(row, 3, QTableWidgetItem(date_str))
        self.table.setItem(row, 1, QTableWidgetItem("...")) 
        self.table.setItem(row, 4, QTableWidgetItem("Hesaplanıyor..."))

        self.update_file_count()

        worker = AnalysisWorker(file_path, row)
        worker.finished_signal.connect(self.update_table_cell)
        worker.finished.connect(lambda: self.cleanup_thread(worker))
        self.threads.append(worker)
        worker.start()

    def update_table_cell(self, row, col, text):
        self.table.setItem(row, col, QTableWidgetItem(text))
        
        if col == 4 and text != "Hata" and text != "Hesaplanıyor...":
            self.smart_colorize_duplicates(text)

    def smart_colorize_duplicates(self, current_md5):
        matching_rows = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 4)
            if item and item.text() == current_md5:
                matching_rows.append(row)

        if len(matching_rows) > 1:
            if current_md5 in self.hash_color_map:
                group_color = self.hash_color_map[current_md5]
            else:
                group_color = self.palette[self.color_index % len(self.palette)]
                self.hash_color_map[current_md5] = group_color
                self.color_index += 1

            for row in matching_rows:
                self.color_row(row, group_color)

    def color_row(self, row, color):
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            if item:
                item.setBackground(QBrush(color))
                item.setForeground(QBrush(QColor("black")))

    def cleanup_thread(self, worker):
        if worker in self.threads:
            self.threads.remove(worker)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HashUygulamasi()
    window.show()
    sys.exit(app.exec())