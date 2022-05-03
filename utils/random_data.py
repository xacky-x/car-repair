import random
from faker import Faker

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


if __name__ == '__main__':
    for i in range(10):
        print(random_license())
