import requests
from bs4 import BeautifulSoup
import time
import json


def get_registrar():
     request = requests.get("https://registrar.kfupm.edu.sa/courses-classes/course-offering/").content
     soup = BeautifulSoup(request, "html.parser")
     terms = soup.find(id="course_term_code")
     departments = soup.find(id="course_dept_code")

     get_terms_and_departments(terms, departments)


def get_terms_and_departments(terms, departments):
     terms_list = []
     departments_list = []

     for i in (terms, departments):
          if (i == terms):
               lists = terms_list
          else:
               lists = departments_list

          options = i.find_all("option")[1::]
          for option in options:
               lists.append(option.text)

     registrar_input = get_registrar_input(terms_list, departments_list)
     if (registrar_input == False):
          return

     time_input = get_time_input()
     if (time_input == False):
          return

     search_input = get_search_input()
     if (search_input == False):
          return


def get_deps_list(i):
     deps_code = ["ACFN", "AE", "ARE", "ARC", "CE", "CEM", "CHE", "CHEM", "COE", "CPG", "CRP", "ERTH", "EE", "ELI", "ELD", "ISOM", "GS", "IAS", "ICS", "LS", "MATH", "MBA", "ME", "MGT", "PE", "PETE", "PYHS", "PSE", "SE", "CIE", "MSE"]

     return deps_code[i]


def get_registrar_input(terms_list, departments_list):
     for i in (terms_list, departments_list):
          for j in range(len(i)):
               print(f"[{j + 1}] {i[j]}")
          user_input = input("[*] - Enter number: ")

          if (len(i) > 0 and len(i) >= int(user_input)):
               if (i == terms_list):
                    term = user_input
               else:
                    department = get_deps_list(int(user_input) - 1)
          else:
               print("You can't choose a number out of range!")
               return False

     return term, department


def get_time_input():
     print("[1] 10s\n[2] 20s\n[3] 30s\n[4] 60s")
     reload_every = int(input("[*] - Check every (enter number): "))

     if (reload_every > 0 and reload_every <= 4):
          if (reload_every == 4):
               reload_every *= 15
          else:
               reload_every *= 10
     else:
          print("You can't choose a number out of range!")
          return False

     return reload_every


def inter_search(i):
     search_list = ["Section", "Activity", "CRN",  "Course Name", "Instructor", "Day", "Time", "Location", "Status", "Gender"]
     search_list_plural = ["/Sections", "/Activities", "/CRNs",  "/Courses Names", "/Instructors", "/Days", "", "/Locations", "", ""]

     return search_list[i], search_list_plural[i]


def get_example(i):
     time = ("e.g. 1000-1050")
     status = ("[1] Open\n[2] Wait list")
     gender = ("[1] Male\n[2] Female\n[3] Any")

     if (i == 7):
          element = time
     elif (i == 9):
          element = status
     else:
          element = gender

     return element


def get_search_input():
     filters = int(input("[*] - How many fliters you want to check each time: "))

     for i in range(filters):
          print("[1] Section\n[2] Activity\n[3] CRN\n[4] Course Name\n[5] Instructor\n[6] Day\n[7] Time\n[8] Location\n[9] Status\n[10] Gender")
          search_by = int(input("[*] - Search by: "))

          if (search_by > 0 and search_by <= 10):
               if (search_by == 7 or search_by == 9 or search_by == 10):
                    print(get_example(search_by))
               input(f"[*] - Enter {inter_search(search_by - 1)[0]}{inter_search(search_by - 1 )[1]}: ")

               # for i in search_by.split():
               #      pass
          else:
               print("You can't choose a number out of range!")
               return False











get_registrar()


def hi():
     for i in range(10000):
          req = requests.get("https://registrar.kfupm.edu.sa/api/course-offering?term_code=202120&department_code=ICS")
          status = req.status_code

          if (status != 200):
               not200()
          else:
               text = req.text
               if (text.find("The site is down")):
                    down()
                    return

               data = json.loads(req.text)
               if (data["data"] == None):
                    print("The API isn't working for the time being, the code will check for sections every 60s.")
                    time.sleep(40)
                    hi()
                    return
               itis200(data, i)
          print("\n\n")
          time.sleep(20)



def not200():
     print("The API isn't working for the time being, the code will check for sections every 60s.")
     time.sleep(40)
     hi()
     return


def down():
     print("The site is down for maintenance for the time being, the code will check every 60s.")
     time.sleep(40)
     hi()
     return


def itis200(data, index):
     datas = data["data"]
     print(index + 1)

     for i in range(44):
          course = datas[i]
          course_number = course["course_number"]
          section = course["section_number"]

          if (section.find("F") != -1):
               continue

          class_type = course["class_type"]
          crn = course["crn"]
          available_seats = course["available_seats"]
          waiting_list_count = course["waiting_list_count"]

          if ((available_seats != 0) or (waiting_list_count != 0)):
               print(f"{course_number}-{section} , Type: {class_type} , AS: {available_seats} - WL: {waiting_list_count} , {crn}")
               if ((section == "55") or (section == "56") or (section == "73") or (section == "97")):
                    print(f"\n\n\n\n\n {section} \n\n\n\n\n")


# def tt():
#      driver = webdriver.Chrome()
#      driver.get("https://registrar.kfupm.edu.sa/api/course-offering?term_code=202120&department_code=ICS")

#      for i in range(10000):
#           source = driver.page_source
#           soup = BeautifulSoup(source, "html.parser").text
#           soup_json = json.loads(soup)
#           for j in (12, 20):
#                course = soup_json["data"][j]
#                crn = course["crn"]
#                available_seats = course["available_seats"]
#                waiting_list_count = course["waiting_list_count"]
#                print("crn: " + str(crn), end=", ")
#                print("AS: " + str(available_seats), end=", ")
#                print("WL: " + str(waiting_list_count), end=f"         {i}")
#                if (available_seats != 0 or waiting_list_count != 0):
#                     print("\n\n\n\n\n")
#                else:
#                     print("")
#           time.sleep(10)
#           driver.refresh()