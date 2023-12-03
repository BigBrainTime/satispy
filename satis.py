import requests, time, json, pygui, pygame
import matplotlib.pyplot as plt

history = []


def connections(tick):
    connections = ['getPower']#, 'getWorldInv', 'getProdStats', 'getPlayer']
    data = []
    msg = ''
    for connection in connections:
        try:
            request = requests.get(
                f'http://localhost:8080/{connection}', verify=False)
        except:
            return False
        raw = (json.loads(request.content))

        match connection:
            case 'getPower':
                capacity_total = 0
                production_total = 0
                consumed_total = 0
                max_consumtion = 0

                msg += '__**Power**__\n'

                for item in raw:
                    capacity_total += item['PowerCapacity']
                    production_total += item['PowerProduction']
                    consumed_total += item['PowerConsumed']
                    max_consumtion += item['PowerMaxConsumed']
                    msg += f"Circuit: {item['CircuitID']}\nPower Capacity: {int(item['PowerCapacity'])}\nPower Production: {int(item['PowerProduction'])}\nPower Consumed: {int(item['PowerConsumed'])}\nPower Max Consumed: {int(item['PowerMaxConsumed'])}\nFuse Triggered: {item['FuseTriggered']}\n"

                msg += '**-----------------------**\n'

                y_axis = [int(capacity_total), int(production_total), int(
                    consumed_total), int(max_consumtion)]
                history.append(y_axis)
                if len(history) >= 100:
                    history.pop(0)

                capacity_axis = []
                production_axis = []
                consumed_axis = []
                max_axis = []

                for axis in history:
                    capacity_axis.insert(0, axis[0])
                    production_axis.insert(0, axis[1])
                    consumed_axis.insert(0, axis[2])
                    max_axis.insert(0, axis[3])

                time_axis = range(len(history))

                plt.clf()
                plt.plot(time_axis, capacity_axis, label='Capacity')
                plt.plot(time_axis, production_axis, label='Production')
                plt.plot(time_axis, consumed_axis, label='Consumed')
                plt.plot(time_axis, max_axis, label='Max Consumed')
                plt.xlabel(f'Ticks ago({tick} Seconds)')
                plt.ylabel('MW')
                plt.title('Power Graph')
                plt.legend()
                plt.savefig('satispower.png')

            case 'getWorldInv':
                sorted = []
                for item in raw:
                    temp = f"{item['Name']}: {item['Amount']}"
                    sorted.append(f'{temp}\n')

                msg += '__**World Inventory**__\n'
                sorted.sort()
                for item in sorted:
                    msg += f'{item}'

                msg += '**-----------------------**\n'

            case 'getProdStats':
                sorted = []
                for item in raw:
                    temp = f"{item['Name']}\n{item['ProdPerMin']}"
                    sorted.append(f'{temp}\n')

                msg += '__**Production Stats**__\n'
                sorted.sort()
                for item in sorted:
                    msg += f'{item}'

                msg += '**-----------------------**\n'

            case 'getPlayer':
                sorted = []
                for item in raw:
                    temp = f"{item['PlayerName']}\n[HP:{item['PlayerHP']}]\n[Ping:{item['PingTime']}]"
                    sorted.append(f'{temp}\n')

                msg += '__**Players**__\n'
                sorted.sort()
                for item in sorted:
                    msg += f'{item}'

                # msg += '**-----------------------**\n'

            case _:
                pass

    data.append(msg)

    return data


pygame.init()

SIZE = (900, 500)
TPS = 10
WINDOW = pygame.display.set_mode(SIZE, pygame.RESIZABLE)

image = pygui.image(0,0,100,100,SIZE[0],SIZE[1],'satispower.png')

objects = [image]

def main():
    global SIZE

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(TPS)

        SIZE = WINDOW.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        connections(TPS)
        WINDOW.fill(pygui.COLOR['BLACK'])
        image.change_image('satispower.png')

        for object in objects:
            object.process(WINDOW, SIZE[0], SIZE[1])

        pygame.display.flip()


if __name__ == '__main__':
    main()

pygame.quit()
quit()
