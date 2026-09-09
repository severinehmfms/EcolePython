# -*- coding: utf-8 -*-

"""
Classe Dao[Address]
"""

from models.address import Address
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressDao(Dao[Address]):
    def create(self, address: Address) -> int:
        """Crée en BD l'entité Address correspondant à une adresse

        :param address: à créer sous forme d'entité Address en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "INSERT INTO address(street, city, postal_code) VALUES (%s, %s, %s) "
                cursor.execute(sql, (address.street, address.city, address.postal_code))

                # On récupère l'identifiant qui vient d'être créé
                address.id = cursor.lastrowid
                # On commit
                Dao.connection.commit()
            return address.id
        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return 0

    def read(self, id_address: int) -> Optional[Address]:
        """Renvoie l'adresse correspondant à l'entité dont l'id est id_address
           (ou None s'il n'a pu être trouvé)"""
        address: Optional[Address]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address WHERE id_address=%s"
            cursor.execute(sql, (id_address,))
            record = cursor.fetchone()
        if record is not None:
            address = Address(record['street'], record['city'], record['postal_code'])
            address.id = record['id_address']
        else:
            address = None

        return address

    def read_all(self):
        """Renvoie la liste des adresses """
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address "
            cursor.execute(sql)
            addresses = cursor.fetchall()
            address_objets = []
            for a in addresses:
                # print(c)
                address = Address(a['street'], a['city'], a['postal_code'])
                address.id = a['id_course']
                address_objets.append(address)

        return address_objets

    def update(self, address: Address) -> bool:
        """Met à jour en BD l'entité Address correspondant à address, pour y correspondre

        :param address: address déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "UPDATE address set street=%s, city=%s, postal_code=%s WHERE id_address=%s "
                cursor.execute(sql, (address.street, address.city, address.postal_code, address.id))

                # On commit
                Dao.connection.commit()

                # cursor.rowcount permet de savoir si une ligne a été modifiée
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return True

    def delete(self, address: Address) -> bool:
        """Supprime en BD l'entité Address correspondant à address

        :param address: address dont l'entité Address correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "DELETE FROM address WHERE id_address = %s "
                cursor.execute(sql, (address.id))

                # On commit
                Dao.connection.commit()

                # cursor.rowcount permet de savoir si une ligne a été modifiée
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Exception : {e}")
            Dao.connection.rollback()
        return True
