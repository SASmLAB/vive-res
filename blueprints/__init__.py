from blueprints import standalone, auth, reservation

blueprint_packages = [
    standalone,
    auth,
    reservation
]

blueprints = [p.blueprint for p in blueprint_packages]
