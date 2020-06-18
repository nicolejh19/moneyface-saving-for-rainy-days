import sqlite3
from decimal import *

def is_float(amt):
    try:
        temp = float(amt)
        return True
    except ValueError as e:
        return False

class DBHelper:
    def __init__(self, dbname):
        self.dbname = dbname
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        dbcursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, phone_number TEXT DEFAULT "NORECORD" NOT NULL, username TEXT NOT NULL)''')
        dbcursor.execute('''CREATE TABLE IF NOT EXISTS monthly_budget (year_month INTEGER NOT NULL, user_id INTEGER NOT NULL, amount TEXT NOT NULL, PRIMARY KEY(year_month, user_id), FOREIGN KEY(user_id) REFERENCES users(user_id))''')
        dbcursor.execute('''CREATE TABLE IF NOT EXISTS daily_exp (date_time DATE NOT NULL, category TEXT NOT NULL, amount TEXT NOT NULL, user_id INTEGER NOT NULL, year_month INTEGER NOT NULL, PRIMARY KEY (date_time, user_id), FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(year_month, user_id) REFERENCES monthly_budget(year_month, user_id))''')
        dbcursor.execute('''CREATE TABLE IF NOT EXISTS monthly_exp (year_month INTEGER NOT NULL, user_id INTEGER NOT NULL, amount TEXT NOT NULL, within_budget INTEGER NOT NULL, PRIMARY KEY(year_month, user_id), FOREIGN KEY(user_id) REFERENCES users(user_id), FOREIGN KEY(year_month, user_id) REFERENCES monthly_budget(year_month, user_id))''')
        dbcursor.execute('''CREATE TABLE IF NOT EXISTS monthly_savings (date_time DATE NOT NULL, year_month INTEGER NOT NULL, user_id INTEGER NOT NULL, amount TEXT NOT NULL, type_savings TEXT NOT NULL, PRIMARY KEY(date_time, user_id), FOREIGN KEY(user_id) REFERENCES users(user_id))''')
        dbcursor.execute('''CREATE TABLE IF NOT EXISTS iou (user_id_debtor INTEGER NOT NULL, name_debtee TEXT NOT NULL, amount TEXT NOT NULL, PRIMARY KEY(user_id_debtor, name_debtee), FOREIGN KEY(user_id_debtor) REFERENCES users(user_id))''')
        dbcursor.execute('''CREATE TABLE IF NOT EXISTS uome (user_id_debtee INTEGER NOT NULL, name_debtor TEXT NOT NULL, amount TEXT NOT NULL, PRIMARY KEY(user_id_debtee, name_debtor), FOREIGN KEY(user_id_debtee) REFERENCES users(user_id))''')
        db.commit()
        dbcursor.close()

    def add_user(self, user_id, username):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        try: 
            stmt = '''INSERT INTO users (user_id, username) VALUES (?, ?)'''
            args = (user_id, username, )
            dbcursor.execute(stmt, args)
            db.commit()
        except sqlite3.IntegrityError:
            pass
        finally:
            dbcursor.close()

    def update_phone_number(self, user_id, phone_number):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''UPDATE users SET phone_number = ? WHERE user_id = ?'''
        args = (phone_number, user_id, )
        dbcursor.execute(stmt, args)
        db.commit()
        dbcursor.close()       
        
    def is_user_phone_number_stored(self, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT phone_number FROM users WHERE user_id = ?'''
        args = (user_id, )
        try: 
            dbcursor.execute(stmt, args)
            record = dbcursor.fetchone()
            return record[0] != "NORECORD"
        except (sqlite3.Error, TypeError):
            return False
        finally:
            dbcursor.close()

    def get_username(self, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT username FROM users WHERE user_id = ?'''
        args = (user_id, )
        dbcursor.execute(stmt, args)
        record = dbcursor.fetchone()
        dbcursor.close()
        return record[0] 
    
    def is_user_stored(self, phone_number):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT user_id FROM users WHERE phone_number = ?'''
        args = (phone_number, )
        try: 
            dbcursor.execute(stmt, args)
            record = dbcursor.fetchone()
            return record is not None
        except (sqlite3.Error, TypeError):
            return False
        finally:
            dbcursor.close()
            
    def get_user_id(self, phone_number):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT user_id FROM users WHERE phone_number = ?'''
        args = (phone_number, )
        dbcursor.execute(stmt, args)
        record = dbcursor.fetchone()
        dbcursor.close()
        return record[0]

    def get_all_users(self):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT user_id FROM users'''
        try:
            dbcursor.execute(stmt)
            records = dbcursor.fetchall()
            res = []
            for row in records:
                res.append(row[0])
            return res
        except sqlite3.DatabaseError:
            return []
        finally:
            dbcursor.close()        

    def add_monthly_budget(self, year_month, amount, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''INSERT INTO monthly_budget (year_month, amount, user_id) VALUES (?, ?, ?)'''
        args = (year_month, amount, user_id, )
        try:
            dbcursor.execute(stmt, args)
            db.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            dbcursor.close()

    def get_monthly_budget(self, year_month, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT amount FROM monthly_budget WHERE year_month = ? AND user_id = ?'''
        args = (year_month, user_id, )
        try: 
            dbcursor.execute(stmt, args)
            record = dbcursor.fetchone()
            return str(Decimal(record[0]).quantize(Decimal('1.00')))
        except (sqlite3.Error, TypeError):
            return "No budget set this month."
        finally:
            dbcursor.close()
    
    def add_daily_exp(self, date_time, category, amount, user_id, year_month):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''INSERT INTO daily_exp (date_time, category, amount, user_id, year_month) VALUES (?, ?, ?, ?, ?)'''
        args = (date_time, category, amount, user_id, year_month, )
        dbcursor.execute(stmt, args)
        db.commit()
        dbcursor.close()
    
    def get_monthly_exp(self, user_id, year_month):
        default_res = "No records of money spent this month. Go back to /main and record your expenditure this month leh. If not how you keep track?"
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT amount FROM daily_exp WHERE user_id = ? AND year_month = ?'''
        args = (user_id, year_month, )
        try:
            dbcursor.execute(stmt, args)
            records = dbcursor.fetchall()
            sum = Decimal(0)
            for row in records:
                sum += Decimal(row[0])
            if sum != Decimal(0):
                return str(sum.quantize(Decimal('1.00')))
            else: 
                return default_res
        except (sqlite3.Error, TypeError):
            return default_res
        finally:
            dbcursor.close()

    def get_monthly_category_exp(self, user_id, year_month, category):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT amount FROM daily_exp WHERE user_id = ? AND year_month = ? AND category = ?'''
        args = (user_id, year_month, category, )
        try:
            dbcursor.execute(stmt, args)
            records = dbcursor.fetchall()
            sum = Decimal(0)
            for row in records:
                sum += Decimal(row[0])
            return str(sum.quantize(Decimal('1.00')))
        except (sqlite3.DatabaseError, TypeError):
            return "0"
        finally:
            dbcursor.close()

    def add_monthly_exp(self, user_id, year_month):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''INSERT INTO monthly_exp (year_month, amount, user_id, within_budget) VALUES (?, ?, ?, ?)'''
        amount = self.get_monthly_exp(user_id, year_month)
        if not is_float(amount):
            return False
        budget = self.get_monthly_budget(year_month, user_id)
        within_budget = 0
        try:
            if float(amount) <= budget:
                within_budget = 1
        except ValueError as e:
            if int(amount) <= budget:
                within_budget = 1
        args = (year_month, amount, user_id, within_budget, )
        try:
            dbcursor.execute(stmt, args)
            db.commit()
            return True
        except sqlite3.DatabaseError:
            return False
        finally:
            dbcursor.close()

    def get_average_monthly_exp(self, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt1 = '''SELECT amount FROM monthly_exp WHERE user_id = ?'''
        args = (user_id, )
        try:
            dbcursor.execute(stmt1, args)
            records = dbcursor.fetchall()
            avg, counter = Decimal(0), 0
            for row in records:
                avg += Decimal(row[0])
                counter += 1
            avg = avg / counter
            return  str(avg.quantize(Decimal('1.00'))) 
        except (sqlite3.DatabaseError, InvalidOperation):
            return "No history of your spendings can be found. Start tracking your spendings from this month by using the spendings menu to update your daily expenditure."
        finally:
            dbcursor.close()
    
    def get_percentage_within_budget(self, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt1 = '''SELECT within_budget FROM monthly_exp WHERE user_id = ?'''
        args = (user_id, )
        try:
            dbcursor.execute(stmt1, args)
            records = dbcursor.fetchall()
            total, counter = 0, 0
            for row in records:
                total += 1
                if row[0] == 1:
                    counter += 1
            res = (counter / total) * 100
            return str(round(res, 2))
        except (sqlite3.DatabaseError, ZeroDivisionError):
            return "No history of your spendings can be found. Start tracking your spendings from this month by using the spendings menu to update your daily expenditure."
        finally:
            dbcursor.close()

    def add_monthly_savings(self, date_time, year_month, amount, user_id, type_savings):
        flag = self.get_whether_current_monthly_saved(year_month, user_id)
        if flag and type_savings == 'MONTHLY':
            return False
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''INSERT INTO monthly_savings (year_month, date_time, amount, user_id, type_savings) VALUES (?, ?, ?, ?, ?)'''
        args = (year_month, date_time, amount, user_id, type_savings, )
        try:
            dbcursor.execute(stmt, args)
            db.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            dbcursor.close()

    def get_whether_current_monthly_saved(self, year_month, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        type_savings = 'MONTHLY'
        stmt = '''SELECT amount FROM monthly_savings WHERE year_month = ? AND user_id = ? AND type_savings = ?'''
        args = (year_month, user_id, type_savings, )
        try: 
            dbcursor.execute(stmt, args)
            records = dbcursor.fetchall()
            if len(records) == 0:
                return False
            else:
                return True
        except (sqlite3.Error):
            return False
        finally:
            dbcursor.close()   

    def get_current_savings(self, year_month, user_id):
        default_res = "Monthly savings has not been keyed in for this month. God of Fortune advise you to go back to /main and record your savings for this month."
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT amount FROM monthly_savings WHERE year_month = ? AND user_id = ?'''
        args = (year_month, user_id, )
        try: 
            dbcursor.execute(stmt, args)
            records = dbcursor.fetchall()
            sum = Decimal(0)
            for row in records:
                sum += Decimal(row[0])
            if sum != Decimal(0):
                return str(sum.quantize(Decimal('1.00'))) 
            else:
                return default_res
        except (sqlite3.Error, TypeError):
            return default_res
        finally:
            dbcursor.close()   

    def get_total_savings(self, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT amount FROM monthly_savings WHERE user_id = ?'''
        args = (user_id, )
        try:
            dbcursor.execute(stmt, args)
            records = dbcursor.fetchall()
            sum = Decimal(0)
            for row in records:
                sum += Decimal(row[0])
            return str(sum.quantize(Decimal('1.00'))) 
        except (sqlite3.DatabaseError, TypeError):
            return "0.00"
        finally:
            dbcursor.close()
    
    def get_num_months_savings(self, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt1 = '''SELECT COUNT(DISTINCT year_month) FROM monthly_savings GROUP BY user_id HAVING user_id = ?'''
        args = (user_id, )
        try:
            dbcursor.execute(stmt1, args)
            record = dbcursor.fetchone()
            if record is None:
                return 0 
            else:
                return record[0]
            except sqlite3.Error:
                return 0
            finally:
                dbcursor.close()
    
    def get_average_monthly_savings(self, user_id):
        total_savings = self.get_total_savings(user_id)
        # print("total savings: " + str(total_savings))
        num_months = self.get_num_months_savings(user_id)
        # print("num_months: " + str(num_months))
        if is_float(total_savings) and num_months != 0:
            return (Decimal(total_savings) / num_months).quantize(Decimal('1.00'))
        else:
            return 0

    def get_all_debtees(self, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT name_debtee, amount FROM iou WHERE user_id_debtor = ?'''
        args = (user_id, )
        try:
            dbcursor.execute(stmt, args)
            records = dbcursor.fetchall()
            res = []
            for row in records:
                res.append((row[0], row[1], ))
            return res
        except sqlite3.DatabaseError:
            return []
        finally:
            dbcursor.close() 
            
    def is_debtee_present_iou(self, user_id_debtor, name_debtee):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT amount FROM iou WHERE user_id_debtor = ? AND name_debtee = ?'''
        args = (user_id_debtor, name_debtee, )
        try: 
            dbcursor.execute(stmt, args)
            record = dbcursor.fetchone()
            return record is not None
        except (sqlite3.Error, TypeError):
            return False
        finally:
            dbcursor.close()
            
    def get_debtee_amount(self, user_id_debtor, name_debtee):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT amount FROM iou WHERE user_id_debtor = ? AND name_debtee = ?'''
        args = (user_id_debtor, name_debtee, )
        dbcursor.execute(stmt, args)
        record = dbcursor.fetchone()
        dbcursor.close()
        return record[0]
    
    def add_debtee_iou(self, user_id_debtor, name_debtee, amt):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        if self.is_debtee_present_iou(user_id_debtor, name_debtee):
            new_amt = Decimal(amt) + Decimal(self.get_debtee_amount(user_id_debtor, name_debtee))
            stmt = '''UPDATE iou SET amount = ? WHERE user_id_debtor = ? AND name_debtee = ?'''
            args = (str(new_amt.quantize(Decimal('1.00'))), user_id_debtor, name_debtee, )
        else:
            stmt = '''INSERT INTO iou (user_id_debtor, name_debtee, amount) VALUES (?, ?, ?)'''
            args = (user_id_debtor, name_debtee, amt)
        dbcursor.execute(stmt, args)
        db.commit()
        dbcursor.close() 
            
    def delete_debtee_iou(self, user_id_debtor, name_debtee):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''DELETE FROM iou WHERE user_id_debtor = ? AND name_debtee = ?'''
        args = (user_id_debtor, name_debtee, )
        dbcursor.execute(stmt, args)
        db.commit()
        dbcursor.close()

    def get_all_debtors(self, user_id):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT name_debtor, amount FROM uome WHERE user_id_debtee = ?'''
        args = (user_id, )
        try:
            dbcursor.execute(stmt, args)
            records = dbcursor.fetchall()
            res = []
            for row in records:
                res.append((row[0], row[1], ))
                return res
        except sqlite3.DatabaseError:
            return []
        finally:
            dbcursor.close()

    def is_debtor_present_uome(self, user_id_debtee, name_debtor):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT amount FROM uome WHERE user_id_debtee = ? AND name_debtor = ?'''
        args = (user_id_debtee, name_debtor, )
        try: 
            dbcursor.execute(stmt, args)
            record = dbcursor.fetchone()
            return record is not None
        except (sqlite3.Error, TypeError):
            return False
        finally:
            dbcursor.close()
            
    def get_debtor_amount(self, user_id_debtee, name_debtor):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT amount FROM uome WHERE user_id_debtee = ? AND name_debtor = ?'''
        args = (user_id_debtee, name_debtor, )
        dbcursor.execute(stmt, args)
        record = dbcursor.fetchone()
        dbcursor.close()
        return record[0]

    def add_debtor_uome(self, user_id_debtee, name_debtor, amt):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        if self.is_debtor_present_uome(user_id_debtee, name_debtor):
            new_amt = Decimal(amt) + Decimal(self.get_debtor_amount(user_id_debtee, name_debtor))
            stmt = '''UPDATE uome SET amount = ? WHERE user_id_debtee = ? AND name_debtor = ?'''
            args = (str(new_amt.quantize(Decimal('1.00'))), user_id_debtee, name_debtor, )
        else:
            stmt = '''INSERT INTO uome (user_id_debtee, name_debtor, amount) VALUES (?, ?, ?)'''
            args = (user_id_debtee, name_debtor, amt)
        dbcursor.execute(stmt, args)
        db.commit()
        dbcursor.close()
        
    def delete_debtor_uome(self, user_id_debtee, name_debtor):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''DELETE FROM uome WHERE user_id_debtee = ? AND name_debtor = ?'''
        args = (user_id_debtee, name_debtor, )
        dbcursor.execute(stmt, args)
        db.commit()
        dbcursor.close()

    ## USE FOR TESTING ONLY
    def test_all_users(self):
        db = sqlite3.connect(self.dbname)
        dbcursor = db.cursor()
        stmt = '''SELECT user_id, phone_number FROM users'''
        try:
            dbcursor.execute(stmt)
            records = dbcursor.fetchall()
            res = []
            for row in records:
                res.append((row[0], row[1],))
            return res
        except sqlite3.DatabaseError:
            return []
        finally:
            dbcursor.close() 
