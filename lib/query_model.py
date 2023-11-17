import sqlite3

# Regular Expression
import re


class QuerylModel:
    def __init__(self, database_file):
        self.database_file = database_file

    # Functions to excecute queries
    def execute_query(self, sql_query):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()

        return result

    def single_cell_query(self, sql_query):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()

        return result

    def execute_update(self, sql_query):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(sql_query)
        conn.commit()

    # Queries for everything from tables

    def get_authors(self):
        query = "SELECT * FROM auteurs"
        return self.execute_query(query)

    def get_leerdoelen(self):
        query = "SELECT * FROM leerdoelen"
        return self.execute_query(query)

    def get_all_questions(self):
        query = "SELECT * FROM vragen LIMIT 50"
        return self.execute_query(query)

    # Queries to get single column from row
    def get_leerdoel_table(self):
        query = "SELECT leerdoel FROM leerdoelen"
        return self.single_cell_query(query)

    def get_auteur_table(self):
        query = "SELECT voornaam, achternaam FROM auteurs"
        return self.single_cell_query(query)

    # Queries for altering data
    def get_questions_without_leerdoel(self):
        query = """SELECT * FROM vragen WHERE leerdoel 
            NOT IN(SELECT id FROM leerdoelen) AND 
            leerdoelException IS NOT 1 OR leerdoel IS NULL LIMIT 1"""
        return self.execute_query(query)

    def get_questions_without_author(self):
        query = """SELECT * FROM vragen WHERE auteur NOT IN(SELECT id
            FROM auteurs) AND authorException IS NOT 1 
            OR auteur IS NULL LIMIT 1"""
        return self.execute_query(query)

    def questions_with_bad_syntax(self):
        query = f"""SELECT * FROM vragen WHERE vraag LIKE '%<br>%' AND 
                sysCodeException IS NOT 1 OR vraag LIKE '%&nbsp;%' AND 
                sysCodeException IS NOT 1 LIMIT 1"""
        return self.execute_query(query)
        # FIX SQLITE VERSION IN VENV!!!! REGEX TRYOUT
        sys_code = "&.+;$"
        html_code = "<.+>$"
        query = f"""SELECT * FROM vragen WHERE vraag REGEXP '{html_code}' AND 
                sysCodeException IS NOT 1 OR vraag REGEXP '{sys_code}' AND 
                sysCodeException IS NOT 1 LIMIT 1"""
        return self.execute_query(query)
        # TRYOUT WITH LIKE QUERY
        query = f"""SELECT * FROM vragen WHERE vraag LIKE '%<__>%' AND 
                sysCodeException IS NOT 1 OR vraag LIKE '%&__%' AND 
                sysCodeException IS NOT 1 LIMIT 1"""
        return self.execute_query(query)

    def get_bad_employee_tabels(self):
        query = """SELECT * FROM auteurs WHERE medewerker IS NOT 0 AND 
                medewerker IS NOT 1 AND employeeException IS NOT 1 LIMIT 1"""
        return self.execute_query(query)

    def get_bad_author_birthdate_tabels(self):
        query = """SELECT * FROM auteurs WHERE geboortejaar < 1950 AND 
                birthYearException IS NOT 1 OR geboortejaar > 2020 AND 
                birthYearException IS NOT 1 LIMIT 1"""
        return self.execute_query(query)

    # Queries for saving changed data

    # Changed questions
    def save_leerdoel(self, question_id, leerdoel_id, user_id):
        query = """UPDATE vragen SET leerdoel = %s, 
                changedBy = %s WHERE id IS %s""" % (leerdoel_id, user_id, question_id)
        print(query)
        self.execute_update(query)

    def save_author(self, question_id, author_id, user_id):
        query = """UPDATE vragen SET auteur = %s, 
                changedBy = %s WHERE id IS %s""" % ( author_id, user_id, question_id,)
        self.execute_update(query)

    def save_question(self, question_id, question_update, user_id):
        query = """UPDATE vragen SET vraag = %s, 
                changedBy = %s WHERE id IS %s""" % (question_update, user_id, question_id)
        self.execute_update(query)

    # changed authors
    def save_employee(self, author_id, user_id):
        query = """UPDATE auteurs SET medewerker = False, 
                changedBy = %s WHERE id IS %s""" % (user_id, author_id)
        self.execute_update(query)

    def save_non_employee(self, author_id, user_id):
        query = """UPDATE auteurs SET medewerker = True, 
                changedBy = %s WHERE id IS %s""" % ( user_id, author_id)
        self.execute_update(query)

    def save_birth_year(self, author_id, birth_year, user_id):
        query = """UPDATE auteurs SET geboortejaar = %s, 
                changedBy = %s WHERE id IS %s""" % (birth_year, user_id, author_id)
        self.execute_update(query)

    # Queries to give vragen row an exception
    def leerdoel_exception(self, question_id, user_id):
        query = f"""UPDATE vragen SET leerdoelException = True, 
                exceptionBy = '{user_id}' WHERE id IS {question_id}"""
        self.execute_update(query)

    def author_exception(self, question_id, user_id):
        query = f"""UPDATE vragen SET authorException = True, 
                exceptionBy = '{user_id}' WHERE id IS {question_id}"""
        self.execute_update(query)

    def sys_code_exception(self, question_id, user_id):
        query = f"""UPDATE vragen SET sysCodeException = True, 
                exceptionBy = '{user_id}' WHERE id IS {question_id}"""
        self.execute_update(query)

    # Queries to give auteurs row an exception
    def employee_exception(self, question_id, user_id):
        query = f"""UPDATE auteurs SET employeeException = 1, 
                exceptionBy = '{user_id}' WHERE id IS {question_id}"""
        self.execute_update(query)

    def birth_year_exception(self, question_id, user_id):
        query = f"""UPDATE auteurs SET birthYearException = 1, 
                exceptionBy = '{user_id}' WHERE id IS {question_id}"""
        self.execute_update(query)

    # Queries to get exceptions
    def get_all_question_exceptions(self):
        query = """SELECT * FROM vragen WHERE leerdoelException IS True OR 
                authorException IS True or sysCodeException IS True"""
        return self.execute_query(query)

    def restore_question_exception(self, question_id):
        leerdoel_exceptions = self.single_cell_query(
            f"SELECT leerdoelException FROM vragen WHERE id IS {question_id}"
        )
        if leerdoel_exceptions[0][0] == 1:
            query = (
                f"UPDATE vragen SET leerdoelException = False WHERE id IS {question_id}"
            )
            return self.execute_update(query)

        author_exceptions = self.single_cell_query(
            f"SELECT authorException FROM vragen WHERE id IS {question_id}"
        )
        if author_exceptions[0][0] == 1:
            query = (
                f"UPDATE vragen SET authorException = False WHERE id IS {question_id}"
            )
            return self.execute_update(query)

        sys_code_exceptions = self.single_cell_query(
            f"SELECT sysCodeException FROM vragen WHERE id IS {question_id}"
        )
        if sys_code_exceptions[0][0] == 1:
            query = (
                f"UPDATE vragen SET sysCodeException = False WHERE id IS {question_id}"
            )
            return self.execute_update(query)

    def get_all_author_exceptions(self):
        query = """SELECT * FROM auteurs WHERE birthYearException IS True 
                OR employeeException IS True"""
        return self.execute_query(query)

    def restore_author_exception(self, author_id):
        birth_year_exception = self.single_cell_query(
            f"SELECT birthYearException FROM auteurs WHERE id IS {author_id}"
        )
        if birth_year_exception[0][0] == 1:
            query = (
                f"UPDATE auteurs SET birthYearException = False WHERE id IS {author_id}"
            )
            return self.execute_update(query)

        employee_exception = self.single_cell_query(
            f"SELECT employeeException FROM auteurs WHERE id IS {author_id}"
        )
        if employee_exception[0][0] == 1:
            query = (
                f"UPDATE auteurs SET employeeException = False WHERE id IS {author_id}"
            )
            return self.execute_update(query)

    # Filter queries

    # Filter UID
    def uid_filter(self, uid_min, uid_max):
        query = f"SELECT * FROM vragen WHERE id > {uid_min} - 1 AND id < {uid_max} + 1"
        return self.execute_query(query)

    # Filter authors
    def author_filter(self, author_id):
        query = f"SELECT * FROM vragen WHERE auteur IS {author_id}"
        return self.execute_query(query)

    def faulty_author(self):
        query = "SELECT * FROM vragen WHERE auteur NOT IN(SELECT id FROM auteurs)"
        return self.execute_query(query)

    def filter_author_exceptions(self):
        query = "SELECT * FROM vragen WHERE authorException IS 1"
        return self.execute_query(query)

    # Filter by employee or not
    def int_employee(self):
        query = """SELECT * FROM vragen JOIN auteurs ON 
                vragen.auteur=auteurs.id WHERE medewerker IS 1"""
        return self.execute_query(query)

    def ext_employee(self):
        query = """SELECT * FROM vragen JOIN auteurs ON 
                vragen.auteur=auteurs.id WHERE medewerker IS 0"""
        return self.execute_query(query)

    def faulty_employee(self):
        query = """SELECT * FROM vragen JOIN auteurs ON 
                vragen.auteur=auteurs.id WHERE medewerker > 1 """
        return self.execute_query(query)

    # Filter by author
    def leerdoel_filter(self, leerdoel_id):
        query = f"SELECT * FROM vragen WHERE leerdoel IS {leerdoel_id}"
        return self.execute_query(query)

    def faulty_leerdoel(self):
        query = """SELECT * FROM vragen WHERE leerdoel 
                NOT IN(SELECT id FROM leerdoelen)"""
        return self.execute_query(query)

    def filter_leerdoel_exceptions(self):
        query = "SELECT * FROM vragen WHERE leerdoelException IS 1"
        return self.execute_query(query)

    # Filter for sys code exception
    def filter_sys_code_exceptions(self):
        query = "SELECT * FROM vragen WHERE sysCodeException IS 1"
        return self.execute_query(query)

    # Filter for changed by user
    def filter_changed_by_user(self, user_id):
        query = f"SELECT * FROM vragen WHERE changedBy IS {user_id}"
        print(query)
        return self.execute_query(query)

    # Filter for exception by user
    def filter_exception_by_user(self, user_id):
        query = f"SELECT * FROM vragen WHERE exceptionBy IS {user_id}"
        return self.execute_query(query)

    # Queries for users
    # New user
    def set_new_user(self, first_name, infix, last_name, email, password, admin):
        query = f"""INSERT INTO users (firstName, infix, lastName, email, password, admin) 
                VALUES ('{first_name}', '{infix}', '{last_name}', '{email}', '{password}', {admin})"""
        return self.execute_update(query)

    # Password check
    def password_check(self, email):
        query = f"SELECT password FROM users WHERE email IS '{email}'"
        return self.single_cell_query(query)

    # Admin check
    def admin_check(self, email):
        query = f"SELECT admin FROM users WHERE email IS '{email}'"
        return self.single_cell_query(query)

    # Get first name
    def get_full_name(self, email):
        query = f"SELECT firstName, infix, lastName FROM users WHERE email IS '{email}'"
        return self.execute_query(query)

    # Get first name
    def get_first_name(self, email):
        query = f"SELECT firstName FROM users WHERE email IS '{email}'"
        return self.single_cell_query(query)

    # Get user id
    def get_user_id(self, email):
        query = f"SELECT id FROM users WHERE email IS '{email}'"
        return self.single_cell_query(query)

    # Get all users
    def get_users(self):
        query = "SELECT * FROM users"
        return self.execute_query(query)

    def get_single_users(self):
        query = "SELECT firstName, infix, lastName FROM users"
        return self.single_cell_query(query)

    # Delete user
    def delete_user(self, user_id):
        query = f"DELETE FROM users WHERE id IS {user_id}"
        print(query)
        return self.execute_update(query)
