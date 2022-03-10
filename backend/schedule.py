import pymysql
import datetime
conn = pymysql.connect(host='localhost', user='root', password='bsideand59min', db='bside', charset='utf8')

cur = conn.cursor()

sql = "select * from pybo_meet where rm_status = 'Y'"
cur.execute(sql)
meets = cur.fetchall()

for meet in meets:
    last_time = meet[-2]
    now = datetime.datetime.now()
    if last_time.year == now.year:
        if last_time.month == now.month:
            if last_time.day+15 == now.day:
                # agenda
                sql = "select * from pybo_agenda WHERE meet_id = %s"
                cur.execute(sql, (meet[0]))
                agendas = cur.fetchall()
                for agenda in agendas:
                    # action
                    sql = "select * from pybo_action WHERE agenda_id = %s"
                    cur.execute(sql, (agenda[0]))
                    actions = cur.fetchall()
                    for action in actions:
                        sql = "DELETE FROM pybo_action WHERE action_id = %s"
                        cur.execute(sql, (action[0]))
                        # conn.commit()
                    print(cur.rowcount, "pybo_action rows deleted")

                    #agenda_progress
                    sql = "select * from pybo_agenda_progress WHERE agenda_id = %s"
                    cur.execute(sql, (agenda[0]))
                    agenda_progress = cur.fetchall()
                    for progress in agenda_progress:
                        sql = "DELETE FROM pybo_agenda_progress WHERE agenda_id = %s"
                        cur.execute(sql, (agenda[0]))
                        conn.commit()
                    print(cur.rowcount, "agenda_progress rows deleted")

                    sql = "DELETE FROM pybo_agenda WHERE agenda_id = %s"
                    cur.execute(sql, (agenda[0]))
                    print(cur.rowcount, "pybo_agenda rows deleted")
                    # conn.commit()
                # selfcheck
                sql = "select * from pybo_selfcheck WHERE meet_id = %s"
                cur.execute(sql, (meet[0]))
                selfchecks = cur.fetchall()
                for selfcheck in selfchecks:
                    sql = "DELETE FROM pybo_selfcheck WHERE meet_id = %s"
                    cur.execute(sql, (selfcheck[5]))
                print(cur.rowcount, "pybo_selfcheck rows deleted")
                sql = "DELETE FROM pybo_meet WHERE meet_id = %s"
                cur.execute(sql, (meet[0]))
                conn.commit()
                print(cur.rowcount, "pybo_meet rows deleted")
