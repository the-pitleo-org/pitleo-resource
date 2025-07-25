import os
import json
import sys

PROXY_FILE = os.path.expanduser("Code/Python/pBrowse/piterm_browser_proxy.txt")
if os.path.exists(PROXY_FILE):
    with open(PROXY_FILE, 'r') as f:
        proxy = f.read().strip()
        if proxy:
            os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = f"--no-sandbox --proxy-server={proxy}"

from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QMenu, QMessageBox, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon

BOOKMARKS_FILE = os.path.expanduser("Code/Python/pBrowse/piterm_browser_bookmarks.json")

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('pBrowse')

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        self.bookmarks = self.load_bookmarks()

        # Update URL bar and window title when URL changes
        self.browser.urlChanged.connect(self.update_urlbar)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        navtb.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        bookmark_btn = QAction("Bookmark", self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        navtb.addAction(bookmark_btn)

        show_bookmarks_btn = QAction("Show Bookmarks", self)
        show_bookmarks_btn.triggered.connect(self.show_bookmark_menu)
        navtb.addAction(show_bookmarks_btn)

        proxy_btn = QAction("Set Proxy", self)
        proxy_btn.triggered.connect(self.set_proxy)
        navtb.addAction(proxy_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        self.bookmark_menu = QMenu("Bookmarks", self)
        self.populate_bookmark_menu()

        self.navigate_home()  # Load homepage on startup
        self.show()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://weelam.ca"))

    def navigate_to_url(self):
        url = self.urlbar.text()
        if os.path.exists(url):  # If it's a valid file path
            file_path = os.path.abspath(url)
            self.browser.setUrl(QUrl.fromLocalFile(file_path))
        else:
            if not url.startswith("http"):
                url = "http://" + url
            self.browser.setUrl(QUrl(url))

    def update_urlbar(self, qurl):
        url_str = qurl.toString()
        self.urlbar.setText(url_str)
        self.urlbar.setCursorPosition(0)
        self.setWindowTitle("pBrowse: " + url_str)  # Set window title to current URL

    def add_bookmark(self):
        url = self.browser.url().toString()
        if url not in self.bookmarks:
            self.bookmarks.append(url)
            self.save_bookmarks()
            self.add_bookmark_to_menu(url)
            QMessageBox.information(self, "Bookmark Added", f"Bookmarked: {url}")
        else:
            QMessageBox.information(self, "Already Bookmarked", f"This URL is already bookmarked.")

    def show_bookmark_menu(self):
        self.bookmark_menu.exec_(self.mapToGlobal(self.cursor().pos()))

    def add_bookmark_to_menu(self, url):
        action = QAction(url, self)
        action.triggered.connect(lambda _, url=url: self.browser.setUrl(QUrl(url)))
        self.bookmark_menu.addAction(action)

    def populate_bookmark_menu(self):
        for url in self.bookmarks:
            self.add_bookmark_to_menu(url)

    def load_bookmarks(self):
        if os.path.exists(BOOKMARKS_FILE):
            try:
                with open(BOOKMARKS_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_bookmarks(self):
        try:
            with open(BOOKMARKS_FILE, 'w') as f:
                json.dump(self.bookmarks, f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save bookmarks: {e}")

    def set_proxy(self):
        proxy, ok = QInputDialog.getText(self, "Set Proxy", "Enter proxy (e.g. 127.0.0.1:8080):")
        if ok:
            with open(PROXY_FILE, 'w') as f:
                f.write(proxy)
            QMessageBox.information(self, "Proxy Set", "Please restart the browser to apply the new proxy.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser()
    sys.exit(app.exec_())
