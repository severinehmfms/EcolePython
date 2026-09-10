# -*- coding: utf-8 -*-

"""
Classe School
"""

from dataclasses import dataclass, field
from datetime import date

from daos.address_dao import AddressDao
from daos.course_dao import CourseDao
from daos.student_dao import StudentDao
from daos.teacher_dao import TeacherDao
from models.address import Address
from models.course import Course
from models.teacher import Teacher
from models.student import Student


@dataclass
class School:
    """Couche métier de l'application de gestion d'une école,
    reprenant les cas d'utilisation et les spécifications fonctionnelles :
    - courses : liste des cours existants
    - teachers : liste des enseignants
    - students : liste des élèves"""

    courses: list[Course] = field(default_factory=list, init=False)
    teachers: list[Teacher] = field(default_factory=list, init=False)
    students: list[Student] = field(default_factory=list, init=False)

    def add_course(self, course: Course) -> None:
        # On crée le cours en base de données
        dao = CourseDao()
        course.id = dao.create(course)
        """Ajout du cours course à la liste des cours."""
        self.courses.append(course)

    def add_teacher(self, teacher: Teacher) -> None:
        # On crée l'adresse de l'enseignant
        dao_address = AddressDao()
        teacher.address.id = dao_address.create(teacher.address)

        # On crée l'enseignant en base
        dao = TeacherDao()
        teacher.id = dao.create(teacher)
        """Ajout de l'enseignant teacher à la liste des enseignants."""
        self.teachers.append(teacher)

    def add_student(self, student: Student) -> None:
        # On crée l'adresse de l'étudiant
        dao_address = AddressDao()
        if (student.address is not None):
            student.address.id = dao_address.create(student.address)

        # On crée l'étudiant en base
        dao = StudentDao()
        student.student_nbr = dao.create(student)
        """Ajout de l'élève spécifié à la liste des élèves."""
        self.students.append(student)

    def update_teacher(self, teacher: Teacher) -> None:
        # On modifie l'enseignant en base
        dao = TeacherDao()
        dao.update(teacher)
        """Modification de l'enseignant spécifié dans la liste des enseignants aussi """
        for i, s in enumerate(self.teachers):
            if s.id == teacher.id:
                self.teachers[i] = teacher
                break

    def update_student(self, student: Student) -> None:
        # On modifie l'étudiant en base
        dao = StudentDao()
        dao.update(student)
        """Modification de l'élève spécifié dans la liste des élèves aussi """
        for i, s in enumerate(self.students):
            if s.student_nbr == student.student_nbr:
                self.students[i] = student
                break

    def delete_teacher(self, teacher: Teacher) -> None:
        # On modifie l'enseignant en base
        dao = TeacherDao()
        """Suppression de l'enseignant spécifié dans la liste des enseignants aussi si la suppression a réussi"""
        if dao.delete(teacher):
            for i, s in enumerate(self.teachers):
                if s.id == teacher.id:
                    self.teachers.pop(i)
                    break

    def delete_student(self, student: Student) -> None:
        # On modifie l'étudiant en base
        dao = StudentDao()
        """Suppression de l'enseignant spécifié dans la liste des enseignants aussi si la suppression a réussi """
        if dao.delete(student):
            for i, s in enumerate(self.students):
                if s.student_nbr == student.student_nbr:
                    self.students.pop(i)
                    break

    def display_courses_list(self) -> None:
        """Affichage de la liste des cours avec pour chacun d'eux :
        - leur enseignant
        - la liste des élèves le suivant"""
        for course in self.courses:
            print(f"cours de {course}")
            for student in course.students_taking_it:
                print(f"- {student}")
            print()

    def get_courses_list(self) -> list[Course]:
        return self.courses

    def display_students_list(self) -> None:
        """Affichage de la liste des étudiasnts """
        for student in self.students:
            print(f"Etudiant : {student}")
            print()

    def get_students_list(self) -> list[Student]:
        return self.students

    def display_teachers_list(self) -> None:
        """Affichage de la liste des professeurs """
        for teacher in self.teachers:
            print(f"Professeur : {teacher}")
            print()

    def get_teachers_list(self) -> list[Teacher]:
        return self.teachers

    @staticmethod
    def get_course_by_id(id_course: int):
        course_dao: CourseDao = CourseDao()
        return course_dao.read(id_course)

    @staticmethod
    def get_teacher_by_id(id_teacher: int):
        teacher_dao: TeacherDao = TeacherDao()
        return teacher_dao.read(id_teacher)

    @staticmethod
    def get_student_by_nbr(student_nbr: int):
        student_dao: StudentDao = StudentDao()
        return student_dao.read(student_nbr)

    def init_bd(self):
        """ Initialisation du jeu de données pour l'école à partir de la base de données """

        # On récupère la liste des étudiants en base de données
        student_dao: StudentDao = StudentDao()
        student_objets = student_dao.read_all()
        # Pour chaque étudiant en base, on ajoute l'étudiant dans la liste des étudiants
        for s in student_objets:
            self.students.append(s)

        # On récupère la liste des enseignants en base de données
        teacher_dao: TeacherDao = TeacherDao()
        teacher_objets = teacher_dao.read_all()
        # Pour chaque enseignant en base, on ajoute l'enseignant dans la liste des enseignants
        for s in teacher_objets:
            self.teachers.append(s)

        # On récupère la liste des cours en base de données (y compris l'id de l'enseignant)
        course_dao: CourseDao = CourseDao()
        courses_objets = course_dao.read_all()

        # On parcoure ces objets et on les ajoute dans self
        for c in courses_objets:
            self.courses.append(c)



        # TODO On récupère en base de données les cours que suivent les étudiants

    def init_static(self) -> None:
        """Initialisation d'un jeu de test pour l'école."""
        
        # création des étudiants et rattachement à leur adresse
        paul: Student    = Student('Paul', 'Dubois', 12)
        valerie: Student = Student('Valérie', 'Dumont', 13)
        louis: Student   = Student('Louis', 'Berthot', 11)

        paul.address    = Address('12 rue des Pinsons', 'Castanet', 31320)
        valerie.address = Address('43 avenue Jean Zay', 'Toulouse', 31200)
        louis.address   = Address('7 impasse des Coteaux', 'Cornebarrieu', 31150)

        # ajout de ceux-ci à l'école
        for student in [paul, valerie, louis]:
            self.add_student(student)

        # création des cours
        francais: Course = Course("Français", date(2024, 1, 29),
                                              date(2024, 2, 16))
        histoire: Course = Course("Histoire", date(2024, 2, 5),
                                              date(2024, 2, 16))
        geographie: Course = Course("Géographie", date(2024, 2, 5),
                                                  date(2024, 2, 16))
        mathematiques: Course = Course("Mathématiques", date(2024, 2, 12),
                                                        date(2024, 3, 8))
        physique: Course = Course("Physique", date(2024, 2, 19),
                                              date(2024, 3, 8))
        chimie: Course = Course("Chimie", date(2024, 2, 26),
                                          date(2024, 3, 15))
        anglais: Course = Course("Anglais", date(2024, 2, 12),
                                            date(2024, 2, 24))
        sport: Course = Course("Sport", date(2024, 3, 4),
                                        date(2024, 3, 15))

        # ajout de ceux-ci à l'école
        for course in [francais, histoire, geographie, mathematiques,
                       physique, chimie, anglais, sport]:
            self.add_course(course)

        # création des enseignants
        victor  = Teacher('Victor', 'Hugo', 23, date(2023, 9, 4))
        jules   = Teacher('Jules', 'Michelet', 32, date(2023, 9, 4))
        sophie  = Teacher('Sophie', 'Germain', 25, date(2023, 9, 4))
        marie   = Teacher('Marie', 'Curie', 31, date(2023, 9, 4))
        william = Teacher('William', 'Shakespeare', 34, date(2023, 9, 4))
        michel  = Teacher('Michel', 'Platini', 42, date(2023, 9, 4))

        # ajout de ceux-ci à l'école
        for teacher in [victor, jules, sophie, marie, william, michel]:
            self.add_teacher(teacher)

        # association des élèves aux cours qu'ils suivent
        for course in [geographie, physique, anglais]:
            paul.add_course(course)

        for course in [francais, histoire, chimie]:
            valerie.add_course(course)

        for course in [mathematiques, physique, geographie, sport]:
            louis.add_course(course)

        # association des enseignants aux cours qu'ils enseignent
        victor.add_course(francais)

        jules.add_course(histoire)
        jules.add_course(geographie)

        sophie.add_course(mathematiques)

        marie.add_course(physique)
        marie.add_course(chimie)

        william.add_course(anglais)

        michel.add_course(sport)
