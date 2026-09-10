# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""

from models.course import Course
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

from models.teacher import Teacher


@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours course

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                #if (course.teacher is None):
                #    print("L'enseignant doit exister dans l'objet Cours")
                #    return 0

                sql = "INSERT INTO course(name, start_date, end_date, id_teacher) VALUES (%s, %s, %s, %s) "
                id_teacher = course.teacher.id
                cursor.execute(sql, (course.name, course.start_date, course.end_date, id_teacher))

                #On récupère l'identifiant qui vient d'être créé
                course.id = cursor.lastrowid
                #On commit
                Dao.connection.commit()
            return course.id
        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return 0

    def read_id_student_by_cours(self, id_course : int) -> list:
        """Renvoie la liste des id des étudiants qui suivent le cours dont l'id est en paramètre"""
        student: Optional[Course]
        list_nbr_students = []

        with Dao.connection.cursor() as cursor:
            # Je récupère maintenant les ids des cours auquel l'étudiant est inscrit
            sql = "SELECT takes.student_nbr, takes.id_course FROM takes WHERE takes.id_course = %s"
            cursor.execute(sql, (id_course,))
            all_result = cursor.fetchall()
            for record in all_result:
                student_nbr = record['student_nbr']
                list_nbr_students.append(student_nbr)

        return list_nbr_students

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoie le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]
        
        with Dao.connection.cursor() as cursor:
            #sql = "SELECT * FROM course WHERE id_course=%s"
            sql = ("SELECT course.*, teacher.hiring_date, person.first_name, person.last_name, person.age "
                   "FROM course JOIN teacher ON course.id_teacher = teacher.id_teacher "
                   "JOIN person ON teacher.id_person = person.id_person "
                   "WHERE id_course=%s")

            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
        if record is not None:
            course = Course(record['name'], record['start_date'], record['end_date'])
            course.id = record['id_course']
            id_teacher = record['id_teacher']
            teacher = Teacher(record['first_name'], record['last_name'], record['age'], record['hiring_date'])
            teacher.id = record['id_teacher']
            #course.teacher = teacher
            course.set_teacher(teacher)
        else:
            course = None

        return course

    def read_all(self):
        """Renvoie la liste des cours """
        with Dao.connection.cursor() as cursor:
            #sql = "SELECT * FROM course "
            sql = ("SELECT course.*, teacher.hiring_date, person.first_name, person.last_name, person.age "
                   "FROM course JOIN teacher ON course.id_teacher = teacher.id_teacher "
                   "JOIN person ON teacher.id_person = person.id_person ")
            cursor.execute(sql)
            courses = cursor.fetchall()
            courses_objets = []
            for c in courses:
                course = Course(c['name'], c['start_date'], c['end_date'])
                course.id = c['id_course']
                # Pour chaque cours on renseigne le professeur enseignant ce cours
                teacher = Teacher(c['first_name'], c['last_name'], c['age'], c['hiring_date'])
                teacher.id = c['id_teacher']
                # course.teacher = teacher
                course.set_teacher(teacher)
                # On ajoute ce cours à la liste des cours qui sera retournée
                courses_objets.append(course)
        return courses_objets

    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "UPDATE course set name=%s, start_date=%s, end_date=%s, id_teacher=%s WHERE id_course=%s "
                cursor.execute(sql, (course.name, course.start_date, course.end_date, course.teacher.id, course.id))

                # On commit
                Dao.connection.commit()

                # cursor.rowcount permet de savoir si une ligne a été modifiée
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return True

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "DELETE FROM course WHERE id_course = %s "
                cursor.execute(sql, (course.id))

                # On commit
                Dao.connection.commit()

                # cursor.rowcount permet de savoir si une ligne a été modifiée
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return True
