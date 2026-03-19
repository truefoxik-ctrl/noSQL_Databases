from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://158.160.227.232:27017/')
db = client['grades_stud']
collection = db['grades_stud']

def insert_document():
    print("\n--- Добавление записи ---")

    print("Данные о студенте:")
    gradebook = input("(Зачётная книжка) Gradebook: ")
    idcard = input("Номер студенческого билета (IDcard): ")
    full_name = input("ФИО (full_name): ")
    faculty = input("Факультет (faculty): ")

    student = {
        "gradebook": gradebook,
        "IDcard": idcard,
        "full_name": full_name,
        "faculty": faculty
    }

    courses = []
    print("\nКурсы:")
    while True:
        course_name = input("Название курса: ")
        if course_name.lower() == 'стоп':
            break
        try:
            term = int(input(f"Семестр прохождения курса '{course_name}': "))
        except ValueError:
            print("Некорректный ввод семестра, используется 1")
            term = 1
        courses.append({
            "name": course_name,
            "term": term
        })

    print("\nОценка за курс:")
    if courses:
        print("Доступные курсы для оценки:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['name']}")
        try:
            course_choice = int(input("Выберите номер курса для оценки: ")) - 1
            if 0 <= course_choice < len(courses):
                selected_course = courses[course_choice]['name']
            else:
                print("Неверный выбор, используется первый курс")
                selected_course = courses[0]['name']
        except ValueError:
            print("Неверный ввод, используется первый курс")
            selected_course = courses[0]['name']
    else:
        selected_course = input("Название курса для оценки: ")

    try:
        grade = int(input("Оценка (1–10): "))
        if grade < 1 or grade > 10:
            print("Неверный диапазон оценки")
    except ValueError:
        print("Некорректная оценка")

    grades_data = {
        "course": selected_course,
        "grade": grade
    }

    document = {
        "student": student,
        "courses": courses,
        "grades": grades_data
    }

    result = collection.insert_one(document)
    print(f"Запись '{full_name}' добавлена с ID: {result.inserted_id}")
    print("Структура документа:")
    print(document)

def find_documents():
    print("\n--- Поиск документов ---")
    field = input("Поле для поиска (или Enter для всех): ")
    value = input("Значение для поиска (или Enter для всех): ")
    query = {}
    if field and value:
        query[field] = value
    documents = collection.find(query)
    for doc in documents:
        print(doc)

def update_document():
    print("\n--- Обновление документа ---")
    doc_id = input("ID документа для обновления: ")
    field = input("Поле для обновления: ")
    new_value = input("Новое значение: ")
    result = collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": {field: new_value}}
    )
    if result.modified_count:
        print("Документ обновлён")
    else:
        print("Документ не найден или не изменён")

def delete_document():
    print("\n--- Удаление документа ---")
    doc_id = input("ID документа для удаления: ")
    result = collection.delete_one({"_id": ObjectId(doc_id)})
    if result.deleted_count:
        print("Документ удалён")
    else:
        print("Документ не найден")

def main_menu():
    while True:
        print("\n" + "="*40)
        print("КОНСОЛЬНЫЙ ИНТЕРФЕЙС ДЛЯ MongoDB")
        print("="*40)
        print("1. Добавить запись")
        print("2. Найти запись")
        print("3. Обновить запись")
        print("4. Удалить запись")
        print("5. Показать все коллекции")
        print("6. Выйти")
        print("-"*40)
        choice = input("Выберите действие (1–6): ")
        if choice == '1':
            insert_document()
        elif choice == '2':
            find_documents()
        elif choice == '3':
            update_document()
        elif choice == '4':
            delete_document()
        elif choice == '5':
            print("Коллекции в базе:", db.list_collection_names())
        elif choice == '6':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    try:
        client.admin.command('ping')
        print("Успешное подключение к MongoDB!")
        main_menu()
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    finally:
        client.close()