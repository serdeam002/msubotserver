import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By

def submit_form():
    # Get values from the Entry widgets
    course_code1 = course_code1_entry.get()
    section1 = section1_entry.get()

    try:
        # Navigate to the login page
        driver.get("https://reg.msu.ac.th/registrar/login.asp")

        # Find the username input field and enter username
        input_field = driver.find_element(By.XPATH, "//input[@name='f_uid']")
        input_field.send_keys(username_entry.get())

        # Find the password input field and enter password
        input_field = driver.find_element(By.XPATH, "//input[@name='f_pwd']")
        input_field.send_keys(password_entry.get())

        # Find and click the login button
        login_button = driver.find_element(By.XPATH, "//input[@value=' ตรวจสอบ ']")
        login_button.click()

        # Navigate to the course registration page
        driver.get("https://reg.msu.ac.th/registrar/enroll.asp")

        # Find the username input field and enter username
        input_field = driver.find_element(By.XPATH, "//input[@name='f_coursecode']")
        input_field.send_keys(course_code1)

        # Find the username input field and enter username
        input_field = driver.find_element(By.XPATH, "//input[@name='f_section']")
        input_field.send_keys(section1)

        # Find and click the login button
        login_button = driver.find_element(By.XPATH, "//input[@name='cmd_ok']")
        login_button.click()

        # Find and click the login button
        login_button = driver.find_element(By.XPATH, "//img[@title='Enroll']")
        login_button.click()

        driver.get("https://reg.msu.ac.th/registrar/confirm_enroll.asp")

        # Find and click the login button
        login_button = driver.find_element(By.XPATH, "//input[@value='ยืนยันการลงทะเบียน']")
        login_button.click()

        # Iterate over the course code and section entries
        for i in range(len(course_code_entries)):
            # Move back to the course registration page for the next iteration
            driver.get("https://reg.msu.ac.th/registrar/adddrop.asp")

            # Find the course code input field and enter course code
            input_field = driver.find_element(By.XPATH, "//input[@name='f_coursecode']")
            input_field.send_keys(course_code_entries[i].get())

            # Find and click the login button
            login_button = driver.find_element(By.XPATH, "//tbody/tr[4]/td[2]/input[1]")
            login_button.click()

            # Find the section input field and enter section
            input_field = driver.find_element(By.XPATH, "//input[@name='f_section']")
            input_field.send_keys(section_entries[i].get())

            # Find and click the login button
            login_button = driver.find_element(By.XPATH, "//input[@value='บันทึก']")
            login_button.click()

            driver.get("https://reg.msu.ac.th/registrar/confirm_adddrop.asp")

            login_button = driver.find_element(By.XPATH, "//input[@value='ยืนยันการลงทะเบียน']")
            login_button.click()

        #alert
        driver.get("https://reg.msu.ac.th/registrar/logout.asp")
        messagebox.showinfo("Success", "Add course successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Reset the Entry widgets
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        course_code1_entry.delete(0, tk.END)
        section1_entry.delete(0, tk.END)

        for entry in course_code_entries:
            entry.delete(0, tk.END)

        for entry in section_entries:
            entry.delete(0, tk.END)

def add_input_fields():
    # Create new Entry widgets for course code and section
    new_course_code_entry = tk.Entry(root)
    new_course_code_entry.grid(row=len(course_code_entries) + 3, column=2, padx=10, pady=10)
    course_code_entries.append(new_course_code_entry)

    new_section_entry = tk.Entry(root)
    new_section_entry.grid(row=len(section_entries) + 3, column=3, padx=10, pady=10)
    section_entries.append(new_section_entry)

def delete_input_fields():
    # Remove the last set of course code and section fields
    if len(course_code_entries) > 1 and len(section_entries) > 1:
        course_code_entries[-1].destroy()
        section_entries[-1].destroy()
        del course_code_entries[-1]
        del section_entries[-1]

# Create a Tkinter window
root = tk.Tk()
root.title("MSU Register for classes by.weap")
root.geometry('580x650')

# Create Entry widgets for user input
username_label = tk.Label(root, text="Username:")
username_label.grid(row=1, column=0, sticky=tk.E, padx=10, pady=10)

username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=10, pady=10)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=2, column=0, sticky=tk.E, padx=10, pady=10)

password_entry = tk.Entry(root, show="*")  # Mask the password
password_entry.grid(row=2, column=1, padx=10, pady=10)

##############enroll################

course_code_label = tk.Label(root, text="(Enroll) Course Code")
course_code_label.grid(row=0, column=2, sticky=tk.E+tk.W)

section_label = tk.Label(root, text="(Enroll) Section")
section_label.grid(row=0, column=3, sticky=tk.E+tk.W)

# Create initial Entry widgets for course code and section
course_code1_entry = tk.Entry(root)
course_code1_entry.grid(row=1, column=2, padx=10, pady=10)

section1_entry = tk.Entry(root)
section1_entry.grid(row=1, column=3, padx=10, pady=10)

######################################

course_code_label = tk.Label(root, text="Course Code")
course_code_label.grid(row=2, column=2, sticky=tk.E+tk.W)

section_label = tk.Label(root, text="Section")
section_label.grid(row=2, column=3, sticky=tk.E+tk.W)

# Create initial Entry widgets for course code and section
course_code_entry = tk.Entry(root)
course_code_entry.grid(row=3, column=2, padx=10, pady=10)

section_entry = tk.Entry(root)
section_entry.grid(row=3, column=3, padx=10, pady=10)

# Lists to keep track of dynamically added Entry widgets
course_code_entries = [course_code_entry]
section_entries = [section_entry]

# Create a button to trigger the Selenium action
submit_button = tk.Button(root, text="Submit Form", command=submit_form, bg='#45b592', fg='#ffffff')
submit_button.grid(row=len(course_code_entries) + 4, column=0, columnspan=2, pady=10)

# Create a button to add new input fields
add_fields_button = tk.Button(root, text="+ Add Fields", command=add_input_fields, bg='#FFFF00')
add_fields_button.grid(row=len(course_code_entries) + 2, column=0, columnspan=2, pady=10)

delete_fields_button = tk.Button(root, text="- Delete Fields", command=delete_input_fields, bg='#FF0000', fg='#ffffff')
delete_fields_button.grid(row=len(course_code_entries) + 3, column=0, columnspan=2, pady=10)

# Create a Chrome WebDriver instance (make sure chromedriver is in your PATH)
driver = webdriver.Chrome()

# Run the Tkinter event loop
root.mainloop()

# Close the WebDriver when the Tkinter window is closed
driver.quit()
