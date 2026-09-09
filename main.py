#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
from datetime import date

from business.school import School
from models.address import Address
from models.course import Course
from models.student import Student
from models.teacher import Teacher

def is_entry_int_ok(user_input, min_int, max_int):
    """ Fonction qui vérifie la saisie d'un numérique, entre min_int et max_int    """
    cleaned_user_input = user_input.strip()
    if not cleaned_user_input.isdigit():
        return False
    if int(cleaned_user_input) < min_int or int(cleaned_user_input) > max_int:
        return False
    return True

def input_principal_menu(options):
    """ Fonction qui demande à l'utilisateur de choisir une action
        -Le choix 0 permet toujours de quitter.
        -Les options fournies en paramètre commencent à 1
    """
    menu = "Bonjour. Menu :\n"
    menu += " 0 Quitter le programme\n"

    for numero, option in enumerate(options, start=1):
        menu += f" {numero} {option}\n"

    input_menu = input(menu)

    while not is_entry_int_ok(input_menu, 0, len(options)):
        input_menu = input("Saisie incorrecte. Merci de recommencer : ")

    return int(input_menu)

def menu_gestion_student():
    print("TODO Ici on fera le menu spécifique à la gestion des étudiants")

def menu_gestion_teacher():
    print("TODO Ici on fera le menu spécifique à la gestion des enseignants")

def menu_gestion_courses():
    print("TODO Ici on fera le menu spécifique à la gestion des cours")

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

    # Menu de l'application => En test dans un premier temps (à modifier quand je gérerai la connection utilisateur)
    menu = [
        "Afficher la liste des cours",
        "Afficher la liste des cours suivis par un étudiant",
        "Afficher la liste des étudiants",
        "Afficher la liste des professeurs",
        "Créer un cours",
        "Créer un étudiant",
        "Créer un enseignant"
    ]
    choix = -1
    # On ne sort pas du programme tant que l'utilisateur ne l'a pas spécifié
    while (choix != 0):
        # On récupère le choix de l'utilisateur par rapport au menu
        choix = input_principal_menu(menu)
        # Affichage des cours (avec enseignants et élèves)
        if (choix == 1):
            print("Liste des cours \n")
            school.display_courses_list()

        # Affichage des cours pour un étudiant donné (par son numéro)
        elif (choix == 2):
            print("Méthode non écrite")

        # Affichage de la liste des étudiants
        elif (choix == 3):
            print("Liste des étudiants \n")
            school.display_students_list()

        # Affichage de la liste des enseignants
        elif (choix == 4):
            print("Liste des enseignants \n")
            school.display_teachers_list()

        # TODO Modifier pour faire Gestion des cours
        elif (choix == 5):
            print("Création d'un cours de test \n")
            # test de la création d'un cours (ok)
            teacher = Teacher('Marie', 'Curie', 31, date(2023, 9, 4))
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
            school.add_course(course)

        # TODO Modifier pour faire Gestion des étudiants (ajout, modif, sup)
        elif (choix == 6):
            print("Création d'un étudiant de test\n")
            # test de la création d'un étudiant
            student: Student = Student('André', 'Dupont', 14)
            student.address = Address('36 rue des dunes de sables', 'Labenne', 40100)
            school.add_student(student)

        # TODO Modifier pour faire Gestion des enseignants (ajout, modif, sup)
        elif (choix == 7):
            print("Création d'un enseignant de test \n")
            # test de la création d'un enseignant
            teacher: Teacher = Teacher('Miranda', 'Bailey', 25, date(2023, 9, 4))
            teacher.address = Address('276 rue des camélias', 'Bayonne', 64100)
            school.add_teacher(teacher)
        elif (choix == 0):
            print("Merci, et à bientôt! ")


    # affichage des cours 1, 2 et 3
    # print(school.get_course_by_id(1))
    # print(school.get_course_by_id(2))
    # print(school.get_course_by_id(9))


if __name__ == '__main__':
    main()
