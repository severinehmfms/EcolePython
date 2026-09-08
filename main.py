#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from business.school import School


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

    # affiche la liste des étudiants
    print("Liste des étudiants \n")
    school.display_students_list()

    # affichage de la liste des cours, leur enseignant et leurs élèves
    print("Liste des cours \n")
    school.display_courses_list()

    # affichage de la liste des enseignants
    print("Liste des enseignants \n")
    school.display_teachers_list()

    # affichage des cours 1, 2 et 3
    print(school.get_course_by_id(1))
    print(school.get_course_by_id(2))
    print(school.get_course_by_id(9))


if __name__ == '__main__':
    main()
