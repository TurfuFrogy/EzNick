import aiohttp, asyncio, tasksio, os, ctypes, datetime
from colorama import Fore, init; init(autoreset=True, convert=True)

class EzNick:
    def __init__(self):
        if os.name == "nt":
            os.system("mode con: cols=138 lines=30")

        self.session = aiohttp.ClientSession()

        self.ratelimitPause = False

        self.available = 0
        self.unavailable = 0
        self.errors = 0

        # Maybe proxy support later
        # self.proxiesScraped = False

    def title(self, title: str):
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(f"EzNick | By Frogy | {title}")
        else:
            print(f"\33]0;EzNick | By Frogy | {title}\a", end="", flush=True)

    def logo(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        print(f"""{Fore.LIGHTMAGENTA_EX}
                                              ███████╗███████╗███╗   ██╗██╗ ██████╗██╗  ██╗
                                              ██╔════╝╚══███╔╝████╗  ██║██║██╔════╝██║ ██╔╝
                                              █████╗    ███╔╝ ██╔██╗ ██║██║██║     █████╔╝ 
                                              ██╔══╝   ███╔╝  ██║╚██╗██║██║██║     ██╔═██╗ 
                                              ███████╗███████╗██║ ╚████║██║╚██████╗██║  ██╗
                                              ╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝ ╚═════╝╚═╝  ╚═╝
                                                             {Fore.LIGHTCYAN_EX}A Minecraft OG Nick Checker by Frogy

{Fore.RESET}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n
        """)

    # Maybe proxy support later
    # async def scrapeProxies(self):
    #     while True:
    #         async with self.session.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all") as response:
    #             proxies = await response.text()
    #             self.proxies = itertools.cycle(proxies.splitlines())

    #             self.proxiesScraped = True

    #             time.sleep(10)

    async def cpm(self):
        while True:
            totalChecked = self.available + self.unavailable

            if totalChecked >= len(self.nicksFile):
                break

            if totalChecked != 0:
                self.title(f"[{totalChecked}/{len(self.nicksFile)}] CPM - {int(totalChecked / ((loop.time() - self.startedAt) / 60))} | Available - {self.available} | Un-Available - {self.unavailable} | Errors - {self.errors}")

            await asyncio.sleep(0.1)

    # Not sure if it works very well so feel free to fix it
    async def ratelimitHandler(self):
        while True:
            totalChecked = self.available + self.unavailable

            if totalChecked >= len(self.nicksFile):
                break

            errorsBefore = self.errors            

            await asyncio.sleep(10)

            errorsAfter = self.errors

            if errorsAfter - errorsBefore >= 25:
                self.ratelimitPause = True

                await asyncio.sleep(120)

                self.ratelimitPause = False

    async def check(self, chunk: list):
        chunk = [x for x in chunk if x] # Remove empty strings

        for nick in chunk:           
            retries = 0
            while retries != self.retries:           
                while self.ratelimitPause:
                    print(f"{Fore.LIGHTRED_EX}[RateLimited] Sleeping for 120 seconds!")

                    await asyncio.sleep(1)

                async with self.session.head(f"https://api.mojang.com/users/profiles/minecraft/{nick}") as response:
                    statusCode = response.status

                    if statusCode == 204:
                        self.available += 1

                        if not os.path.exists(f"results/{self.date}"):
                            os.makedirs(f"results/{self.date}")

                        with open(f"results/{self.date}/available.txt", "a", encoding="utf-8") as file:
                            file.write(f"{nick}\n")
                            file.close()

                        print(f"{Fore.LIGHTGREEN_EX}[Available] {nick} (https://fr.namemc.com/profile/{nick})")

                        break
                    elif statusCode == 200:
                        self.unavailable += 1

                        if not os.path.exists(f"results/{self.date}"):
                            os.makedirs(f"results/{self.date}")

                        with open(f"results/{self.date}/unavailable.txt", "a", encoding="utf-8") as file:
                            file.write(f"{nick}\n")
                            file.close()

                        if self.showUnavailable:
                            print(f"{Fore.LIGHTRED_EX}[Un-Available] {nick} (https://fr.namemc.com/profile/{nick})")

                        break
                    else:
                        self.errors += 1
                        retries += 1

                        if self.showErrors:
                            print(f"{Fore.LIGHTYELLOW_EX}[Error - {statusCode}] {nick} ({self.retries - retries} retries left)")

            self.unavailable += 1

    async def starter(self):
        self.title("Initialization")

        while True:
            try:
                self.logo()

                self.nicksFile = open(input(f"{Fore.LIGHTYELLOW_EX}Please enter the name of the file that contains the nicknames (with .extension).\n\n{Fore.RESET}~# "), encoding="utf-8").read().splitlines()

                break
            except KeyboardInterrupt:
                exit()
            except:
                pass

        if len(self.nicksFile) == 0:
            self.logo()
            return print(f"{Fore.LIGHTRED_EX}The list of nicknames you just specified is empty.")

        while True:
            try:
                self.logo()

                threadCount = int(input(f"{Fore.LIGHTYELLOW_EX}Please enter the number of parallel checks (suggested: 3).\n\n{Fore.RESET}~# "))

                break
            except KeyboardInterrupt:
                exit()
            except:
                pass

        while True:
            try:
                self.logo()

                self.retries = int(input(f"{Fore.LIGHTYELLOW_EX}Please enter the number of retries you want if the verification fails (suggested: 3).\n\n{Fore.RESET}~# "))

                break
            except KeyboardInterrupt:
                exit()
            except:
                pass

        while True:
            try:
                self.logo()

                self.showUnavailable = input(f"{Fore.LIGHTYELLOW_EX}Do you want un-available nicknames to be displayed? (y/n).\n\n{Fore.RESET}~# ").lower()

                if self.showUnavailable in ["y", "n"]:
                    break
            except KeyboardInterrupt:
                exit()
            except:
                pass

        while True:
            try:
                self.logo()

                self.showErrors = input(f"{Fore.LIGHTYELLOW_EX}Do you want checking errors to be displayed? (y/n).\n\n{Fore.RESET}~# ").lower()

                if self.showErrors in ["y", "n"]:
                    break
            except KeyboardInterrupt:
                exit()
            except:
                pass

        self.title("Starting")
        self.logo()

        self.startedAt = loop.time()
        self.date = datetime.datetime.now().strftime("%d-%m-%Y %Hh%Mm%Ss")

        nicksChunks = [self.nicksFile[i::threadCount] for i in range(threadCount)]

        async with tasksio.TaskPool(threadCount + 2) as pool:
            await pool.put(self.cpm())
            await pool.put(self.ratelimitHandler())
            for chunk in nicksChunks:
                await pool.put(self.check(chunk))

        self.title("Finished")
        self.logo()
        print(f"{Fore.LIGHTYELLOW_EX}Checking Finished! Results here: results/{self.date}/")

        input()

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(EzNick().starter())
    except KeyboardInterrupt:
        exit()