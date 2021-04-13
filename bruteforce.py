"""Project OC DAP 7 main file."""

import time


class Action:
    """(à compléter)..."""

    get_all: dict = {}

    def __init__(self, name, price, profit):
        """(à compléter)..."""
        self.name = name
        self.price = price
        self.profit = profit
        self.brut_profit = self.calculate_brut_profit()
        Action.get_all[self.name] = self

    def calculate_brut_profit(self):
        """(à compléter)..."""
        result = self.price * self.profit / 100
        return result


class Wallet:
    """(à compléter)..."""

    optimum_wallet = None
    to_be_treated: list = []
    completed: list = []

    def __init__(self, money, actions, possible_purchases):
        """(à compléter)..."""
        self.money = money
        self.actions = actions.copy()
        self.possible_purchases = list(possible_purchases)
        self.brut_profit = 0

    def make_purchase(self, action_name):
        """(à compléter)..."""
        self.money -= Action.get_all[action_name].price

        if action_name in self.actions:
            self.actions[action_name] += 1
        else:
            self.actions[action_name] = 1

    def create_sub_wallet(self):
        """(à compléter)..."""
        action = self.possible_purchases[0]
        self.possible_purchases.remove(action)

        wallet_no_purchase = Wallet(self.money, self.actions, self.possible_purchases)
        if wallet_no_purchase.possible_purchases:
            Wallet.to_be_treated.append(wallet_no_purchase)
        else:
            Wallet.completed.append(wallet_no_purchase)
            wallet_no_purchase.calculate_brut_profit()

        if Action.get_all[action].price <= self.money:
            wallet_purchase = Wallet(self.money, self.actions, self.possible_purchases)
            wallet_purchase.make_purchase(action)
            if wallet_no_purchase.possible_purchases:
                Wallet.to_be_treated.append(wallet_purchase)
            else:
                Wallet.completed.append(wallet_purchase)
                wallet_purchase.calculate_brut_profit()

    def calculate_brut_profit(self):
        """(à compléter)..."""
        result = 0
        for action_name, action_number in self.actions.items():
            result += action_number * Action.get_all[action_name].brut_profit

        self.brut_profit = result
        self.test_optimum_wallet()

    def test_optimum_wallet(self):
        """(à compléter)..."""
        if not Wallet.optimum_wallet:
            Wallet.optimum_wallet = self
        else:
            if Wallet.optimum_wallet.brut_profit < self.brut_profit:
                Wallet.optimum_wallet = self

    @staticmethod
    def find_optimum_investment():
        """(à compléter)..."""
        REFRESH_PRINT = 20000
        refresh_counter = REFRESH_PRINT
        combinaison_treated = 0
        total_combinaison = 2 ** len(Action.get_all)
        start_time = time.time()
        while Wallet.to_be_treated:
            Wallet.to_be_treated[0].create_sub_wallet()
            del Wallet.to_be_treated[0]
            combinaison_treated += 1
            refresh_counter -= 1
            if refresh_counter == 0:
                pourcent_progress = round(
                    combinaison_treated * 100 / total_combinaison, 2
                )
                print(f"Progress : {pourcent_progress}%")
                refresh_counter = REFRESH_PRINT

        print(" ")
        print(" ")
        exe_time = round(time.time() - start_time, 2)
        print(f"Completed wallets: {len(Wallet.completed)} in {exe_time} seconds")
        print(" ")
        print("Optimum wallet has the following properties :")
        wallet = Wallet.optimum_wallet
        profit = round(wallet.brut_profit, 2)
        print(f"{wallet.money}€ left, {wallet.actions} brut profit: {profit}€")


class Application:
    """Project application class."""

    def __init__(self):
        """Init Application class."""
        pass

    def run(self):
        """Run the application."""
        actions = {
            "Action-1": Action("Action-1", 20, 5),
            "Action-2": Action("Action-2", 30, 10),
            "Action-3": Action("Action-3", 50, 15),
            "Action-4": Action("Action-4", 70, 20),
            "Action-5": Action("Action-5", 60, 17),
            "Action-6": Action("Action-6", 80, 25),
            "Action-7": Action("Action-7", 22, 7),
            "Action-8": Action("Action-8", 26, 11),
            "Action-9": Action("Action-9", 48, 13),
            "Action-10": Action("Action-10", 34, 27),
            "Action-11": Action("Action-11", 42, 17),
            "Action-12": Action("Action-12", 110, 9),
            "Action-13": Action("Action-13", 38, 23),
            "Action-14": Action("Action-14", 14, 1),
            "Action-15": Action("Action-15", 18, 3),
            "Action-16": Action("Action-16", 8, 8),
            "Action-17": Action("Action-17", 4, 12),
            "Action-18": Action("Action-18", 10, 14),
            "Action-19": Action("Action-19", 24, 21),
            "Action-20": Action("Action-20", 114, 18),
        }
        main_wallet = Wallet(500, {}, list(actions.keys()))
        Wallet.to_be_treated.append(main_wallet)

        Wallet.find_optimum_investment()


def main():
    """Program entry point."""
    app = Application()
    app.run()


main()
