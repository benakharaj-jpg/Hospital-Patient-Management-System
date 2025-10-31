import sqlite3
from datetime import datetime

# -----------------------------
# Database Connection & Setup
# -----------------------------
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS Departments (
    dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    phone TEXT,
    dept_id INTEGER,
    FOREIGN KEY(dept_id) REFERENCES Departments(dept_id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    phone TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    date TEXT,
    time TEXT,
    reason TEXT,
    FOREIGN KEY(patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES Doctors(doctor_id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    medicine TEXT,
    dosage TEXT,
    instructions TEXT,
    FOREIGN KEY(appointment_id) REFERENCES Appointments(appointment_id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Billing (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    total_amount REAL,
    date TEXT,
    FOREIGN KEY(patient_id) REFERENCES Patients(patient_id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS MedicalRecords (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    diagnosis TEXT,
    treatment TEXT,
    record_date TEXT,
    FOREIGN KEY(patient_id) REFERENCES Patients(patient_id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS DoctorAvailability (
    avail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER,
    day TEXT,
    time_slot TEXT,
    FOREIGN KEY(doctor_id) REFERENCES Doctors(doctor_id)
)''')

conn.commit()

# -----------------------------
# CRUD FUNCTIONS
# -----------------------------

# Departments
def add_department():
    name = input("Enter Department Name: ")
    cursor.execute("INSERT INTO Departments (name) VALUES (?)", (name,))
    conn.commit()
    print("✅ Department added")

def view_departments():
    cursor.execute("SELECT * FROM Departments")
    for row in cursor.fetchall():
        print(row)

# Doctors
def add_doctor():
    name = input("Enter Doctor Name: ")
    specialization = input("Enter Specialization: ")
    phone = input("Enter Phone: ")
    view_departments()
    dept_id = int(input("Enter Department ID: "))
    cursor.execute("INSERT INTO Doctors (name, specialization, phone, dept_id) VALUES (?, ?, ?, ?)",
                   (name, specialization, phone, dept_id))
    conn.commit()
    print("✅ Doctor added")

def view_doctors():
    cursor.execute('''SELECT d.doctor_id, d.name, d.specialization, d.phone, dept.name 
                      FROM Doctors d LEFT JOIN Departments dept ON d.dept_id = dept.dept_id''')
    for row in cursor.fetchall():
        print(row)

def update_doctor():
    doctor_id = int(input("Enter Doctor ID to update: "))
    name = input("Enter New Name: ")
    specialization = input("Enter New Specialization: ")
    phone = input("Enter New Phone: ")
    view_departments()
    dept_id = int(input("Enter New Department ID: "))
    cursor.execute("UPDATE Doctors SET name=?, specialization=?, phone=?, dept_id=? WHERE doctor_id=?",
                   (name, specialization, phone, dept_id, doctor_id))
    conn.commit()
    print("✅ Doctor updated")

def delete_doctor():
    doctor_id = int(input("Enter Doctor ID to delete: "))
    cursor.execute("DELETE FROM Doctors WHERE doctor_id=?", (doctor_id,))
    conn.commit()
    print("✅ Doctor deleted")

# Patients
def add_patient():
    name = input("Enter Patient Name: ")
    age = int(input("Enter Age: "))
    gender = input("Enter Gender: ")
    phone = input("Enter Phone: ")
    cursor.execute("INSERT INTO Patients (name, age, gender, phone) VALUES (?, ?, ?, ?)",
                   (name, age, gender, phone))
    conn.commit()
    print("✅ Patient added")

def view_patients():
    cursor.execute("SELECT * FROM Patients")
    for row in cursor.fetchall():
        print(row)

def update_patient():
    patient_id = int(input("Enter Patient ID to update: "))
    name = input("Enter New Name: ")
    age = int(input("Enter New Age: "))
    gender = input("Enter New Gender: ")
    phone = input("Enter New Phone: ")
    cursor.execute("UPDATE Patients SET name=?, age=?, gender=?, phone=? WHERE patient_id=?",
                   (name, age, gender, phone, patient_id))
    conn.commit()
    print("✅ Patient updated")

def delete_patient():
    patient_id = int(input("Enter Patient ID to delete: "))
    cursor.execute("DELETE FROM Patients WHERE patient_id=?", (patient_id,))
    conn.commit()
    print("✅ Patient deleted")

# Appointments
def schedule_appointment():
    view_patients()
    patient_id = int(input("Enter Patient ID: "))
    view_doctors()
    doctor_id = int(input("Enter Doctor ID: "))
    date = input("Enter Date (YYYY-MM-DD): ")
    time = input("Enter Time (HH:MM AM/PM): ")
    reason = input("Enter Reason: ")
    cursor.execute("INSERT INTO Appointments (patient_id, doctor_id, date, time, reason) VALUES (?, ?, ?, ?, ?)",
                   (patient_id, doctor_id, date, time, reason))
    conn.commit()
    print("✅ Appointment scheduled")

def view_appointments():
    cursor.execute('''SELECT a.appointment_id, p.name, d.name, a.date, a.time, a.reason 
                      FROM Appointments a
                      JOIN Patients p ON a.patient_id = p.patient_id
                      JOIN Doctors d ON a.doctor_id = d.doctor_id''')
    for row in cursor.fetchall():
        print(row)

# Prescriptions
def add_prescription():
    view_appointments()
    appointment_id = int(input("Enter Appointment ID: "))
    medicine = input("Enter Medicine Name: ")
    dosage = input("Enter Dosage: ")
    instructions = input("Enter Instructions: ")
    cursor.execute("INSERT INTO Prescriptions (appointment_id, medicine, dosage, instructions) VALUES (?, ?, ?, ?)",
                   (appointment_id, medicine, dosage, instructions))
    conn.commit()
    print("✅ Prescription added")

def view_prescriptions():
    cursor.execute('''SELECT pr.prescription_id, a.appointment_id, p.name, d.name, pr.medicine, pr.dosage, pr.instructions
                      FROM Prescriptions pr
                      JOIN Appointments a ON pr.appointment_id = a.appointment_id
                      JOIN Patients p ON a.patient_id = p.patient_id
                      JOIN Doctors d ON a.doctor_id = d.doctor_id''')
    for row in cursor.fetchall():
        print(row)

# Billing
def generate_bill():
    view_patients()
    patient_id = int(input("Enter Patient ID: "))
    total_amount = float(input("Enter Total Amount: "))
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO Billing (patient_id, total_amount, date) VALUES (?, ?, ?)",
                   (patient_id, total_amount, date))
    conn.commit()
    print("✅ Bill generated")

def view_bills():
    cursor.execute('''SELECT b.bill_id, p.name, b.total_amount, b.date
                      FROM Billing b
                      JOIN Patients p ON b.patient_id = p.patient_id''')
    for row in cursor.fetchall():
        print(row)

# -----------------------------
# RECEPTIONIST MENU
# -----------------------------
def menu():
    while True:
        print("\n--- Hospital Management System ---")
        print("1. Manage Departments")
        print("2. Manage Doctors")
        print("3. Manage Patients")
        print("4. Schedule/View Appointments")
        print("5. Manage Prescriptions")
        print("6. Billing")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            print("\n--- Departments ---")
            print("a. Add Department")
            print("b. View Departments")
            sub = input("Choice: ")
            if sub == "a":
                add_department()
            elif sub == "b":
                view_departments()

        elif choice == "2":
            print("\n--- Doctors ---")
            print("a. Add Doctor")
            print("b. View Doctors")
            print("c. Update Doctor")
            print("d. Delete Doctor")
            sub = input("Choice: ")
            if sub == "a":
                add_doctor()
            elif sub == "b":
                view_doctors()
            elif sub == "c":
                update_doctor()
            elif sub == "d":
                delete_doctor()

        elif choice == "3":
            print("\n--- Patients ---")
            print("a. Add Patient")
            print("b. View Patients")
            print("c. Update Patient")
            print("d. Delete Patient")
            sub = input("Choice: ")
            if sub == "a":
                add_patient()
            elif sub == "b":
                view_patients()
            elif sub == "c":
                update_patient()
            elif sub == "d":
                delete_patient()

        elif choice == "4":
            print("\n--- Appointments ---")
            print("a. Schedule Appointment")
            print("b. View Appointments")
            sub = input("Choice: ")
            if sub == "a":
                schedule_appointment()
            elif sub == "b":
                view_appointments()

        elif choice == "5":
            print("\n--- Prescriptions ---")
            print("a. Add Prescription")
            print("b. View Prescriptions")
            sub = input("Choice: ")
            if sub == "a":
                add_prescription()
            elif sub == "b":
                view_prescriptions()

        elif choice == "6":
            print("\n--- Billing ---")
            print("a. Generate Bill")
            print("b. View Bills")
            sub = input("Choice: ")
            if sub == "a":
                generate_bill()
            elif sub == "b":
                view_bills()

        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("❌ Invalid Choice. Try again!")

# -----------------------------
# RUN SYSTEM
# -----------------------------
if __name__ == "__main__":
    menu()
