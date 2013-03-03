from apps.bike.models import Bike


def create( team, owner, name, description, active, reserve, station, lockcode, 
            size, lights ):
    bike = Bike()
    bike.team = team
    bike.owner = owner
    bike.name = name
    bike.description = description
    bike.active = active
    bike.reserve = reserve
    bike.station = station
    bike.lockcode = lockcode
    bike.size = size
    bike.lights = lights
    bike.save()
    return bike


def edit( bike, owner, name, description, active, reserve, station, lockcode, 
          size, lights ):
    bike.owner = owner
    bike.name = name
    bike.description = description
    bike.active = active
    bike.reserve = reserve
    bike.station = station
    bike.lockcode = lockcode
    bike.size = size
    bike.lights = lights
    bike.save()
    return bike


