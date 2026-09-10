#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
import re

from business.school import School
from models import course
from models.address import Address
from models.course import Course
from models.student import Student
from models.teacher import Teacher
from datetime import datetime

def input_bool(prompt) -> bool:
    """Fonction qui attend strictement oui ou non dans une saisie et renvoie booléen true/false correspondant"""
    text: str = ""
    while text not in ["oui", "non"]:
        text = input(prompt).lower().strip()
    return text == "oui"

def get_date_input(prompt):
    """Demande à l'utilisateur de saisir une date valide."""
    while True:
        input_user = input(prompt).strip()

        try:
            date = datetime.strptime(input_user, "%d/%m/%Y")
            return date

        except ValueError:
            print("Saisie incorrecte. Merci de recommencer.")

def get_address_input(prompt):
    """Demande à l'utilisateur de saisir une adresse. Accepte les espaces, les points, les chiffres..."""
    while True:
        input_user = input(prompt).strip()

        if input_user and all(
            char.isalnum() or char in " -'" for char in input_user
        ):
            return input_user

        print("Saisie incorrecte. Merci de recommencer.")

def get_str_input(prompt):
    """Demande à l'utilisateur de saisir une chaîne alphanumérique. Sans espaces, ni tiret, ni chiffres..."""
    while True:
        input_user = input(prompt).strip()

        if input_user.isalpha():
            return input_user

        print("Saisie incorrecte. Merci de recommencer.")

def get_str_postal_code(prompt):
    """Demande à l'utilisateur de saisir un code postal français valide."""
    postal_code = input(prompt).strip()

    while len(postal_code) != 5 or not postal_code.isdigit():
        postal_code = input("Saisie incorrecte. Merci de recommencer : ").strip()

    return postal_code

def get_int_input(prompt, min_int, max_int):
    """Demande à l'utilisateur de saisir un entier compris entre min_int et max_int."""
    user_input = input(prompt).strip()

    while not user_input.isdigit() or not min_int <= int(user_input) <= max_int:
        user_input = input(
            "Saisie incorrecte. Merci de recommencer : "
        ).strip()

    return int(user_input)

def input_menu(items, multiline = False):
    """Demande à l'utilisateur de choisir un item dans un menu.
    Le choix 0 permet toujours de quitter.
    Les options fournies en paramètre commencent à 1.

    param items : liste des options du menu
    param multiline : affiche le menu sur une seule ligne si False.
    """
    separator = "\n" if multiline else " "
    menu = "Menu :\n"
    menu += "- 0 Quitter"
    menu += separator
    for numero, option in enumerate(items, start=1):
        menu += f"- {numero} {option} {separator}"
    menu += "\n"
    return get_int_input(menu, 0, len(items))

def menu_gestion_student(school):
    sous_menu_gestion_students = [
        "Créer un étudiant",
        "Modifier un étudiant",
        "Supprimer un étudiant"
    ]
    choix_menu_stud = -1
    # On ne sort pas du programme tant que l'utilisateur ne l'a pas spécifié
    while (choix_menu_stud != 0):
        # On affiche la liste des étudiants
        print("Liste des étudiants\n")
        list_students_show = school.get_students_list()
        for numero, student in enumerate(list_students_show, start=1):
            print(f"{numero} - {student}")
        # On récupère le choix de l'utilisateur par rapport au sous-menu
        choix_menu_stud = input_menu(sous_menu_gestion_students)
        if (choix_menu_stud == 1):
            print("*****************Créer un étudiant")
            #On demande à l'utilisateur les informations pour cet étudiant à créer
            last_name = get_str_input("Entrez le nom de cet étudiant : ")
            first_name = get_str_input("Entrez le prénom de cet étudiant : ")
            age = get_int_input("Entrez l'âge de cet étudiant : ", 0, 100)
            student_to_create: Student = Student(first_name, last_name, age)
            is_student_address = input_bool("Est ce que vous souhaitez entrer l'adresse de cet étudiant ?")
            if (is_student_address):
                street = get_address_input("Entrez l'adresse : ")
                city = get_str_input("Entrez la ville : ")
                postal_code = get_str_postal_code("Entrez le code postal : ")
                student_to_create.address = Address(street, city, postal_code)
            school.add_student(student_to_create)
        elif (choix_menu_stud == 2):
            print("*****************Modifier un étudiant")
            numero_line_student = get_int_input("Entrez le numéro de ligne de l'étudiant à modifier : ",1, len(list_students_show))
            student_sans_add = list_students_show[numero_line_student - 1]
            #On récupère l'étudiant complet à partir du numéro d'étudiant(sinon on perd l'address que je n'ai pas remonté dans la liste...)
            print(f"On va chercher l'étudiant numéro {student_sans_add.student_nbr}")
            student = school.get_student_by_nbr(student_sans_add.student_nbr)

            if (student is not None):
                student.last_name = get_str_input("Entrez le nom de cet étudiant : ")
                student.first_name = get_str_input("Entrez le prénom de cet étudiant : ")
                student.age = get_int_input("Entrez l'âge de cet étudiant : ", 0, 100)
                is_student_address = input_bool("Est ce que vous souhaitez ajouter/modifier l'adresse de cet étudiant ?")
                # Si l'utilisateur a demandé à modifier l'adresse (non nulle)
                if (is_student_address and student.address is not None):
                    student.address.street = get_address_input("Entrez l'adresse : ")
                    student.address.city = get_str_input("Entrez la ville : ")
                    student.address.postal_code = get_str_postal_code("Entrez le code postal : ")
                # Si l'utilisateur a demandé à ajouter une adresse (adresse nulle)
                elif (is_student_address and student.address is None):
                    street = get_address_input("Entrez l'adresse : ")
                    city = get_str_input("Entrez la ville : ")
                    postal_code = get_str_postal_code("Entrez le code postal : ")
                    student.address = Address(street, city, postal_code)
                school.update_student(student)
            else:
                print("Erreur il n'a pas été possible de récupérer l'étudiant correspondant à ce numéro de ligne")
        elif (choix_menu_stud == 3):
            print("*****************Supprimer un étudiant")
            numero_line_student = get_int_input("Entrez le numéro de ligne de l'étudiant à supprimer : ", 1, len(list_students_show))
            student_sans_add = list_students_show[numero_line_student - 1]
            # On récupère l'étudiant complet à partir du numéro d'étudiant(sinon on perd l'address que je n'ai pas remonté dans la liste...)
            print(f"On va chercher l'étudiant numéro {student_sans_add.student_nbr}")
            student = school.get_student_by_nbr(student_sans_add.student_nbr)
            # On demande confirmation avant la suppression
            confirmation_delete = input_bool(f"Etes vous sur de vouloir supprimer cet étudiant : {student.last_name} {student.first_name} ?")

            # On va supprimer cet étudiant
            if (student is not None and confirmation_delete):
                school.delete_student(student)
            elif (not confirmation_delete):
                print("La suppression a bien été annulée")
            else:
                print("Erreur il n'a pas été possible de récupérer l'étudiant correspondant à ce numéro de ligne")
        elif (choix_menu_stud == 0):
            print("Retour au menu précédent")

#TODO Fonction non terminée j'ai pas fini d'implémenter les formulaires pour création/modification/suppression d'un enseignant
def menu_gestion_teacher(school):
    sous_menu_gestion_teachers = [
        "Créer un enseignant",
        "Modifier un enseignant",
        "Supprimer un enseignant"
    ]
    choix_menu_teach = -1
    # On ne sort pas du programme tant que l'utilisateur ne l'a pas spécifié
    while (choix_menu_teach != 0):
        # On affiche la liste des enseignants
        print("Liste des enseignants\n")
        school.display_teachers_list()
        # On récupère le choix de l'utilisateur par rapport au sous-menu
        choix_menu_teach = input_menu(sous_menu_gestion_teachers)
        if (choix_menu_teach == 1):
            print("*****************Créer un enseignant")
            print("Fonction testée en test, mais formulaire non encore implémenté")
            # test de la création d'un enseignant (ok)
            # teacher: Teacher = Teacher('Miranda', 'Bailey', 25, date(2023, 9, 4))
            # teacher.address = Address('276 rue des camélias', 'Bayonne', 64100)
            # school.add_teacher(teacher)
        elif (choix_menu_teach == 2):
            print("*****************Modifier un enseignant")
            print("Fonction testée en test, mais formulaire non encore implémenté")
            # teacher = school.get_teacher_by_id(52)

            # On va tester la modification de cet enseignant (ok)
            # teacher.last_name = "Greys"
            # teacher.first_name = "Meredith"
            # teacher.address.street = "277 rue des roses"
            # school.update_teacher(teacher)
        elif (choix_menu_teach == 3):
            print("*****************Supprimer un enseignant")
            print("Fonction testée en test, mais formulaire non encore implémenté")
            # On va tester la suppression de cet enseignant (ok)
            # school.delete_teacher(teacher)
        elif (choix_menu_teach == 0):
            print("Retour au menu précédent")

#TODO Fonction non terminée j'ai pas fini d'implémenter les formulaires pour création/modification/suppression d'un cours
def menu_gestion_courses(school):
    sous_menu_gestion_courses = [
        "Créer un cours",
        "Modifier un cours",
        "Supprimer un cours"
    ]
    choix_menu_course = -1
    # On ne sort pas du programme tant que l'utilisateur ne l'a pas spécifié
    while (choix_menu_course != 0):
        # On affiche la liste des cours
        print("Liste des cours \n")
        school.display_courses_list()
        # On récupère le choix de l'utilisateur par rapport au sous-menu
        choix_menu_course = input_menu(sous_menu_gestion_courses)
        if (choix_menu_course == 1):
            print("*****************Créer un cours")

            # On demande à l'utilisateur les informations pour ce cours à créer
            name = get_str_input("Entrez le nom de ce cours : ")
            start_date = get_date_input("Entrez la date de début du cours : ")
            end_date = get_date_input("Entrez la date de fin du cours : ")
            course_to_create: Course = Course(name, start_date, end_date)
            # On affiche la liste des enseignants
            print("Liste des enseignants\n")
            list_teachers_show = school.get_teachers_list()
            for numero, teacher in enumerate(list_teachers_show, start=1):
                print(f"{numero} - {teacher}")
            numero_line_teacher = get_int_input("Entrez le numéro de ligne de l'enseignant pour ce cours : ", 1, len(list_teachers_show))
            # On récupère l'enseignant
            teacher = list_teachers_show[numero_line_teacher - 1]
            course_to_create.teacher = teacher
            school.add_course(course_to_create)
        elif (choix_menu_course == 2):
            print("*****************Modifier un cours")
            print("Fonctionnalité non encore implémentée")
        elif (choix_menu_course == 3):
            print("*****************Supprimer un cours")
            print("Fonctionnalité non encore implémentée")
        elif (choix_menu_course == 0):
            print("Retour au menu précédent")

def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # initialisation d'un ensemble de cours, enseignants et élèves composant l'école
    #school.init_static()

    # initialise les données à partir de la base de données
    school.init_bd()

    # Menu de l'application => En test dans un premier temps (à modifier quand je gérerai la connection utilisateur)
    menu = [
        "Liste cours",
        "Liste cours suivis par un étudiant",
        "Liste étudiants",
        "Liste enseignants",
        "Gestion cours",
        "Gestion étudiants",
        "Gestion enseignants"
    ]
    choix = -1
    # On ne sort pas du programme tant que l'utilisateur ne l'a pas spécifié
    while (choix != 0):
        # On récupère le choix de l'utilisateur par rapport au menu
        choix = input_menu(menu)
        # Affichage des cours (avec enseignants et élèves)
        if (choix == 1):
            print("*******************Liste des cours \n")
            school.display_courses_list()

        # Affichage des cours pour un étudiant donné (par son numéro)
        elif (choix == 2):
            # On affiche la liste des étudiants
            print("*******************Liste des étudiants\n")
            list_students_show = school.get_students_list()
            for numero, student in enumerate(list_students_show, start=1):
                print(f"{numero} - {student}")

            numero_line_student = get_int_input("Entrez le numéro de ligne de l'étudiant dont vous souhaitez connaître les cours : ", 1, len(list_students_show))
            student_sans_add = list_students_show[numero_line_student - 1]
            # Test de lecture d'un étudiant (avec les cours auquel il s'est inscrit)
            student: Student = school.get_student_by_nbr(student_sans_add.student_nbr)
            # On va récupérer les cours auquel il s'est inscrit
            list_courses_id = school.get_courses_by_student(student)
            # Pour chaque id on récupère l'objet cours
            for id in list_courses_id:
                cours: Course = school.get_course_by_id(id)
                student.add_course(cours)
            print("\n", student)
            print("Cours suivis par cet étudiant : ")
            for cours in student.courses_taken:
                print(f" - {cours}")

        # Affichage de la liste des étudiants
        elif (choix == 3):
            print("*******************Liste des étudiants \n")
            school.display_students_list()

        # Affichage de la liste des enseignants
        elif (choix == 4):
            print("*******************Liste des enseignants \n")
            school.display_teachers_list()

        # Gestion des cours
        elif (choix == 5):
            menu_gestion_courses(school)

        # Gestion des étudiants
        elif (choix == 6):
            menu_gestion_student(school)

        # Gestion des enseignants
        elif (choix == 7):
            menu_gestion_teacher(school)

        # Sortie de l'application
        elif (choix == 0):
            print("Merci, et à bientôt! ")

    # affichage des cours 1, 2 et 3
    # print(school.get_course_by_id(1))
    # print(school.get_course_by_id(2))
    # print(school.get_course_by_id(9))

if __name__ == '__main__':
    main()
