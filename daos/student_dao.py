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
        try:
            with Dao.connection.cursor() as cursor:
                # On doit créer en premier la personne, puis récupérer l'id et ensuite créer l'étudiant relié à l'id de la personne
                if (student.address is None):
                    sql = "INSERT INTO person(first_name, last_name, age) VALUES (%s, %s, %s) "
                    cursor.execute(sql, (student.first_name, student.last_name, student.age))
                else:
                    sql = "INSERT INTO person(first_name, last_name, age, id_address) VALUES (%s, %s, %s, %s) "
                    cursor.execute(sql, (student.first_name, student.last_name, student.age, student.address.id))

                # On récupère l'identifiant de la personne qui vient d'être créé
                id_person_created = cursor.lastrowid

                # On crée ensuite l'étudiant correspondant à cette personne
                sql = "INSERT INTO student(student_nbr, id_person) VALUES (%s, %s) "
                cursor.execute(sql, (id_person_created,id_person_created))

                # On récupère l'identifiant de l'étudiant qui vient d'être créé
                student.student_nbr = cursor.lastrowid

                # On commit
                Dao.connection.commit()
            return student.id
        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return 0

    # TODO Méthode à implémenter
    def read(self, student_nbr: int) -> Optional[Student]:
        """Renvoit le student correspondant à l'entité dont l'id est student_nbr
           (ou None s'il n'a pu être trouvé)"""
        return None

    def read_all(self):
        """Renvoit la liste des cours """
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
        """Supprime en BD l'entité Student correspondant à student

        :param student: student dont l'entité Student correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """

        return True
