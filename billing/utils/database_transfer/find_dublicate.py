import csv


def check_unique_login(csv_filepath):
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        logins = {}
        duplicates = []

        for row in reader:
            login = row[9]
            if login in logins:
                duplicates.append(login)
            else:
                logins[login] = 1

        return duplicates


duplicates = check_unique_login('utils/database_transfer/csv/users_utf.csv')

print(duplicates)
