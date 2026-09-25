# importing libraries
import datetime
from datetime import date
from datetime import datetime
from tabulate import tabulate

# creating a login list
login_list = []

try:
    with open("user.txt", "r+") as file:
        for line in file:
            words = line.replace("\n", "").split(", ")

            username = words[0]
            password = words[1]

            login_details = username, password

            login_list.append(login_details)

except FileNotFoundError:
    print("The file that you are trying to open does not exist")


# while loop so user can only login if details are correct
while True:

    print("Please enter your username and password:\n")
    entered_username = input("Username:")
    entered_password = input("Password:")

    entered_login = entered_username, entered_password

    if entered_login in login_list:
        break

    else:
        print("Incorrect username or password. Please try again.\n")


def reg_user():
    """
    If the user is the admin, allows them to input a new username
    and password to register a new user.
    Confirms that the password is correct and then appends the
    text file user.txt to add the new login details.
    """

    existing_users = []

    with open("user.txt", "r") as file:
        for line in file:
            words = line.replace("\n", "").split(", ")

            usernames = words[0]

            existing_users.append(usernames)

    if entered_username == "admin":

        while True:

            print("New User Registration:\n")
            new_username = input("Username:")
            new_password = input("Password:")
            conf_password = input("Confirm Password:")

            # if the username already exists the user can retry
            if new_username in existing_users:
                print(
                    "\nUsername already exists. Would you like to try again?."
                )
                choice = input(
                    """1. Yes
                2. No"""
                )

                if choice == "No" or choice == "no" or choice == "2":
                    return

            else:
                break

        # confirm that both passwords entered match
        if new_password == conf_password:

            with open("user.txt", "a") as file:

                file.write(f"\n{new_username}, {new_password}")

            print("User successfully registered.")

        else:
            print("Passwords do not match. Please try again.\n")

    else:
        print("You have entered an invalid input. Please try again.")


def add_task():
    """
    Allows user to input the assigned username, title, description
    and due date of a task.
    Uses the datetime library to determine the date set and sets the
    status of the task to incomplete.
    Opens text file tasks.txt and adds the new task.
    """

    print("Please enter the following information.\n")

    task_username = input("Username task is assigned to:")
    task_title = input("The title of the task:")
    task_description = input("A description of the task:")
    task_due = input("The due date of the task:")

    today = date.today()
    current_date = today.strftime("%d %B %Y")
    task_set = current_date

    completed_status = False

    with open("tasks.txt", "a") as file:

        file.write(
            f"{task_username}, {task_title}, {task_description}, "
            f"{task_set}, {task_due}, {'Yes' if completed_status else 'No'}\n"
        )


def view_all():
    """
    Creates an empty list table and appends it by adding items from
    the text file tasks.txt.
    Uses the tabulate library to format the list as a table.
    """

    table = []

    try:
        with open("tasks.txt", "r+") as file:
            for line in file:
                words = line.replace("\n", "").split(", ")

                username = words[0]
                title = words[1]
                description = words[2]
                task_set = words[3]
                due_date = words[4]
                completed_status = words[5]

                row = [
                    username,
                    title,
                    description,
                    task_set,
                    due_date,
                    completed_status,
                ]

                table.append(row)

            print(
                tabulate(
                    table,
                    headers=[
                        "Username",
                        "Title",
                        "Description",
                        "Date Set",
                        "Date Due",
                        "Completed Status",
                    ],
                    tablefmt="fancy_grid",
                    maxcolwidths=[None, 40, 40, None, None, None],
                )
            )

    except FileNotFoundError:
        print("The file that you are trying to open does not exist")


def view_mine():
    """
    Opens text file tasks.txt and uses the tabulate library
    to create a table of all tasks assigned to the active
    user.
    If the user is assigned no tasks, a message informing
    of this appears.
    Allows the user to select a task to edit/mark complete.
    """

    table = []

    try:
        with open("tasks.txt", "r+") as file:
            for index, line in enumerate(file, start=1):
                words = line.replace("\n", "").split(", ")

                username = words[0]
                title = words[1]
                description = words[2]
                task_set = words[3]
                due_date = words[4]
                completed_status = words[5]

                if username == entered_username:

                    row = [
                        index,
                        username,
                        title,
                        description,
                        task_set,
                        due_date,
                        completed_status,
                    ]

                    table.append(row)

        if len(table) == 0:
            print("No tasks available.")

        else:
            print(
                tabulate(
                    table,
                    headers=[
                        "Task No.",
                        "Username",
                        "Title",
                        "Description",
                        "Date Set",
                        "Date Due",
                        "Completed Status",
                    ],
                    tablefmt="fancy_grid",
                    maxcolwidths=[None, None, 40, 40, None, None],
                )
            )

    except FileNotFoundError:
        print("The file that you are trying to open does not exist")

    while True:

        # choose to select a task or return to the main menu
        choice_1 = input(
            """
        1. Select a task
        -1. Return to menu
        """
        )

        if choice_1 == "-1":

            break

        elif choice_1 != "1":

            print("Invalid input. Please try again.")

        task_no = int(input("Enter the task number:"))

        with open("tasks.txt", "r") as file:

            for index, line in enumerate(file, start=1):

                if index == task_no:

                    words = line.replace("\n", "").split(", ")

                    username = words[0]
                    title = words[1]
                    description = words[2]
                    task_set = words[3]
                    due_date = words[4]
                    completed_status = words[5]

                    break

        if completed_status == "Yes":

            print(
                "The task has already been completed and so cannot be edited."
            )
            break

        # choose to edit the task or mark it as complete
        choice_2 = input(
            """
        1. Edit task
        2. Mark task as complete
        """
        )

        with open("tasks.txt", "r") as file:
            lines = file.readlines()

        if choice_2 == "1":

            with open("tasks.txt", "w") as file:

                for index, line in enumerate(lines, start=1):

                    if index != task_no:
                        file.write(line)
                    else:
                        new_username = input("Who is the task assigned to?")
                        new_due = input("What is the due date of the task?")

                        new_task = (
                            f"{new_username}, {title}, {description}, "
                            f"{task_set}, {new_due}, {completed_status}\n"
                        )

                        file.write(new_task)

                        print("Task successfully updated.")

        elif choice_2 == "2":

            with open("tasks.txt", "w") as file:

                for index, line in enumerate(lines, start=1):

                    if index != task_no:
                        file.write(line)

                    else:
                        completed_status = True

                        new_task = (
                            f"{username}, {title}, {description}, "
                            f"{task_set}, {due_date}, "
                            f"{'Yes' if completed_status else 'No'}\n"
                        )

                        file.write(new_task)

                        print("Task successfully updated.")

        else:
            print("\nInvalid input.")


def view_completed():
    """
    If the user is the admin, allows them to view a table
    of all completed tasks using the tabulate library.
    Opens text file tasks.txt and adds all items whereby the
    completed status is positive to the table.
    """

    if entered_username == "admin":

        table = []

        try:
            with open("tasks.txt", "r+") as file:
                for line in file:
                    words = line.replace("\n", "").split(", ")

                    username = words[0]
                    title = words[1]
                    description = words[2]
                    task_set = words[3]
                    due_date = words[4]
                    completed_status = words[5]

                    if completed_status == "Yes":

                        row = [
                            username,
                            title,
                            description,
                            task_set,
                            due_date,
                            completed_status,
                        ]

                        table.append(row)

            if len(table) == 0:
                print("No tasks available.")

            else:
                print(
                    tabulate(
                        table,
                        headers=[
                            "Username",
                            "Title",
                            "Description",
                            "Date Set",
                            "Date Due",
                            "Completed Status",
                        ],
                        tablefmt="fancy_grid",
                        maxcolwidths=[None, 40, 40, None, None, None],
                    )
                )

        except FileNotFoundError:
            print("The file that you are trying to open does not exist")


def delete_task():
    """
    If the user is the admin, displays a table of all tasks
    using the tabulate function, and prompts the user to select
    one to delete.
    Appends the text file tasks.txt so chosen task is deleted.
    """

    if entered_username == "admin":

        table = []

        try:
            with open("tasks.txt", "r+") as file:
                for line in file:
                    words = line.replace("\n", "").split(", ")

                    username = words[0]
                    title = words[1]
                    description = words[2]
                    task_set = words[3]
                    due_date = words[4]
                    completed_status = words[5]

                    row = [
                        username,
                        title,
                        description,
                        task_set,
                        due_date,
                        completed_status,
                    ]

                    table.append(row)

            print(
                tabulate(
                    table,
                    headers=[
                        "Username",
                        "Title",
                        "Description",
                        "Date Set",
                        "Date Due",
                        "Completed Status",
                    ],
                    tablefmt="fancy_grid",
                    maxcolwidths=[None, 40, 40, None, None, None],
                )
            )

            deleted = input(
                "What is the title of the task you wish to delete?"
            )

        except FileNotFoundError:
            print("The file that you are trying to open does not exist")

        try:
            with open("tasks.txt", "r") as file:
                lines = file.readlines()

            task_found = False

            with open("tasks.txt", "w") as file:
                for line in lines:
                    words = line.replace("\n", "").split(", ")
                    title = words[1]

                    if title != deleted:
                        file.write(line)

                    else:
                        task_found = True

            if task_found:
                print(f"Task {deleted} has been deleted.")

            else:
                print(f"Task {deleted} was not found.")

        except FileNotFoundError:
            print("The file that you are trying to open does not exist")

    else:
        print("You have entered an invalid input. Please try again")


def display_stats():
    """
    Prints the text files tasks_overview.txt and
    user_overview.txt so that the content is
    displayed.
    """

    try:
        print("\nTask Overview:\n")
        with open("tasks_overview.txt", "r") as file:
            print(file.read())

        print("\nUser Overview:\n")
        with open("user_overview.txt", "r") as file:
            print(file.read())

    except FileNotFoundError:
        print("\nError - please generate reports first.\n")


def generate_reports():
    """
    Creates text files tasks_overview.txt and
    user_overview.txt which contain information
    regarding the data in tasks.txt.
    """

    total_tasks = 0
    completed_track = 0
    incompleted_track = 0
    overdue = 0

    user_list = []

    with open("tasks.txt", "r") as file:
        all_tasks = file.readlines()

        for task in all_tasks:
            total_tasks += 1
            words = task.replace("\n", "").split(", ")

            if len(words) < 6:
                continue

            username = words[0]
            title = words[1]
            description = words[2]
            task_set = words[3]
            due_date = words[4]
            completed_status = words[5]

            if username not in user_list:
                user_list.append(username)

            due_date_formatted = datetime.strptime(due_date, "%d %b %Y")
            today = datetime.today()

            if completed_status == "Yes":
                completed_track += 1

            else:
                incompleted_track += 1

                if today > due_date_formatted:
                    overdue += 1

    # calculating statistics to display in text file
    perc_incomplete = (incompleted_track / total_tasks) * 100

    perc_overdue = (overdue / total_tasks) * 100

    with open("user.txt", "r") as file:
        total_users = len(file.readlines())

    with open("tasks_overview.txt", "w") as file:

        data = [
            ["Total tasks generated", total_tasks],
            ["Completed tasks", completed_track],
            ["Incomplete tasks", incompleted_track],
            ["Overdue tasks", overdue],
            ["Percentage Incomplete", perc_incomplete],
            ["Percentage Overdue", perc_overdue],
        ]

        table = tabulate(data, tablefmt="fancy_grid")

        file.write(table)

    user_table = []

    with open("user_overview.txt", "w") as file:

        file.write(f"Number of registered users: {total_users}\n")
        file.write(f"Number of tasks: {total_tasks}\n")

        for user in user_list:

            user_tasks = 0
            user_complete = 0
            user_incomplete = 0
            user_overdue = 0

            for line in all_tasks:
                words = line.replace("\n", "").split(", ")

                if len(words) < 6:
                    continue

                due_date = words[4]

                if words[0] == user:
                    user_tasks += 1

                    if words[5] == "Yes":
                        user_complete += 1

                    else:
                        user_incomplete += 1

                        due_date_formatted = datetime.strptime(
                            due_date, "%d %b %Y"
                        )
                        today = datetime.today()

                        if today > due_date_formatted:
                            user_overdue += 1

            if total_tasks > 0:
                perc_assigned = (user_tasks / total_tasks) * 100

            else:
                perc_assigned = 0

            if user_tasks > 0:

                perc_completed = (user_complete / user_tasks) * 100

                perc_incomplete = (user_incomplete / user_tasks) * 100

                perc_overdue = (user_overdue / user_tasks) * 100

            else:
                perc_completed = 0
                perc_incomplete = 0
                perc_overdue = 0

            row = [
                user,
                user_tasks,
                perc_assigned,
                perc_completed,
                perc_incomplete,
                perc_overdue,
            ]

            user_table.append(row)

    display_table = tabulate(
        user_table,
        headers=[
            "User",
            "Tasks assigned",
            "% Assigned",
            "% Completed",
            "% Incomplete",
            "% Overdue",
        ],
        tablefmt="fancy_grid",
    )

    with open("user_overview.txt", "a") as file:
        file.write(display_table)


# creating menus for the admin and other users
while True:

    if entered_username == "admin":

        menu = input(
            """\nSelect one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete tasks
ds - display statistics
gr - generate reports
e - exit
:\n """
        ).lower()

    else:
        menu = input(
            """\nSelect one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
:\n """
        ).lower()

    if menu == "r":

        reg_user()

    elif menu == "a":

        add_task()

    elif menu == "va":

        view_all()

    elif menu == "vm":

        view_mine()

    elif menu == "vc":

        view_completed()

    elif menu == "del":

        delete_task()

    elif menu == "ds":

        display_stats()

    elif menu == "gr":

        generate_reports()

    elif menu == "e":
        print("Goodbye!")
        break

    else:
        print("You have entered an invalid input. Please try again")
