import random
from faker import Faker
from sqlalchemy import DateTime
fake = Faker(locale='zh_CN')


def random_name():
    sex = random.choice(range(2))
    # 生成并返回一个名字
    if sex > 0:
        return fake.name_female()
    else:
        return fake.name_male()


def random_company():
    return fake.company()


def random_discount():
    discount_list = ['50', '55', '60', '65', '70', '75', '80', '85', '90', '95', '100']
    return random.choice(discount_list)


def random_phone():
    return fake.phone_number()


def random_license():
    return fake.license_plate()


def random_type():
    type_list = ["机修", "钣金", "电工", "喷漆"]
    return random.choice(type_list)


def random_hour():
    hour_list = [20, 30, 40, 50, 60, 70, 80]
    return random.choice(hour_list)


# 维修表的假数据
def random_r_type():
    type_list = ['普通', '加急']
    return random.choice(type_list)


def random_r_class():
    class_list = ['大修', '中修', '小修']
    return random.choice(class_list)


def random_payment():
    pay_list = ['自付', '三包', '进保']
    return random.choice(pay_list)


def random_mileage():
    return round(random.uniform(100000, 1000000), 2)


def random_fuel():
    return round(random.uniform(0,1), 2)


def random_approach_time():
    # 进场日期
    return fake.date_time_between(start_date="-5y", end_date="now", tzinfo=None)


def random_failure():
    # 故障描述(单个段落)
    return fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)


def random_completion_time():
    # 预计完工时间(未来日期）
    return fake.future_date(end_date="+30d", tzinfo=None)


def random_date():
    return fake.past_date(start_date="-30d", tzinfo=None)


def random_cost():
    return round(random.uniform(50, 1000), 2)


def random_id():
    return 1


if __name__ == '__main__':
    for i in range(10):
        # print(random_license())
        print(random_approach_time())
