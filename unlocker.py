#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025
# Developer : Mohammed Al-Baqer

import sys
import json
import os
import time
import subprocess
import shutil
import ctypes
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QFileDialog, 
    QSpacerItem, QSizePolicy, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

''''def Administrator():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def switch():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()'''

SETTINGS_FILE = "settings.json"

class UnlockerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unlocker GUI")
        self.setGeometry(100, 100, 100, 100)
        self.setStyleSheet("""
            font-family: 'Segoe UI', 'Cairo';
            font-size: 14px;
            QPushButton {
                padding: 8px;
                min-width: 80px;
            }
            QComboBox {
                padding: 6px;
            }
        """)
        self.setWindowIcon(QIcon(r"icon\icon.ico"))

        self.current_lang = "ar"
        self.current_action = "لا شيء"
        self.selected_file = ""
        self.process_name = ""

        self.load_settings()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        lang_layout = QHBoxLayout()
        lang_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.lang_btn = QPushButton("English" if self.current_lang == "ar" else "العربية")
        self.lang_btn.setStyleSheet("min-width: 80px;")
        self.lang_btn.clicked.connect(self.toggle_language)
        lang_layout.addWidget(self.lang_btn)
        main_layout.addLayout(lang_layout)

        file_action_layout = QHBoxLayout()
        file_action_layout.setSpacing(10)
        
        self.action_combo = QComboBox()
        self.set_actions()
        file_action_layout.addWidget(self.action_combo, 1)
        
        self.browse_btn = QPushButton("تصفح ملف" if self.current_lang == "ar" else "Browse File")
        self.browse_btn.clicked.connect(self.browse_file)
        file_action_layout.addWidget(self.browse_btn, 1)
        
        main_layout.addLayout(file_action_layout)

        self.file_info = QLabel("" if self.current_lang == "ar" else "")
        self.file_info.setStyleSheet("color: #666; font-size: 12px;")
        self.file_info.setWordWrap(True)
        main_layout.addWidget(self.file_info)

        action_exit_layout = QHBoxLayout()
        action_exit_layout.setSpacing(10)
        
        self.admin_button = QPushButton("تنفيذ" if self.current_lang == "ar" else "Execute")
        self.admin_button.setIcon(QIcon(r"icon\Adminisrtator.ico"))
        self.admin_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.admin_button.clicked.connect(self.run_admin_action)
        action_exit_layout.addWidget(self.admin_button, 1)

        self.exit_btn = QPushButton("خروج" if self.current_lang == "ar" else "Exit")
        self.exit_btn.setStyleSheet("background-color: #f44336; color: white;")
        self.exit_btn.clicked.connect(self.close)
        action_exit_layout.addWidget(self.exit_btn, 1)
        
        main_layout.addLayout(action_exit_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(5)
        
        self.about_btn = QPushButton("حول المطور" if self.current_lang == "ar" else "About")
        self.about_btn.setStyleSheet("font-size: 12px; color: #2196F3;")
        self.about_btn.clicked.connect(self.show_about)
        
        self.license_btn = QPushButton("الترخيص" if self.current_lang == "ar" else "License")
        self.license_btn.setStyleSheet("font-size: 12px; color: #2196F3;")
        self.license_btn.clicked.connect(self.show_license)
        
        self.policy_btn = QPushButton("الخصوصية" if self.current_lang == "ar" else "Privacy")
        self.policy_btn.setStyleSheet("font-size: 12px; color: #2196F3;")
        self.policy_btn.clicked.connect(self.show_policy)
        
        bottom_layout.addWidget(self.about_btn)
        bottom_layout.addWidget(self.license_btn)
        bottom_layout.addWidget(self.policy_btn)

        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "ar" else "ar"
        self.save_settings()
        self.refresh_ui()

    def set_actions(self):
        self.action_combo.clear()
        actions_ar = ["لا شيء", "إنهاء المهمة", "حذف الملف", "تغيير الاسم", "نقل الملف"]
        actions_en = ["Select action", "End Task", "Delete File", "Rename File", "Move File"]
        actions = actions_ar if self.current_lang == "ar" else actions_en
        self.action_combo.addItems(actions)
        index = actions.index(self.current_action) if self.current_action in actions else 0
        self.action_combo.setCurrentIndex(index)

    def browse_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 
            "اختيار ملف" if self.current_lang == "ar" else "Select File",
            "", "All Files (*)")
        
        if file:
            self.selected_file = file
            file_name = os.path.basename(file)
            self.file_info.setText(f"{'الملف المحدد:' if self.current_lang == 'ar' else 'Selected file:'} {file_name}")

    def run_admin_action(self):
        '''if not Administrator():
            switch()
            return'''

        action = self.action_combo.currentText()
        self.current_action = action
        self.save_settings()

        if not self.selected_file:
            self.show_message("خطأ", "لم يتم اختيار أي ملف" if self.current_lang == "ar" else "No file selected", "error")
            return

        try:
            if action in ["إنهاء المهمة", "Kill Process"]:
                self.kill_process()
            elif action in ["حذف الملف", "Delete File"]:
                self.delete_file()
            elif action in ["تغيير الاسم", "Rename File"]:
                self.rename_file()
            elif action in ["نقل الملف", "Move File"]:
                self.move_file()
            else:
                self.show_message("خطأ", "لم يتم اختيار أي عملية" if self.current_lang == "ar" else "No action selected", "error")
        except Exception as e:
            self.show_message("خطأ", f"فشل التنفيذ: {str(e)}" if self.current_lang == "ar" else f"Execution failed: {str(e)}", "error")

    def kill_process(self):
        try:
            if os.name == 'nt':
                subprocess.run(["taskkill", "/f", "/im", os.path.basename(self.selected_file)], check=True)
            else:
                subprocess.run(["pkill", "-f", self.selected_file], check=True)
            
            self.show_message("نجاح", "تم إنهاء المهمة بنجاح" if self.current_lang == "ar" else "Process killed successfully", "info")
            self.log_action("إنهاء المهمة" if self.current_lang == "ar" else "Kill Process", self.selected_file)
        except subprocess.CalledProcessError:
            self.show_message("خطأ", "فشل في إنهاء المهمة" if self.current_lang == "ar" else "Failed to kill process", "error")
    
    def delete_file(self):
        try:
            if os.path.exists(self.selected_file):
                os.remove(self.selected_file)
                self.show_message("نجاح", "تم حذف الملف بنجاح" if self.current_lang == "ar" else "File deleted successfully", "info")
                self.log_action("حذف الملف" if self.current_lang == "ar" else "Delete File", self.selected_file)
                self.selected_file = ""
                self.file_info.setText("لا يوجد ملف محدد" if self.current_lang == "ar" else "No file selected")
            else:
                self.show_message("خطأ", "الملف غير موجود" if self.current_lang == "ar" else "File does not exist", "error")
        except Exception as e:
            self.show_message("خطأ", f"فشل في حذف الملف: {str(e)}" if self.current_lang == "ar" else f"Failed to delete file: {str(e)}", "error")
    
    def rename_file(self):
        new_name, ok = QInputDialog.getText(
            self,
            "تغيير الاسم" if self.current_lang == "ar" else "Rename File",
            "أدخل الاسم الجديد:" if self.current_lang == "ar" else "Enter new name:"
        )
        
        if ok and new_name:
            try:
                dir_path = os.path.dirname(self.selected_file)
                new_path = os.path.join(dir_path, new_name)
                os.rename(self.selected_file, new_path)
                self.selected_file = new_path
                self.file_info.setText(f"{'الملف المحدد:' if self.current_lang == 'ar' else 'Selected file:'} {new_name}")
                self.show_message("نجاح", "تم تغيير الاسم بنجاح" if self.current_lang == "ar" else "File renamed successfully", "info")
                self.log_action("تغيير الاسم" if self.current_lang == "ar" else "Rename File", 
                              self.selected_file, {"new_name": new_name})
            except Exception as e:
                self.show_message("خطأ", f"فشل في تغيير الاسم: {str(e)}" if self.current_lang == "ar" else f"Failed to rename: {str(e)}", "error")

    def move_file(self):
        new_dir = QFileDialog.getExistingDirectory(
            self,
            "اختر مجلد الوجهة" if self.current_lang == "ar" else "Select destination folder"
        )
        
        if new_dir:
            try:
                file_name = os.path.basename(self.selected_file)
                new_path = os.path.join(new_dir, file_name)
                shutil.move(self.selected_file, new_path)
                self.selected_file = new_path
                self.file_info.setText(f"{'الملف المحدد:' if self.current_lang == 'ar' else 'Selected file:'} {file_name} ({new_dir})")
                self.show_message("نجاح", "تم نقل الملف بنجاح" if self.current_lang == "ar" else "File moved successfully", "info")
                self.log_action("نقل الملف" if self.current_lang == "ar" else "Move File", 
                              self.selected_file, {"destination": new_dir})
            except Exception as e:
                self.show_message("خطأ", f"فشل في نقل الملف: {str(e)}" if self.current_lang == "ar" else f"Failed to move file: {str(e)}", "error")

    def log_action(self, action_name, file_path, extra_info=None):
        log_entry = {
            "action": action_name,
            "file": file_path,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if extra_info:
            log_entry.update(extra_info)

        data = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        if "history" not in data:
            data["history"] = []

        data["history"].append(log_entry)

        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def show_message(self, title, message, icon_type="info"):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        
        if icon_type == "info":
            msg.setIcon(QMessageBox.Information)
        elif icon_type == "error":
            msg.setIcon(QMessageBox.Critical)
        else:
            msg.setIcon(QMessageBox.Warning)
            
        msg.exec_()

    def show_about(self):
        about_text = """
        <h3>Unlocker GUI</h3>
        <p>أداة لإدارة الملفات والعمليات</p>
        <p>تطوير: محمد الباقر</p>
        """ if self.current_lang == "ar" else """
        <h3>Unlocker GUI</h3>
        <p>File and process management tool</p>
        <p>Developer: Mohammed Al-Baqer</p>
        """
        self.show_message("حول المطور" if self.current_lang == "ar" else "About", about_text)

    def show_license(self):
        license_text = """
        <h3>الترخيص</h3>
        <p>هذا البرنامج مجاني للاستخدام الشخصي.</p>
        <p>ممنوع إعادة توزيعه أو بيعه بدون إذن.</p>
        """ if self.current_lang == "ar" else """
        <h3>License</h3>
        <p>This software is free for personal use.</p>
        <p>Redistribution or sale without permission is prohibited.</p>
        """
        self.show_message("الترخيص" if self.current_lang == "ar" else "License", license_text)

    def show_policy(self):
        policy_text = """
        <h3>سياسة الخصوصية</h3>
        <p>هذا التطبيق لا يجمع أي بيانات شخصية.</p>
        <p>جميع العمليات تتم على جهازك فقط.</p>
        """ if self.current_lang == "ar" else """
        <h3>Privacy Policy</h3>
        <p>This application does not collect any personal data.</p>
        <p>All operations are performed locally on your device.</p>
        """
        self.show_message("سياسة الخصوصية" if self.current_lang == "ar" else "Privacy Policy", policy_text)

    def save_settings(self):
        data = {
            "language": self.current_lang,
            "action": self.current_action
        }
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.current_lang = data.get("language", "ar")
                self.current_action = data.get("action", "اختر عملية" if self.current_lang == "ar" else "Select action")

    def refresh_ui(self):
        self.lang_btn.setText("English" if self.current_lang == "ar" else "العربية")
        self.browse_btn.setText("تصفح ملف" if self.current_lang == "ar" else "Browse File")
        self.admin_button.setText("تنفيذ" if self.current_lang == "ar" else "Execute")
        self.exit_btn.setText("خروج" if self.current_lang == "ar" else "Exit")
        self.about_btn.setText("حول المطور" if self.current_lang == "ar" else "About")
        self.license_btn.setText("الترخيص" if self.current_lang == "ar" else "License")
        self.policy_btn.setText("الخصوصية" if self.current_lang == "ar" else "Privacy")
        self.file_info.setText("لا يوجد ملف محدد" if self.current_lang == "ar" else "No file selected")
        self.set_actions()

if __name__ == "__main__":

    '''if not Administrator():
        switch()'''
    
    start_time = time.time()
    log_file = "log.txt"

    try:
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"[START] {time.ctime()}\n")
    except Exception as e:
        pass
    
    try:
        app = QApplication(sys.argv)
        window = UnlockerApp()
        window.show()
        sys.exit(app.exec_())

    except Exception as e:
        pass

    finally:
        end_time = time.time()
        duration = end_time - start_time
        try:
            with open(log_file, "a", encoding="utf-8") as log:
                log.write(f"[END] {time.ctime()} - Duration: {duration:.2f} seconds\n\n")
        except Exception as e:
            pass


   