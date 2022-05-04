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

def random_license():
    char0 = ["京", "津", "沪", "渝", "冀", "豫", "云", "辽", "黑", "湘", "皖", "鲁", "新", "苏", "浙", "赣", "鄂", "桂", "甘", "晋", "蒙",
             "陕", "吉", "闽", "赣", "粤", "青", "藏", "川", "宁", "琼"]  # 省份简称
    char1 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'  # 车牌号中没有I和O
    char2 = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'

    id_1 = random.choice(char0)  # 车牌号第一位     省份简称
    id_2 = ''.join(random.sample(char1, 1))  # 车牌号第二位

    while True:
        id_3 = ''.join(random.sample(char2, 5))
        v = id_3.isalpha()  # 所有字符都是字母时返回 true
        if v == True:
            continue
        else:
            car_id = id_1 + id_2 + id_3
            break

    return car_id

def random_vtype():
    vtype_list = ["SUV", "MPV", "HATCHBACK", "COUPE","ROADSTER"]
    return random.choice(vtype_list)

def random_color():
    color_list=["红色","蓝色","黑色","灰色","白色","金色"]
    return color_list

def random_vclass():
    vclass_list=["微型车","中型车","中大型车","小型车","豪华车"]
    return vclass_list

if __name__ == '__main__':
    for i in range(10):
        print(random_license())
