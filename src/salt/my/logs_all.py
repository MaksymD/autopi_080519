services():
    service = os.system('service --status-all')
    return {"msg": "List of services: " + str(service)}