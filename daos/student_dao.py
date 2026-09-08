# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""

from models.student import Student
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class StudentDao(Dao[Student]):

    # TODO Méthode à implémenter
    def create(self, student: Student) -> int:
        """Crée en BD l'entité Student correspondant au Student student

        :param student: à créer sous forme d'entité Student en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """

        return 0

    # TODO Méthode à implémenter
    def read(self, id_student: int) -> Optional[Student]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        return None

    def read_all(self):
        """Renvoit la liste des cours """
        student: Optional[Student]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT student.student_nbr, student.id_person, person.first_name, person.last_name, person.age, person.id_address FROM student JOIN person ON student.id_person = person.id_person "
            cursor.execute(sql)
            students_lignes_sql = cursor.fetchall()
            students_objets = []
            #print("Nombre de résultats :", len(students_lignes_sql))
            #print("Résultats :", students_lignes_sql)
            #print(f"on va afficher les résultats pour cette requête {sql} ")

            for s in students_lignes_sql:
                #print(s)
                student = Student(s['first_name'], s['last_name'], s['age'])
                student.student_nbr = s['student_nbr']
                students_objets.append(student)

        return students_objets

    # TODO Méthode à implémenter
    def update(self, student: Student) -> bool:
        """Met à jour en BD l'entité Student correspondant à student, pour y correspondre

        :param student: student déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """

        return True

    # TODO Méthode à implémenter
    def delete(self, student: Student) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """

        return True
