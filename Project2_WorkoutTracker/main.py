# Imports
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QDateEdit, QLineEdit, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import pandas as pd

from sys import exit

# Main Class
class FitTrack(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.button_click()
    
    # Settings
    def settings(self):
        self.setWindowTitle("Workout Tracker")
        self.resize(1400, 1200)

    # init UI
    def initUI(self):
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())

        # Entry boxes
        self.workout_box = QComboBox()
        self.workout_box.setPlaceholderText("Enter Workout Type")
        self.workout_box.addItems(["Upper Body", "Lower Body", "Cardio"])
        
        self.cal_box = QLineEdit()
        self.cal_box.setPlaceholderText("(Optional)")

        self.duration_box = QLineEdit()
        self.duration_box.setPlaceholderText("Duration in Min.")

        self.description_box = QLineEdit()
        self.description_box.setPlaceholderText("Enter a description")

        self.chart_type_box = QComboBox()
        self.chart_type_box.setPlaceholderText("Choose desired chart")
        self.chart_type_box.addItems(["Duration vs Calories", "Schedule", "Total Workout Hours per Month"])
        
        # Buttons
        self.submit_btn = QPushButton("Submit")
        self.add_btn = QPushButton("Add")
        self.delete_btn = QPushButton("Delete")
        self.clear_btn = QPushButton("Clear")
        self.dark_mode_btn = QCheckBox("Dark Mode")

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Workout", "Calories", "Duration", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        self.figure = plt.figure(figsize=(9,9))
        self.canvas = FigureCanvas(self.figure)

        # Layout Design
        self.master_layout = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

            # Workout Data Entry
        self.logo_row = QHBoxLayout()
        self.sub_row1 = QHBoxLayout()
        self.sub_row2 = QHBoxLayout()
        self.sub_row3 = QHBoxLayout()
        self.sub_row4 = QHBoxLayout()
        self.sub_row5 = QHBoxLayout()
        self.sub_row6 = QHBoxLayout()

        label = QLabel(self)
        logo = QPixmap("Design ohne Titel.png")
        label.setPixmap(logo)
        self.logo_row.addWidget(label)

        self.sub_row1.addWidget(QLabel("Date"))
        self.sub_row1.addWidget(self.date_box)

        self.sub_row2.addWidget(QLabel("Workout Type"))
        self.sub_row2.addWidget(self.workout_box)
        
        self.sub_row3.addWidget(QLabel("Calories"))
        self.sub_row3.addWidget(self.cal_box)

        self.sub_row4.addWidget(QLabel("Duration"))
        self.sub_row4.addWidget(self.duration_box)
        
        self.sub_row5.addWidget(QLabel("Description"))
        self.sub_row5.addWidget(self.description_box)

        self.col1.addLayout(self.logo_row)
        self.col1.addLayout(self.sub_row1)
        self.col1.addLayout(self.sub_row2)
        self.col1.addLayout(self.sub_row3)
        self.col1.addLayout(self.sub_row4)
        self.col1.addLayout(self.sub_row5)
        self.col1.addWidget(self.dark_mode_btn)

            # Buttons & Chart Selection
        btn_row1 = QHBoxLayout()
        btn_row2 = QHBoxLayout()
        btn_row3 = QHBoxLayout()
        btn_row4 = QHBoxLayout()

        btn_row1.addWidget(self.add_btn)
        btn_row1.addWidget(self.delete_btn)
        
        btn_row2.addWidget(QLabel("Chart"))
        btn_row3.addWidget(self.chart_type_box)
        btn_row4.addWidget(self.submit_btn)
        btn_row4.addWidget(self.clear_btn)

        self.col1.addLayout(btn_row1)
        self.col1.addLayout(btn_row2)
        self.col1.addLayout(btn_row3)
        self.col1.addLayout(btn_row4)

            # Plotting Area & Database Table
        self.col2.addWidget(self.canvas)
        self.col2.addWidget(self.table)

        self.master_layout.addLayout(self.col1, 30)
        self.master_layout.addLayout(self.col2, 70)
        self.setLayout(self.master_layout)

        self.apply_styles()
        self.load_data()

    # Button Events
    def button_click(self):
        self.add_btn.clicked.connect(self.add_workout)
        self.delete_btn.clicked.connect(self.delete_workout)
        self.submit_btn.clicked.connect(self.create_chart)
        self.dark_mode_btn.stateChanged.connect(self.toggle_dark)
        self.clear_btn.clicked.connect(self.reset)
   
    # Load data
    def load_data(self):
        self.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM workout ORDER BY date DESC")
        row = 0
        while query.next():
            workout_id = query.value(0)
            date = query.value(1)
            workout_type = query.value(2)
            calories = query.value(3)
            duration = query.value(4)
            description = query.value(5)

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(workout_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(str(workout_type)))
            self.table.setItem(row, 3, QTableWidgetItem(str(calories)))
            self.table.setItem(row, 4, QTableWidgetItem(str(duration)))
            self.table.setItem(row, 5, QTableWidgetItem(str(description)))
            row += 1
            
    # Add workout data
    def add_workout(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        calories = self.cal_box.text()
        workout_type = self.workout_box.currentText()
        duration = self.duration_box.text()
        description = self.description_box.text()

        if workout_type == "":
                print("ERROR:{e}")
                QMessageBox.warning(self, "Error", "Please choose a workout type!")
                return
        
        if duration == "":
                print("ERROR:{e}")
                QMessageBox.warning(self, "Error", "Please enter how long you worked out for.")
                return

        if calories == "":
            if workout_type == "Upper Body" or "Lower Body":
                # ca. 170 calories per 30 mins
                calories = str(round(170/30*int(duration)))

            else:
                # cardio ca. 350 calories per 30 mins
                calories = str(round(350/30*int(duration)))

        
        query = QSqlQuery("""
                          INSERT INTO workout (date, workout, calories, duration, description)
                          VALUES (?,?,?,?,?)
                          """)
        query.addBindValue(date)
        query.addBindValue(workout_type)
        query.addBindValue(calories)
        query.addBindValue(duration)
        query.addBindValue(description)
        query.exec_()

        self.cal_box.clear()
        self.duration_box.clear()
        self.description_box.clear()

        self.load_data()

    # Delete workout data
    def delete_workout(self):
        selected_row = self.table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please choose a row to delete")

        work_id = int(self.table.item(selected_row,0).text())
        confirm = QMessageBox.question(self, "Confirmation", "Are you sure you want to delete this workout?", QMessageBox.Yes, QMessageBox.No)

        if confirm == QMessageBox.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM workout WHERE id = ?")
        query.addBindValue(work_id)
        query.exec_()

        self.load_data()

    # Create plots
    def create_chart(self):
        
        # Reset plotting area
        self.figure.clear()
        self.canvas.draw()
        
        plt.style.use("seaborn-v0_8-darkgrid")

        # 1st plot - Scatter plot "Duration vs Calories"
        if self.chart_type_box.currentText() == "Duration vs Calories":
            
            durations = []
            calories = []
            query = QSqlQuery("SELECT duration, calories FROM workout ORDER BY calories ASC")

            while query.next():
                dist_value = query.value(0)
                cal_value = query.value(1)
                durations.append(dist_value)
                calories.append(cal_value)

            try:
                min_cal = min(calories)
                max_cal = max(calories)
                normalized_cal = [(cal_value - min_cal / (max_cal - min_cal)) for cal_value in calories]

                ax = self.figure.subplots()
                ax.scatter(durations, calories, c=normalized_cal, cmap="winter")
                ax.set_title("Duration VS Calories",fontsize=20)
                ax.set_xlabel("Duration (min)", fontsize=16)
                ax.set_ylabel("Burned Calories", fontsize=16)
                ax.tick_params(axis="both", which="major", labelsize=14)

                cbar = ax.figure.colorbar(ax.collections[0], label="Normalized Calories")
                cbar.ax.tick_params(labelsize=12)
                ax.legend()
                self.canvas.draw()

            except Exception as e:
                print("ERROR:{e}")
                QMessageBox.warning(self, "Error", "Please enter some data first!")

        # 2nd plot - Scatter plot "Schedule"
        elif self.chart_type_box.currentText() == "Schedule":

            days = []
            months_years = []
            query = QSqlQuery("SELECT date FROM workout ORDER BY date")

            while query.next():
                day_value  = int(query.value(0)[-2:])
                year_month_value = query.value(0)[:7]
                days.append(day_value)
                months_years.append(year_month_value)

            try:
                ax = self.figure.subplots()

                y_labels = []
                y_labels.extend(range(1,32))

                ax.scatter(months_years, days, c=days, cmap="winter", marker="s", s=200)
                ax.set_title("Past Workout Schedule", fontsize=20)
                ax.set_xlabel("Month", fontsize=18)
                ax.set_ylabel("Day",fontsize=18)
                ax.set_yticks(y_labels)
                ax.tick_params(axis="both", which="major", labelsize=16)
                ax.invert_yaxis()
                self.canvas.draw()

            except Exception as e:
                print("ERROR:{e}")
                QMessageBox.warning(self, "Error", "Please enter some data first!")
        
        # 3rd Plot - Monthly workout hours
        elif self.chart_type_box.currentText() == "Total Workout Hours per Month":
            
            data = []
            query = QSqlQuery("SELECT date, duration FROM workout ORDER BY date")

            while query.next():
                year_month_value = query.value(0)[:7]
                data.append([year_month_value, query.value(1)])

            months_df = pd.DataFrame(data=data, columns=["year-month", "duration"])
            months_df = months_df.groupby(by="year-month").sum().reset_index()
            months_df["monthly_hrs"] = round(months_df["duration"]/60, 2)
            
            # print(months_df)

            try:
                ax = self.figure.subplots()

                ax.plot(months_df["year-month"], months_df["monthly_hrs"], c="#3bd6c6")
                ax.set_title("Monthly Time at the Gym", fontsize=16)
                ax.set_xlabel("Month", fontsize=14)
                ax.set_ylabel("Total Time (hrs)",fontsize=14)
                ax.tick_params(axis="both", which="major", labelsize=12)
                self.canvas.draw()

            except Exception as e:
                print("ERROR:{e}")
                QMessageBox.warning(self, "Error", "Please enter some data first!")

        # No plot selection
        else:
            QMessageBox.warning(self, "Error", "Please chose a chart type.")
        
    # Style GUI
    def apply_styles(self):
        self.setStyleSheet("""
        QWidget {
                background-color: #c7cfd7;
        }
                           
        QLabel {
                color: #333;
                font-size: 24px;
        }        
        
        QLineEdit, QComboBox, QDateEdit {
                background-color: #dadada;
                color: #333;
                border: 1px solid #444;
                padding: 10px;
        }
        
        QCheckBox {
                padding: 10px;
        }
                                             
        QTableWidget {
                background-color: #c7cfd7;
                color: #333;
                border: 1px solid #444;
                selection-background-color: #ddd;
        }
        
        QHeaderView::section {
                background-color: #dadada;
                color: #333;
        }
                           
        QPushButton {
                background-color: #dadada;
                color: #333;
                border: 1px solid #444;
                padding: 8px 16px;
                font-size: 24px;
        }
                           
        QPushButton:hover {
                background-color: #54927d;
        }
        """)

        self.figure.patch.set_facecolor("#8899ac")
        self.table.setStyleSheet("background-color: #8899ac")

        if self.dark_mode_btn.isChecked():
            self.setStyleSheet("""
                QWidget {
                        background-color: #15202b;
                }
                                
                QLabel {
                        background-color: #15202b;
                        color: #fff;
                        font-size: 24px;
                }        
                
                QLineEdit, QComboBox, QDateEdit {
                        background-color: #15202b;
                        color: #fff;
                        border: 1px solid #444;
                        padding: 10px;
                }
                               
                QComboBox, QAbstractItemView {
                        color: #fff;
                }
                               
                QCheckBox {
                        background-color: #15202b;
                        color: #fff;
                        padding: 10px;
                }

                QTableWidget {
                        background-color: #22303c;
                        color: #eeeeee;
                        border: 1px solid #444;
                        selection-background-color: #ddd;
                }
                               
                QHeaderView::section {
                        background-color: #5d7185;
                        color: #eeeeee;
                }
                                
                QPushButton {
                        background-color: #8899ac;
                        color: #fff;
                        border: none;
                        padding: 8px 16px;
                        font-size: 24px;
                }
                                
                QPushButton:hover {
                        background-color: #444d4f;
                }
                """)

            self.figure.patch.set_facecolor("#8899ac")
            self.table.setStyleSheet("background-color: #8899ac")
   
    # Dark Mode
    def toggle_dark(self):
        self.apply_styles()

    # Reset all contents
    def reset(self):
        self.date_box.setDate(QDate.currentDate())
        self.cal_box.clear()
        self.duration_box.clear()
        self.description_box.clear()
        self.figure.clear()
        self.canvas.draw()


# Initialize DB
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("workout.db")

if not db.open():
    QMessageBox.critical(None, "ERROR", "Cannot open database")
    exit(2)

query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS workout(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            workout TEXT,
            calories REAL,
            duration REAL,
            description TEXT
            )
            """)


if __name__ == "__main__":
    app = QApplication([])
    main = FitTrack()
    main.show()
    app.exec_()
