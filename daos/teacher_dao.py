# -*- coding: utf-8 -*-

"""
Classe Dao[Teacher]
"""
from models.address import Address
from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class TeacherDao(Dao[Teacher]):

    def create(self, teacher: Teacher) -> int:
        """Crée en BD l'entité Teacher correspondant au Teacher teacher

        :param teacher: à créer sous forme d'entité Teacher en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:

                # On doit créer en premier la personne, puis récupérer l'id et ensuite créer l'étudiant relié à l'id de la personne
                if (teacher.address is None):
                    sql = "INSERT INTO person(first_name, last_name, age) VALUES (%s, %s, %s) "
                    cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age))
                else:
                    sql = "INSERT INTO person(first_name, last_name, age, id_address) VALUES (%s, %s, %s, %s) "
                    cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age, teacher.address.id))

                # On récupère l'identifiant de la personne qui vient d'être créé
                id_person = cursor.lastrowid

                # On crée ensuite l'étudiant correspondant à cette personne
                sql = "INSERT INTO teacher(hiring_date, id_person) VALUES (%s, %s) "
                cursor.execute(sql, (teacher.hiring_date, id_person))

                # On récupère l'identifiant de l'enseignant qui vient d'être créé
                teacher.id = cursor.lastrowid

                # On commit
                Dao.connection.commit()
            return teacher.id

        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return 0

    def read(self, id_teacher: int) -> Optional[Teacher]:
        """Renvoie le teacher correspondant à l'entité dont l'id est id_teacher
           (ou None s'il n'a pu être trouvé)"""

        teacher: Optional[Teacher]

        with Dao.connection.cursor() as cursor:
            sql = ("SELECT teacher.id_teacher, teacher.id_person, teacher.hiring_date, person.first_name, person.last_name, person.age, "
                   "person.id_address, address.street, address.city, address.postal_code "
                   "FROM teacher JOIN person ON teacher.id_person = person.id_person "
                   "LEFT JOIN address ON person.id_address = address.id_address "
                   "WHERE id_teacher=%s")
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()
        if record is not None:
            teacher = Teacher(record['first_name'], record['last_name'], record['age'], record['hiring_date'])
            teacher.id = record['id_teacher']
            address_id = record['id_address']
            if (address_id is not None):
                teacher.address = Address(record['street'], record['city'], record['postal_code'])
                teacher.address.id = address_id
        else:
            teacher = None

        return teacher

    def read_all(self):
        """Renvoie la liste des professeurs """
        with Dao.connection.cursor() as cursor:
            #sql = "SELECT teacher.id_teacher, teacher.id_person, teacher.hiring_date, person.first_name, person.last_name, person.age, person.id_address FROM teacher JOIN person ON teacher.id_person = person.id_person "
            sql = (
                "SELECT teacher.id_teacher, teacher.id_person, teacher.hiring_date, person.first_name, person.last_name, person.age, "
                "person.id_address, address.street, address.city, address.postal_code "
                "FROM teacher JOIN person ON teacher.id_person = person.id_person "
                "LEFT JOIN address ON person.id_address = address.id_address ")
            cursor.execute(sql)
            teachers_lignes_sql = cursor.fetchall()
            teachers_objets = []
            #print("Nombre de résultats :", len(teachers_lignes_sql))
            #print("Résultats :", teachers_lignes_sql)
            #print(f"on va afficher les résultats pour cette requête {sql} ")

            for s in teachers_lignes_sql:
                # On récupère les informations pour l'objet Teacher
                teacher = Teacher(s['first_name'], s['last_name'], s['age'], s['hiring_date'])
                teacher.id = s['id_teacher']
                # On récupère les informations pour l'objet Address
                address_id = s['id_address']
                if (address_id is not None):
                    teacher.address = Address(s['street'], s['city'], s['postal_code'])
                    teacher.address.id = address_id
                # On ajoute le Teacher ainsi obtenu dans la liste
                teachers_objets.append(teacher)
        return teachers_objets

    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité Teacher correspondant à teacher, pour y correspondre

        :param teacher: teacher déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """

        try:
            with Dao.connection.cursor() as cursor:
                #TODO A finir et Tester
                # On va d'abord récupérer l'id de la personne qui correspond à cet étudiant
                sql = "SELECT id_person FROM teacher WHERE id_teacher = %s"
                cursor.execute(sql, (teacher.id_teacher,))

                result = cursor.fetchone()

                if result is None:
                    print("Erreur lors de la récupération de l'id de la personne correspondant à cet enseignant")
                    return False

                id_person = result['id_person']

                #On modifie la personne correspondant à cet enseignant
                if (teacher.address is None):
                    sql = "UPDATE person SET first_name=%s, last_name=%s, age=%s WHERE id_person=%s "
                    cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age, id_person))
                else:
                    sql = "UPDATE person SET first_name=%s, last_name=%s, age=%s, id_address=%s WHERE id_person=%s "
                    cursor.execute(sql,(teacher.first_name, teacher.last_name, teacher.age, teacher.address.id, id_person))

                # On commit
                Dao.connection.commit()

                # cursor.rowcount permet de savoir si une ligne a été modifiée
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return True

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher

        :param teacher: teacher dont l'entité Teacher correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:

                #On va d'abord récupérer l'id de la personne qui correspond à cet enseignant
                sql = "SELECT id_person FROM teacher WHERE id_teacher = %s"
                cursor.execute(sql, (teacher.id,))

                result = cursor.fetchone()

                if result is None:
                    print("Erreur lors de la récupération de l'id de la personne correspondant à cet enseignant")
                    return False

                id_person = result['id_person']
                #print("Id personne : ", id_person)

                # On va supprimer l'enseignant
                sql = "DELETE FROM teacher WHERE id_teacher = %s "
                cursor.execute(sql, (teacher.id,))

                # cursor.rowcount = nombre de lignes qui ont été affectées par cette requête. On attend une seule (une suppression).
                if cursor.rowcount != 1:
                    #Si il y a erreur on remet la base dans l'état ou elle était
                    Dao.connection.rollback()
                    return False

                # On va supprimer la personne qui correspond à l'enseignant
                sql = "DELETE FROM person WHERE id_person = %s"
                cursor.execute(sql, (id_person,))

                # cursor.rowcount = nombre de lignes qui ont été affectées par cette requête. On attend une seule (une suppression).
                if cursor.rowcount != 1:
                    # Si il y a erreur on remet la base dans l'état ou elle était
                    Dao.connection.rollback()
                    return False

                # Si c'est ok, on commit
                Dao.connection.commit()
        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
            return False
        return True