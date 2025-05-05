import os
import re
import sys
import networkx as nx
from pyvis.network import Network
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self, html_path):
        super().__init__()
        self.setWindowTitle("Graph Viewer")
        self.setGeometry(100, 100, 1280, 720)
        self.browser = QWebEngineView()
        self.load_html(html_path)
        self.setCentralWidget(self.browser)

    def load_html(self, path):
        """Загружает HTML с принудительным обновлением"""
        self.browser.load(QUrl.fromLocalFile(path))
        self.browser.reload()


def main():
    try:
        # 1. Пути и подготовка
        current_dir = os.path.dirname(os.path.abspath(__file__))
        edges_path = os.path.join(current_dir, "edges.txt")
        html_path = os.path.join(current_dir, "graph.html")
        
        print(f"Рабочая директория: {current_dir}")
        print(f"Путь к edges.txt: {edges_path}")
        print(f"Путь к graph.html: {html_path}")

        # 2. Удаление старого графа
        if os.path.exists(html_path):
            os.remove(html_path)
            print("Старый graph.html удален")

        # 3. Чтение edges.txt с диагностикой
        edges = []
        line_counter = 0
        error_counter = 0
        
        with open(edges_path, "r", encoding="utf-8", errors="replace") as f:
            print("\nНачало чтения edges.txt:")
            for line_number, line in enumerate(f, 1):
                line_counter += 1
                raw_line = line.rstrip('\n')
                clean_line = raw_line.strip()
                
                if not clean_line:
                    print(f"Строка {line_number}: Пропущена (пустая)")
                    continue
                
                # Гибкое разделение данных
                parts = re.split(r'[\s,;|]+', clean_line)
                if len(parts) < 2:
                    error_counter += 1
                    print(f"Строка {line_number}: ОШИБКА '{raw_line}'")
                    continue
                
                src, dst = parts[0], parts[1]
                edges.append((src, dst))
                print(f"Строка {line_number}: OK '{src}' -> '{dst}'")

        print(f"\nИтого: {line_counter} строк обработано")
        print(f"Успешных ребер: {len(edges)}")
        print(f"Ошибочных строк: {error_counter}")

        if not edges:
            print("\nФАТАЛЬНАЯ ОШИБКА: Нет данных для графа!")
            return None

        # 4. Генерация графа
        G = nx.Graph()
        G.add_edges_from(edges)
        
        net = Network(
            notebook=False,
            height="720px",
            width="1280px",
            cdn_resources="in_line",
            bgcolor="#1a1a1a",
            font_color="white"
        )
        
        net.from_nx(G)
        html_content = net.generate_html()
        
        # 5. Сохранение HTML с проверкой
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"\nФайл {html_path} успешно создан")
        print(f"Размер файла: {os.path.getsize(html_path)} байт")
        
        return html_path

    except Exception as e:
        print(f"\nКРИТИЧЕСКАЯ ОШИБКА: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    html_path = main()
    
    if html_path and os.path.exists(html_path):
        app = QApplication(sys.argv)
        window = MainWindow(html_path)
        window.show()
        sys.exit(app.exec_())
    else:
        print("\nСоздание графа невозможно!")
        sys.exit(1)