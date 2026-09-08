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
                student.student_nbr = cursor.lastrowid

                # On crée ensuite l'étudiant correspondant à cette personne
                sql = "INSERT INTO student(student_nbr, id_person) VALUES (%s, %s) "
                cursor.execute(sql, (student.student_nbr,student.student_nbr))

                # On commit
                Dao.connection.commit()
            return student.student_nbr

        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return 0

    def read(self, student_nbr: int) -> Optional[Student]:
        """Renvoie le student correspondant à l'entité dont l'id est student_nbr
           (ou None s'il n'a pu être trouvé)"""
        student: Optional[Student]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT student.student_nbr, student.id_person, person.first_name, person.last_name, person.age, person.id_address FROM student JOIN person ON student.id_person = person.id_person WHERE student_nbr=%s"
            cursor.execute(sql, (student_nbr,))
            record = cursor.fetchone()
        if record is not None:
            student = Student(record['first_name'], record['last_name'], record['age'])
            student.student_nbr = record['student_nbr']
        else:
            student = None

        return student


    def read_all(self):
        """Renvoie la liste des cours """
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

    def update(self, student: Student) -> bool:
        """Met à jour en BD l'entité Student correspondant à student, pour y correspondre

        :param student: student déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:

                # On va d'abord récupérer l'id de la personne qui correspond à cet étudiant
                sql = "SELECT id_person FROM student WHERE student_nbr = %s"
                cursor.execute(sql, (student.student_nbr,))

                result = cursor.fetchone()

                if result is None:
                    print("Erreur lors de la récupération de l'id de la personne correspondant à cet étudiant")
                    return False

                id_person = result['id_person']

                #On modifie la personne correspondant à cet étudiant
                if (student.address is None):
                    sql = "UPDATE person SET first_name=%s, last_name=%s, age=%s WHERE id_person=%s "
                    cursor.execute(sql, (student.first_name, student.last_name, student.age, id_person))
                else:
                    sql = "UPDATE person SET first_name=%s, last_name=%s, age=%s, id_address=%s WHERE id_person=%s "
                    cursor.execute(sql,(student.first_name, student.last_name, student.age, student.address.id, id_person))

                # On commit
                Dao.connection.commit()

                # cursor.rowcount permet de savoir si une ligne a été modifiée
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return True

    def delete(self, student: Student) -> bool:
        """Supprime en BD l'entité Student correspondant à student

        :param student: student dont l'entité Student correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                # On va d'abord récupérer l'id de la personne qui correspond à cet étudiant
                sql = "SELECT id_person FROM student WHERE student_nbr = %s"
                cursor.execute(sql, (student.student_nbr,))

                result = cursor.fetchone()

                if result is None:
                    print("Erreur lors de la récupération de l'id de la personne correspondant à cet étudiant")
                    return False

                id_person = result['id_person']
                # print("Id personne : ", id_person)

                # On va supprimer l'élève
                sql = "DELETE FROM student WHERE student_nbr = %s "
                cursor.execute(sql, (student.student_nbr,))

                print(sql)
                print("student_nbr :", student.student_nbr)
                print("id_person :", id_person)
                print("DELETE student :", cursor.rowcount)

                # cursor.rowcount = nombre de lignes qui ont été affectées par cette requête. On attend une seule (une suppression).
                if cursor.rowcount != 1:
                    #Si il y a erreur on remet la base dans l'état ou elle était
                    Dao.connection.rollback()
                    return False

                # On va supprimer la personne qui correspond à l'enseignant
                sql = "DELETE FROM person WHERE id_person = %s"
                cursor.execute(sql, (id_person,))

                print(sql)
                print("DELETE person :", cursor.rowcount)

                # cursor.rowcount = nombre de lignes qui ont été affectées par cette requête. On attend une seule (une suppression).
                if cursor.rowcount != 1:
                    # Si il y a erreur on remet la base dans l'état ou elle était
                    Dao.connection.rollback()
                    return False

                # Si c'est ok, on commit
                Dao.connection.commit()
                print("COMMIT effectué")
        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
            return False
        return True
