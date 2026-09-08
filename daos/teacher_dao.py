# -*- coding: utf-8 -*-

"""
Classe Dao[Teacher]
"""

from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class TeacherDao(Dao[Teacher]):

    # TODO Méthode à implémenter
    def create(self, teacher: Teacher) -> int:
        """Crée en BD l'entité Teacher correspondant au Teacher teacher

        :param teacher: à créer sous forme d'entité Teacher en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """

        return 0

    # TODO Méthode à implémenter
    def read(self, id_teacher: int) -> Optional[Teacher]:
        """Renvoit le teacher correspondant à l'entité dont l'id est id_teacher
           (ou None s'il n'a pu être trouvé)"""
        return None

    def read_all(self):
        """Renvoit la liste des professeurs """
       # teacher: Optional[Teacher]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT teacher.id_teacher, teacher.id_person, person.first_name, person.last_name, person.age, person.id_address FROM teacher JOIN person ON teacher.id_person = person.id_person "
            cursor.execute(sql)
            teachers_lignes_sql = cursor.fetchall()
            teachers_objets = []
            #print("Nombre de résultats :", len(teachers_lignes_sql))
            #print("Résultats :", teachers_lignes_sql)
            #print(f"on va afficher les résultats pour cette requête {sql} ")

            for s in teachers_lignes_sql:
                #print(s)
                teacher = Teacher(s['first_name'], s['last_name'], s['age'])
                teacher.id = s['id_teacher']
                teachers_objets.append(teacher)

        return teachers_objets

    # TODO Méthode à implémenter
    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité Teacher correspondant à teacher, pour y correspondre

        :param teacher: teacher déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """

        return True

    # TODO Méthode à implémenter
    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher

        :param teacher: teacher dont l'entité Teacher correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """

        return True
