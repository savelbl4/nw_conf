from pprint import pprint

print('\nсколько портов нужно?')
value = int(input('\n\tответ: ').strip()) # сколько портов нужно
print('\nсколько портов в изизе?')
isis_count =  int(input('\n\tответ: ').strip()) # сколько портов нужно

name_cfg = "vprn_sava.cfg" # имя конфига

# очищаем старый конфиг
file = open(name_cfg, 'w')
file.write('')
file.close()

class MyConfig():
    def __init__(self):
        self.isis_hash = {}
        self.isis = [0, 0]
        self.actet = [0, 0, 0] # второй и третий актеты
        self.list = [] # массив для имён
        self.port_sap = 1000 # первый порт

    def create_interface(self, isis_count):
        int_name = f"ISIS-{self.isis[0]}-{self.isis[1]}"

        if self.isis_hash.get(f"{self.isis[0]}") is None:
            self.isis_hash[f"{self.isis[0]}"] = []

        self.isis_hash[f"{self.isis[0]}"].append(int_name)

        config = [
                f"        interface \"{int_name}\" create\n",
                f"            address 100.{self.actet[1]}.{self.actet[2]}.1/24\n",
                f"            port 2/2/5:{self.port_sap}.*\n",
                f"            no shutdown\n",
                f"        exit\n"
            ]
        for x in config:
            file.write(x)

        self.isis[1] += 1
        self.actet[2] += 1
        self.port_sap += 1

        if self.actet[2] == 256:        # если третий актет достиг прелельного значения
            self.actet[1] += 1          # увеличим второй актет на еденицу
            self.actet[2] = 0           # и обнулим третий
        # elif self.actet[1] == 256:
        #     self.actet[2] += 1
        #     self.actet[1] = 0

        if self.isis[1] == isis_count:  # если портов больше чем влезает в изиз
            self.isis[0] += 1           # увеличим номер изиза
            self.isis[1] = 0            # и обнулим номер порта

        self.list.append(int_name) # добавляем имя интерфейса в массив

    def print_interface(self):
        pprint(self.isis_hash)
        xx = 0
        for x in self.list:
            xx += 1
            # print(x)
        print(f"\n\t\t{xx} портов создано\n")

    def create_isis(self):
        for key in self.isis_hash.keys():
            config = [ # открываем изиз
                    f"        isis {key}\n",
                    f"            system-id 0000.0000.0001\n",
                    f"            level-capability level-2\n",
                    f"            area-id 49.0000\n",
                    f"            level 2\n",
                    f"                wide-metrics-only\n",
                    f"            exit\n"
                ]
            for x in config:
                file.write(x)
            for int_name in self.isis_hash[key]: # пишем конфиг для каждого имени интерфейса в массиве
                config = [
                        f"            interface \"{int_name}\"\n",
                        f"                interface-type point-to-point\n",
                        f"                no shutdown\n",
                        f"            exit\n",
                        f"            no shutdown\n"
                    ]
                for x in config:
                    file.write(x)
            config = [ # закрываем изиз
                    f"        exit\n"
                ]
            for x in config:
                file.write(x)

master_config = MyConfig()
file = open(name_cfg, 'a')

hovmuch = -value # первый порт
while hovmuch <= -1:
    hovmuch += 1
    master_config.create_interface(isis_count)

master_config.print_interface()
master_config.create_isis()

file.close()