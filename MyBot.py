import hlt
import logging

# GAME START
game = hlt.Game("tatuf")
logging.info("tatuf bot is ready !")
planetsAimed = []

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    # For every ship that I control
    for ship in game_map.get_me().all_ships():
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        # For each planet in the game (only non-destroyed planets are included)
        for planet in game_map.all_planets(): 
            # If the planet is owned
            if planet.is_owned():
                # Skip this planet
                continue

            # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
            if ship.can_dock(planet):
                # We add the command by appending it to the command_queue
                command_queue.append(ship.dock(planet))
            else:
                if planet in planetsAimed:
                    continue
                else:
                    navigate_command = ship.navigate(
                        ship.closest_point_to(planet),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)
                    # If the move is possible, add it to the command_queue 
                    # if there are too many obstacles on the way navigate_command will return null
                    if navigate_command:
                        command_queue.append(navigate_command)
                        planetsAimed.append(planet)
            break

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
