import os
import sqlite3
from collections import Counter
from datetime import datetime, timedelta
CCSCORE_DB_PATH = os.path.expanduser('~/.hoshino/CC_counter.db')




# 用于与赛跑金币互通
class CCScoreCounter:
    def __init__(self):
        os.makedirs(os.path.dirname(CCSCORE_DB_PATH), exist_ok=True)
        self._create_table()
    def _connect(self):
        return sqlite3.connect(CCSCORE_DB_PATH)

    def _create_table(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS CCSCORE
                          (
                           UID             INT    NOT NULL,
                           SCORE           INT    NOT NULL,
                           PRIMARY KEY(UID));''')
        except:
            raise Exception('创建表发生错误')
            
    def _add_score(self,uid, score):
        try:
            current_score = self._get_score(uid,)
            conn = self._connect()
            conn.execute("INSERT OR REPLACE INTO CCSCORE (UID,SCORE) \
                                VALUES (?,?)", (uid, int(current_score + score)))
            conn.commit()
        except:
            current_score = self._get_score(uid,)
            if (current_score + score) >= 9223372036854775806:
                conn = self._connect()
                conn.execute("INSERT OR REPLACE INTO CCSCORE (UID,SCORE) \
                                VALUES (?,?)", (uid, int(9223372036854775806)))
                conn.commit()
                print('金币超出上限！')
            else:
                raise Exception('更新表发生错误')

    def _reduce_score(self,uid, score):
        try:
            current_score = self._get_score(uid,)
            if current_score >= score:
                conn = self._connect()
                conn.execute("INSERT OR REPLACE INTO CCSCORE (UID,SCORE) \
                                VALUES (?,?)", (uid, current_score - score))
                conn.commit()
            else:
                conn = self._connect()
                conn.execute("INSERT OR REPLACE INTO CCSCORE (UID,SCORE) \
                                VALUES (?,?)", (uid, 0))
                conn.commit()
        except:
            raise Exception('更新表发生错误')

    def _get_score(self, uid):
        try:
            r = self._connect().execute("SELECT SCORE FROM CCSCORE WHERE UID=?", (uid,)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')

#判断金币是否足够下注
    def _judge_score(self, uid ,score):
        try:
            current_score = self._get_score(uid)
            if current_score >= score:
                return 1
            else:
                return 0
        except Exception as e:
            raise Exception(str(e))