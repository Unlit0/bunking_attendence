import json
import os
import math

# file to store attendance data
file_name = "my_attendance.json"

def load_attendance():
    if os.path.exists(file_name):
        f = open(file_name, "r")
        data = json.load(f)
        f.close()
        return data
    else:
        return {}

def save_attendance(data):
    f = open(file_name, "w")
    json.dump(data, f, indent=4)
    f.close()

def check_bunk_status(att, tot):
    if tot == 0:
        return 0, "No classes happened yet"
    
    perc = (att / tot) * 100
    perc = round(perc, 1)

    # if attendance is less than 75%
    if perc < 75:
        # formula: (att + x) / (tot + x) = 0.75
        req = math.ceil((0.75 * tot - att) / 0.25)
        return perc, f"DANGER! Attend next {req} classes"
    
    # if attendance is 75% or more
    else:
        # formula: att / (tot + x) = 0.75
        bunks = math.floor((att / 0.75) - tot)
        if bunks == 0:
            return perc, "SAFE (On border, dont bunk next!)"
        else:
            return perc, f"SAFE! Can bunk {bunks} classes"

# load saved data at start
subjects = load_attendance()

while True:
    print("\n======================================")
    print("     COLLEGE ATTENDANCE TRACKER")
    print("======================================")
    print("1. Show Attendance Status")
    print("2. Add New Subject")
    print("3. Mark Today's Attendance")
    print("4. Delete Subject")
    print("5. Exit")
    
    ch = input("\nEnter choice (1-5): ")

    if ch == "1":
        if len(subjects) == 0:
            print("\nNo subjects added yet! Use option 2 first.")
        else:
            print("\n------------------------------------------------------------")
            for sub in subjects:
                att = subjects[sub]["attended"]
                tot = subjects[sub]["total"]
                
                perc, msg = check_bunk_status(att, tot)
                
                # making a simple 10-step bar using # and -
                hashes = int(perc // 10)
                dashes = 10 - hashes
                bar = "[" + ("#" * hashes) + ("-" * dashes) + "]"
                
                print(f"{sub} ({att}/{tot}) -> {bar} {perc}%  |  {msg}")
            print("------------------------------------------------------------")

    elif ch == "2":
        sub = input("Enter subject name: ").strip().capitalize()
        try:
            att = int(input("Classes attended so far: "))
            tot = int(input("Total classes taken so far: "))
            
            if att > tot or att < 0 or tot < 0:
                print("Error: Attended cant be more than total classes!")
            else:
                subjects[sub] = {"attended": att, "total": tot}
                save_attendance(subjects)
                print(f"Saved {sub}!")
        except:
            print("Invalid input! Please enter numbers only.")

    elif ch == "3":
        sub = input("Enter subject name: ").strip().capitalize()
        if sub in subjects:
            ans = input("Were you Present or Absent? (p/a): ").lower()
            if ans == "p":
                subjects[sub]["attended"] += 1
                subjects[sub]["total"] += 1
                save_attendance(subjects)
                print("Updated! Marked Present.")
            elif ans == "a":
                subjects[sub]["total"] += 1
                save_attendance(subjects)
                print("Updated! Marked Absent.")
            else:
                print("Wrong input, type p or a.")
        else:
            print("Subject not found! Add it in option 2 first.")

    elif ch == "4":
        sub = input("Enter subject name to delete: ").strip().capitalize()
        if sub in subjects:
            del subjects[sub]
            save_attendance(subjects)
            print(f"{sub} deleted.")
        else:
            print("Subject not found.")

    elif ch == "5":
        print("Exiting...")
        break

    else:
        print("Invalid choice, try again.")