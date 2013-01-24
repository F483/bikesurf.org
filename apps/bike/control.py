from apps.bike.models import Bike


def create( team, owner, name, description, active, reserve, station, lockcode, 
            keycode, kind, gender, size, lights, fenders, rack, basket ):
    bike = Bike()
    bike.team = team
    bike.owner = owner
    bike.name = name
    bike.description = description
    bike.active = active
    bike.reserve = reserve
    bike.station = station
    bike.lockcode = lockcode
    bike.keycode = keycode
    bike.kind = kind
    bike.gender = gender
    bike.size = size
    bike.lights = lights
    bike.fenders = fenders
    bike.rack = rack
    bike.basket = basket
    bike.save()
    return bike


def edit( bike, owner, name, description, active, reserve, station, lockcode, 
            keycode, kind, gender, size, lights, fenders, rack, basket ):
    bike.owner = owner
    bike.name = name
    bike.description = description
    bike.active = active
    bike.reserve = reserve
    bike.station = station
    bike.lockcode = lockcode
    bike.keycode = keycode
    bike.kind = kind
    bike.gender = gender
    bike.size = size
    bike.lights = lights
    bike.fenders = fenders
    bike.rack = rack
    bike.basket = basket
    bike.save()
    return bike


