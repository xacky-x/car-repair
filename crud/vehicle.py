from sqlalchemy.orm import Session

import models,utils,random


def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def get_vehicles_by_id(db: Session, c_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.c_id == c_id).all()

def create_random_vehicle(db: Session, num: int):
    client_list = db.query(models.Client.c_id).all()
    # print(client_list)
    # id = random.choice(client_list)
    # print(int(str(id).replace('(','').replace(')','').replace(',','')))
    db_vehicle_list = []
    for i in range(num):
        id = random.choice(client_list)
        cid = int(str(id).replace('(','').replace(')','').replace(',',''))
        db_vehicle = models.Vehicle(
            license=utils.random_license(),
            v_type=utils.random_vtype(),
            colour=utils.random_color(),
            v_class=utils.random_vclass(),
            c_id=cid
        )
        db_vehicle_list.append(db_vehicle)
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
    return db_vehicle_list

def remove_vehicle_by_id(db,v_id,c_id):
    db_vehicle = db.query(models.Vehicle).filter(models.Client.c_id == c_id,models.Vehicle.v_id==v_id).first()
    if db_vehicle:
        db.delete(db_vehicle)
    else:
        return False
    db.commit()
    db.flush()
    return True