#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
import re
from datetime import date
from xmlrpc.client import MAXINT

from business.school import School
from models.address import Address
from models.course import Course
from models.student import Student
from models.teacher import Teacher

def input_bool(prompt) -> bool:
    """Fonction qui attend strictement oui ou non dans une saisie et renvoie booléen true/false correspondant"""
    text: str = ""
    while text not in ["oui", "non"]:
        text = input(prompt).lower().strip()
    return text == "oui"

def is_saisie_str_ok(saisie):
    """Vérifie si une saisie chaine est correcte (Aide chatgpt pour regex, je suis pas très douée avec les regex)"""
    cleaned_saisie = saisie.strip()
    return bool(re.fullmatch(r"[A-Za-zÀ-ÿ0-9 ]+", cleaned_saisie))

def get_str_input(prompt):
    """Fonction qui demande à l'utilisateur de saisir une chaine"""
    input_user = input(prompt)
    while not is_saisie_str_ok(input_user):
        input_user = input("Saisie incorrecte. Merci de recommencer : ")
    return input_user

def is_saisie_postal_code_ok(saisie):
    """Vérifie qu'une saisie correspond au format d'un code postal français."""
    cleaned_code_postal = saisie.strip()
    return len(cleaned_code_postal) == 5 and cleaned_code_postal.isdigit()

def get_str_postal_code(prompt):
    """Fonction qui demande à l'utilisateur de saisir un code postal français"""
    input_user = input(prompt)
    while not is_saisie_postal_code_ok(input_user):
        input_user = input("Saisie incorrecte. Merci de recommencer : ")
    return input_user

def get_int_input(prompt, min_int, max_int):
    """Fonction qui demande à l'utilisateur de saisir un int"""
    input_int = input(prompt)
    while not is_entry_int_ok(input_int, min_int, max_int):
        input_int = input("Saisie incorrecte. Merci de recommencer : ")
    return int(input_int)

def is_entry_int_ok(user_input, min_int, max_int):
    """ Fonction qui vérifie la saisie d'un numérique, entre min_int et max_int    """
    cleaned_user_input = user_input.strip()
    if not cleaned_user_input.isdigit():
        return False
    if int(cleaned_user_input) < min_int or int(cleaned_user_input) > max_int:
        return False
    return True

def input_menu(items):
    """ Fonction qui demande à l'utilisateur de choisir un item dans un menu passé en paramètre (tableau)
        -Le choix 0 permet toujours de quitter.
        -Les options fournies en paramètre commencent à 1
    """
    menu = "Menu :\n"
    menu += " - 0 Quitter "

    for numero, option in enumerate(items, start=1):
        menu += f"- {numero} {option} "
    menu += "\n"
    input_menu = input(menu)

    while not is_entry_int_ok(input_menu, 0, len(items)):
        input_menu = input("Saisie incorrecte. Merci de recommencer : ")

    return int(input_menu)

def menu_gestion_student(school):
    sous_menu_gestion_students = [
        "Créer un étudiant",
        "Modifier un étudiant",
        "Supprimer un étudiant"
    ]
    choix = -1
    # On ne sort pas du programme tant que l'utilisateur ne l'a pas spécifié
    while (choix != 0):
        # On affiche la liste des étudiants
        print("Liste des étudiants\n")
        list_students_show = school.get_students_list()
        for numero, student in enumerate(list_students_show, start=1):
            print(f"{numero} - {student}")
        # On récupère le choix de l'utilisateur par rapport au sous-menu
        choix = input_menu(sous_menu_gestion_students)
        if (choix == 1):
            print("**************************Création d'un étudiant")
            #On demande à l'utilisateur les informations pour cet étudiant à créer
            last_name = get_str_input("Entrez le nom de cet étudiant : ")
            first_name = get_str_input("Entrez le prénom de cet étudiant : ")
            age = get_int_input("Entrez l'âge de cet étudiant : ", 0, 100)
            student_to_create: Student = Student(first_name, last_name, age)
            is_student_address = input_bool("Est ce que vous souhaitez entrer l'adresse de cet étudiant ?")
            if (is_student_address):
                street = get_str_input("Entrez l'adresse : ")
                city = get_str_input("Entrez la ville : ")
                postal_code = get_str_postal_code("Entrez le code postal : ")
                student_to_create.address = Address(street, city, postal_code)
            school.add_student(student_to_create)
        elif (choix == 2):
            print("Modifier un étudiant")
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
                    student.address.street = get_str_input("Entrez l'adresse : ")
                    student.address.city = get_str_input("Entrez la ville : ")
                    student.address.postal_code = get_str_postal_code("Entrez le code postal : ")
                # Si l'utilisateur a demandé à ajouter une adresse (adresse nulle)
                elif (is_student_address and student.address is None):
                    street = get_str_input("Entrez l'adresse : ")
                    city = get_str_input("Entrez la ville : ")
                    postal_code = get_str_postal_code("Entrez le code postal : ")
                    student.address = Address(street, city, postal_code)
                school.update_student(student)
            else:
                print("Erreur il n'a pas été possible de récupérer l'étudiant correspondant à ce numéro de ligne")
        elif (choix == 3):
            print("Supprimer un étudiant")
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
        elif (choix == 0):
            print("Retour au menu précédent")

def menu_gestion_teacher(school):
    sous_menu_gestion_teachers = [
        "Créer un enseignant",
        "Modifier un enseignant",
        "Supprimer un enseignant"
    ]
    choix = -1
    # On ne sort pas du programme tant que l'utilisateur ne l'a pas spécifié
    while (choix != 0):
        # On affiche la liste des enseignants
        print("Liste des enseignants\n")
        school.display_teachers_list()
        # On récupère le choix de l'utilisateur par rapport au sous-menu
        choix = input_menu(sous_menu_gestion_teachers)
        if (choix == 1):
            print("Créer un enseignant")

            # test de la création d'un enseignant (ok)
            # teacher: Teacher = Teacher('Miranda', 'Bailey', 25, date(2023, 9, 4))
            # teacher.address = Address('276 rue des camélias', 'Bayonne', 64100)
            # school.add_teacher(teacher)
        elif (choix == 2):
            print("Modifier un enseignant")

            # teacher = school.get_teacher_by_id(52)

            # On va tester la modification de cet enseignant (ok)
            # teacher.last_name = "Greys"
            # teacher.first_name = "Meredith"
            # teacher.address.street = "277 rue des roses"
            # school.update_teacher(teacher)
        elif (choix == 3):
            print("Supprimer un enseignant")
            # On va tester la suppression de cet enseignant (ok)
            # school.delete_teacher(teacher)
        elif (choix == 0):
            print("Retour au menu précédent")

def menu_gestion_courses(school):
    sous_menu_gestion_courses = [
        "Créer un cours",
        "Modifier un cours",
        "Supprimer un cours"
    ]
    choix = -1
    # On ne sort pas du programme tant que l'utilisateur ne l'a pas spécifié
    while (choix != 0):
        # On affiche la liste des cours
        print("Liste des cours \n")
        school.display_courses_list()
        # On récupère le choix de l'utilisateur par rapport au sous-menu
        choix = input_menu(sous_menu_gestion_courses)
        if (choix == 1):
            print("Créer un cours")

            # test de la création d'un cours (ok)
            """teacher = Teacher('Marie', 'Curie', 31, date(2023, 9, 4))
            teacher.id = 4
            student: Student = Student('Valérie', 'Dumont', 13)
            student.id = 2
            course = Course(
                "Python",
                date(2026, 6, 22),
                date(2026, 6, 29),
            )
            course.teacher = teacher
            course.student = [student]
            school.add_course(course)"""
        elif (choix == 2):
            print("Modifier un cours")
        elif (choix == 3):
            print("Supprimer un cours")
        elif (choix == 0):
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

    #Affichage d'un enseignant pour test (ok)
    #print("Affichage de l'enseignant 51 pour test")
    #teacher = school.get_teacher_by_id(51)
    #print(teacher)
    #exit(0)

    # Affichage d'un étudiant pour test (ok)
    # print("Affichage de l'étudiant 87 pour test")
    # student = school.get_student_by_nbr(87)
    # print(student)
    # exit(0)

    # Affichage d'un cours pour test
    # print("Affichage du cours 24 Java")
    # courstest = school.get_course_by_id(24)
    # print(courstest)
    # exit(0)

    # Menu de l'application => En test dans un premier temps (à modifier quand je gérerai la connection utilisateur)
    menu = [
        "Liste des cours",
        "Liste des cours suivis par un étudiant",
        "Liste des étudiants",
        "Liste des enseignants",
        "Gestion des cours",
        "Gestion des étudiants",
        "Gestion des enseignants"
    ]
    choix = -1
    # On ne sort pas du programme tant que l'utilisateur ne l'a pas spécifié
    while (choix != 0):
        # On récupère le choix de l'utilisateur par rapport au menu
        choix = input_menu(menu)
        # Affichage des cours (avec enseignants et élèves)
        if (choix == 1):
            print("Liste des cours \n")
            school.display_courses_list()

        # Affichage des cours pour un étudiant donné (par son numéro)
        elif (choix == 2):
            print("Affichage des cours pour un étudiant donné : Méthode non écrite")

        # Affichage de la liste des étudiants
        elif (choix == 3):
            print("Liste des étudiants \n")
            school.display_students_list()

        # Affichage de la liste des enseignants
        elif (choix == 4):
            print("Liste des enseignants \n")
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
