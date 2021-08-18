file = open('vprn_sava.cfg', 'w')
file.write('')
file.close()

class MyTimer():
    def __init__(self):
        self.one = 0
        self.two = 0
        self.tre = 0
        self.vprn = 1000
        self.port_sap = 1032
    def router_(self):
        # vprn = 1000
        router = [
                f"    vprn {self.vprn} name \"{self.vprn}\" customer 1 create\n",
                f"    route-distinguisher auto-rd\n"
            ]
        for x in router:
            print(x)
            file.write(x)
        self.vprn += 1
        hovmuch = 0
        while hovmuch <= 31:
            hovmuch += 1
            config = [
                    f"        interface \"ISIS-{self.one}\" create\n",
                    f"            address 100.{self.two}.{self.tre}.1/24\n",
                    f"            sap 2/2/5:{self.port_sap}.* create\n",
                    f"            exit\n",
                    f"        exit\n",
                    f"        isis {self.one}\n",
                    f"            system-id 0000.0000.0001\n",
                    f"            level-capability level-2\n",
                    f"            area-id 49.0000\n",
                    f"            level 2\n",
                    f"                wide-metrics-only\n",
                    f"            exit\n",
                    f"            interface \"ISIS-{self.one}\"\n",
                    f"                interface-type point-to-point\n",
                    f"                no shutdown\n",
                    f"            exit\n",
                    f"            no shutdown\n",
                    f"        exit\n"
                ]
            for x in config:
                print(x)
                file.write(x)
            self.one += 1
            self.tre += 1
            self.port_sap +=1
            if self.tre == 256:
                self.two += 1
                self.tre = 0
            elif self.two == 256:
                self.tre += 1
                self.two = 0
        router2 = [
                f"    no shutdown\n",
                f"    exit\n"
            ]
        for x in router2:
            print(x)
            file.write(x)
        print(self.port_sap)
        self.one = 0
        self.two = 0
        self.tre = 0

timer = MyTimer()
hovmuch = 0

file = open('vprn_sava.cfg', 'a')

while hovmuch <= 31:
    hovmuch += 1
    timer.router_()

file.close()