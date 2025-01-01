import sqlite3
import time
import os 
import openpyxl
def check_line_user(user_name):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    try:
        cur.execute("SELECT * FROM line_user WHERE name=?;",(user_name,))
        ans = cur.fetchall()
        if ans:
            return 1
        else:
            return 0
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()

def store_line_user(id,name):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    try:
        cur.execute("INSERT INTO line_user (user_id, name) VALUES (?,?);",(id,name))
        con.commit()

    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
    finally:
        con.close()

def find_line_id():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    try:
        cur.execute("SELECT user_id FROM line_user;")
        rows=cur.fetchall()
        data=[]
        for row in rows:
            data.append(row[0])
        return data
    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
    finally:
        con.close()

def arduino_update_rfid(rfid):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    now = time.strftime("%H:%M:%S", time.localtime())

    try:
        cur.execute("SELECT state FROM entry_and_exit WHERE user_id=?;", (rfid,))
        ans = cur.fetchone() 

        if ans: 
            current_state = ans[0]
            if current_state == 'entry':
                reset = 'exit'
            elif current_state == 'exit':
                reset = 'entry'
            cur.execute("UPDATE entry_and_exit SET state=?, time=? WHERE user_id=?;",(reset, now, rfid))
            con.commit()
            print(f"RFID {rfid} 的狀態更新為 {reset}，時間更新為 {now}")
        else:
            print(f"RFID {rfid} 不存在於資料庫中")

        cur.execute("SELECT * FROM entry_and_exit WHERE user_id=?;", (rfid,))
        insert = cur.fetchone()
        data=f"{insert[5]},{insert[2]},{insert[3]},{insert[4]}\n"
        now2=time.strftime("%Y-%m-%d", time.localtime())
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "../static/entry_and_exit")
        log_file=os.path.join(log_dir, f"{now2}.log")
        with open(log_file, "a") as f:
            f.write(data)

    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
    finally:
        con.close()

def arduino_check_pass(key):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    try:
        cur.execute("SELECT * FROM cabinet WHERE pass=?;",(key,))
        ans = cur.fetchall()
        if ans:
            return 1
        else:
            return 0
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()

def arduino_update_cabinet(key):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    now = time.strftime("%H:%M:%S", time.localtime())

    try:
        # 查詢當前狀態
        cur.execute("SELECT state FROM cabinet WHERE pass=?;", (key,))
        ans = cur.fetchone()

        if ans:
            current_state = ans[0]
            if current_state == 'open':
                reset = 'close'
            elif current_state == 'close':
                reset = 'open'
            else:
                print(f"未知的狀態：{current_state}")
                return

            # 更新狀態
            cur.execute("UPDATE cabinet SET state=?, time=? WHERE pass=?;", (reset, now, key))
            con.commit()
            print(f"鑰匙櫃的狀態更新為 {reset}，時間更新為 {now}")
            # 查詢更新後的數據
            cur.execute("SELECT * FROM cabinet WHERE pass=?;", (key,))
            insert = cur.fetchone()
            if insert:
                data = f"{insert[5]},{insert[1]},{insert[2]},{insert[4]}\n"
                now2 = time.strftime("%Y-%m-%d", time.localtime())
                base_dir = os.path.dirname(os.path.abspath(__file__))
                log_dir = os.path.join(base_dir, "../static/cabinet")

                # 確保目錄存在
                os.makedirs(log_dir, exist_ok=True)

                log_file = os.path.join(log_dir, f"{now2}.log")
                with open(log_file, "a") as f:
                    f.write(data)
                return reset
            else:
                print(f"更新後未找到資料，RFID {key}")
        else:
            print(f"RFID {key} 不存在於資料庫中")

    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
    finally:
        con.close()

def alert_open(key):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    try:
        cur.execute("SELECT * FROM cabinet WHERE pass=?;",(key,))
        rows=cur.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
    finally:
        con.close()

def qrcode_update(text):

    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    now = time.strftime("%H:%M:%S", time.localtime())

    try:
        cur.execute("SELECT state FROM gun_state WHERE gun_id=?;", (text,))
        ans = cur.fetchone() 

        if ans: 
            current_state = ans[0]
            if current_state == 'in':
                reset = 'out'
            elif current_state == 'out':
                reset = 'in'
            cur.execute("UPDATE gun_state SET state=?, time=? WHERE gun_id=?;",(reset, now, text))
            con.commit()
            print(f"{text} 的狀態更新為 {reset}，時間更新為 {now}")
        else:
            print(f"{text} 不存在於資料庫中")
            pass

        cur.execute("SELECT * FROM gun_state WHERE gun_id=?;", (text,))
        insert = cur.fetchone()
        data=f"{insert[4]},{insert[1]},{insert[2]},{insert[3]}\n"
        now2=time.strftime("%Y-%m-%d", time.localtime())
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "../static/gun_state")
        log_file=os.path.join(log_dir, f"{now2}.log")
        with open(log_file, "a") as f:
            f.write(data)

    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
    finally:
        con.close()

def cabinet_state_search():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    try:
        cur.execute("SELECT * FROM cabinet WHERE state=?;",('close',))
        ans = cur.fetchall()
        if ans:
            return ans
        else:
            return 0
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()

def gun_state_search():

    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    try:
        cur.execute("SELECT * FROM gun_state WHERE state=?;",('out',))
        ans = cur.fetchall()
        if ans:
            return ans
        else:
            return 0
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()

def read_log(limit,choose):
    now=time.strftime("%Y-%m-%d", time.localtime())
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, f"../static/{choose}")
    log_file=os.path.join(log_dir, f"{now}.log")
    ans=''
    try:
        with open(log_file, 'r') as file:
            lines = file.readlines()
    except:
        return 0

    # 反轉檔案內容
    for i, line in enumerate(reversed(lines[-limit:])):
        ans+=line.strip()+'\n'
    return ans



            

