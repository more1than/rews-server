from app.models.disk import Base as Base_disk
from app.models.nodes import Base as Base_vm
from app.models.region import Base as Base_region
from app.models.network import Base as Base_new_work
from app.models.external_resource import Base as Base_external_resource
from app.models.alert_logs import Base as Base_alert_logs
from app.models.account import Base as Base_account, Account
from app.models.peoples import Base as Base_people, Peoples
from pkg.create_con import create_con
from pkg.create_engine import create_myengine
from pkg.util.setting import setting

engine = create_myengine()


def init_db():
    Base_vm.metadata.create_all(engine)
    Base_disk.metadata.create_all(engine)
    Base_region.metadata.create_all(engine)
    Base_new_work.metadata.create_all(engine)
    Base_people.metadata.create_all(engine)
    Base_external_resource.metadata.create_all(engine)
    Base_alert_logs.metadata.create_all(engine)
    Base_account.metadata.create_all(engine)
    people_msg = setting.get_email_config()
    mail = people_msg.get("mail_user")
    con = create_con()
    people = con.query(Peoples).filter_by(mail=mail).first()
    if people:
        people.name = people_msg.get("mail_name")
        people.mail = people_msg.get("mail_user")
        people.phone = people_msg.get("phone")
        con.merge(people)
        con.commit()
    else:
        people = Peoples()
        people_msg = setting.get_email_config()
        people.name = people_msg.get("mail_name")
        people.mail = people_msg.get("mail_user")
        people.phone = people_msg.get("phone")
        con.add(people)
        con.commit()
    accounts = con.query(Account).all()
    if not accounts:
        acc = Account()
        tty_data = setting.get_tty_config()
        acc.name = tty_data.get("AccountName")
        acc.cloud_type = tty_data.get("Provider")
        acc.api_key = tty_data.get("AccessKey")
        acc.api_sec = tty_data.get("SecurityKey")
        con.add(acc)
        con.commit()
    con.close()


def drop_db():
    Base_disk.metadata.drop_all(engine)
    Base_vm.metadata.drop_all(engine)
    Base_region.metadata.drop_all(engine)
    Base_new_work.metadata.drop_all(engine)
