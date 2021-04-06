"""Project OC DAP 7 main file."""

import copy


class Action:
    """(à compléter)..."""

    def __init__(self, name, price, profit):
        """(à compléter)..."""
        self.name = name
        self.price = price
        self.profit = profit


class Wallet:
    """(à compléter)..."""

    empty_wallets: list = []

    def __init__(self, money, actions, possible_purchases):
        """(à compléter)..."""
        self.money = money
        self.actions = actions
        self.possible_purchases = possible_purchases
        self.sub_wallet = []

    def make_purchase(self, action_name):
        """(à compléter)..."""
        self.money -= self.possible_purchases[action_name].price

        if action_name in self.actions:
            self.actions[action_name] += 1
        else:
            self.actions[action_name] = 1

    def create_sub_wallet(self, action_name):
        """(à compléter)..."""
        sub_wallet = copy.deepcopy(self)
        sub_wallet.make_purchase(action_name)
        self.sub_wallet.append(sub_wallet)

    def create_all_sub_wallets(self):
        """(à compléter)..."""
        action_names = list(self.possible_purchases.keys())
        for action_name in action_names:
            if self.possible_purchases[action_name].price <= self.money:
                self.create_sub_wallet(action_name)
            else:
                del self.possible_purchases[action_name]

        for wallet in self.sub_wallet:
            wallet.create_all_sub_wallets()

        if not self.possible_purchases:
            Wallet.empty_wallets.append(self)
            print(f"{self.money} with actions {self.actions}")


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
        main_wallet = Wallet(12, {}, actions)
        main_wallet.create_all_sub_wallets()


def main():
    """Program entry point."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
