# 引入sqlalchemy依赖
from sqlalchemy import Column, Integer, String, Date, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
"""
基于 sqlalchemy 实现
"""

# 申明基类对象
Base = declarative_base()

class QrFortune:
    __tablename__='qr_fortune'
    id = Column(Integer, primary_key=True)
    fortune_summary = Column(String(255))
    lucky_star = Column(String(255))
    sign_text= Column(String(255))
    un_sign_text = Column(String(255))
    def __repr__(self):
        return ("QrFortune(id:{},fortune_summary:{},lucky_star:{},sign_text:{},un_sign_text:{})"
                .format(self.id,self.fortune_summary,self.lucky_star,self.sign_text,self.un_sign_text))

class QrFortuneLog:
    __tablename__ = 'qr_fortune_log'
    id = Column(Integer, primary_key=True)
    fortune_summary = Column(String(255))
    lucky_star = Column(String(255))
    sign_text = Column(String)
    un_sign_text = Column(String(255))
    user_id = Column(String(255))
    extract_time = Column(Date)
    def __repr__(self):
        return ("QrFortune(id:{},fortune_summary:{},lucky_star:{},sign_text:{},un_sign_text:{})"
                .format(self.id, self.fortune_summary, self.lucky_star, self.sign_text, self.un_sign_text))



class SqliteSqlalchemy(object):
    def __init__(self):
        # 创建Sqlite连接引擎
        engine = create_engine('sqlite:///./chat_bot.db', echo=True)
        # 创建Sqlite的session连接对象
        self.session = sessionmaker(bind=engine)()



# 查询 今日运势
selectFortune = text("select * from qr_fortune  order by random() limit 1")
#根据 id 查询是否生抽取过今日运势
selectFortuneLog = text("select * from qr_fortune_log where user_id = :member_openid  and extract_time = date('now')")
#插入日志表
insertFortuneLog = text(" insert into qr_fortune_log (fortune_summary, lucky_star, sign_text,un_sign_text,user_id,extract_time) values (:fortune_summary, :lucky_star, :sign_text,:un_sign_text,:member_openid,date('now'))")


def get_today_fortune(member_openid):
    # 查询今日是否已经获取过今日运势，如果获取过则直接从日志取
    result = is_get_fortune_log(member_openid)
    if result is not None:
        result = ("\n" + "您的今日运势为：" + "\n" +
                  result.fortune_summary + "\n" +
                  result.lucky_star+ "\n" +
                  "签文：" + result.sign_text + "\n" +
                  "————————————————————" + "\n" +
                  "解签：" + result.un_sign_text)
        return result
    elif result is None:
        # 获取 运势说明
        result = get_fortune()
        # 把抽取的今日运势插入日志
        q = QrFortuneLog()
        q.fortune_summary = result.fortune_summary
        q.lucky_star = result.lucky_star
        q.sign_text = result.sign_text
        q.un_sign_text = result.un_sign_text
        q.user_id = member_openid
        insert_fortune_log(q)
        result = ("\n" + "您的今日运势为：" + "\n" +
                  result.fortune_summary + "\n" +
                  result.lucky_star+ "\n" +
                  "签文：" + result.sign_text + "\n" +
                  "————————————————————" + "\n" +
                  "解签：" + result.un_sign_text)
        return result



# 查询今日是否已经获取过今日运势，如果获取过则直接从日志取
def is_get_fortune_log(member_openid):
    session = SqliteSqlalchemy().session
    result = session.execute(selectFortuneLog, {'member_openid': member_openid}).fetchone()
    return result

def get_fortune():
    session = SqliteSqlalchemy().session
    result = session.execute(selectFortune).fetchone()
    return result

def insert_fortune_log(QrFortuneLog):
    session = SqliteSqlalchemy().session
    session.execute(insertFortuneLog, {'fortune_summary':QrFortuneLog.fortune_summary,'lucky_star':QrFortuneLog.lucky_star,'sign_text':QrFortuneLog.sign_text,
                                                'un_sign_text':QrFortuneLog.un_sign_text,'member_openid':QrFortuneLog.user_id
                                                })
    session.commit()
    session.close()
    return ""




if __name__ == '__main__':
    result = get_today_fortune('8A91A2F3BE5B5AF3FEC97FB5AA6D9B38')
    print(result)
    # session.close()

