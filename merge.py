# pdf_merger.py

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton,
    QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyPDF2 import PdfMerger

class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super(FileListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QListWidget.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)

    def dragEnterEvent(self, event):
        # Accept external and internal drags
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.accept()

    def dragMoveEvent(self, event):
        # Accept the event to allow drag-and-drop
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.accept()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            # Handle external file drops
            for url in event.mimeData().urls():
                filepath = url.toLocalFile()
                if filepath.lower().endswith('.pdf'):
                    if filepath not in [self.item(i).text() for i in range(self.count())]:
                        self.addItem(filepath)
                    else:
                        QMessageBox.warning(self, 'Duplicate File', f'{os.path.basename(filepath)} is already added.')
                else:
                    QMessageBox.warning(self, 'Invalid File', f'{os.path.basename(filepath)} is not a PDF file.')
            event.acceptProposedAction()
        else:
            # Handle internal drag-and-drop reordering
            super(FileListWidget, self).dropEvent(event)

class PDFMergerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Merger')
        self.setGeometry(100, 100, 800, 300)
        self.initUI()
            
    def initUI(self):
        layout = QVBoxLayout()
        
        # Use the subclassed QListWidget
        self.listWidget = FileListWidget()
        layout.addWidget(self.listWidget)
        
        # Create buttons
        buttonLayout = QHBoxLayout()
        
        self.mergeButton = QPushButton('Merge')
        self.mergeButton.clicked.connect(self.mergePDFs)
        buttonLayout.addWidget(self.mergeButton)
        
        self.clearButton = QPushButton('Clear')
        self.clearButton.clicked.connect(self.clearList)
        buttonLayout.addWidget(self.clearButton)
        
        self.removeButton = QPushButton('Remove Selected')
        self.removeButton.clicked.connect(self.removeSelected)
        buttonLayout.addWidget(self.removeButton)
        
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
            
    def mergePDFs(self):
        if self.listWidget.count() == 0:
            QMessageBox.warning(self, 'No PDFs', 'Please add PDF files to merge.')
            return
            
        options = QFileDialog.Options()
        saveFilePath, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "", "PDF Files (*.pdf)", options=options)
        if saveFilePath:
            if not saveFilePath.lower().endswith('.pdf'):
                saveFilePath += '.pdf'
            if os.path.exists(saveFilePath):
                reply = QMessageBox.question(
                    self, 'Overwrite File',
                    f'The file {os.path.basename(saveFilePath)} already exists. Do you want to overwrite it?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    return
            try:
                merger = PdfMerger()
                for index in range(self.listWidget.count()):
                    pdf_path = self.listWidget.item(index).text()
                    merger.append(pdf_path)
                merger.write(saveFilePath)
                merger.close()
                QMessageBox.information(self, 'Success', f'Merged PDF saved to {saveFilePath}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'An error occurred while merging PDFs:\n{str(e)}')
        else:
            # User canceled save dialog
            return
                
    def clearList(self):
        self.listWidget.clear()
            
    def removeSelected(self):
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec_())
