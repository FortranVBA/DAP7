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


class Purchase:
    """(à compléter)..."""

    def __init__(self, actions_list):
        """(à compléter)..."""
        self.actions = list(actions_list)
        self.price = self.calculate_price()
        self.brut_profit = self.calculate_brut_profit()

    def calculate_brut_profit(self):
        """(à compléter)..."""
        result = 0
        for action_name in self.actions:
            result += Action.get_all[action_name].brut_profit

        return round(result, 2)

    def calculate_price(self):
        """(à compléter)..."""
        result = 0
        for action_name in self.actions:
            result += Action.get_all[action_name].price

        return round(result, 2)


class DynamicWallet:
    """(à compléter)..."""

    def __init__(self, budget_max, action_added, previous_wallet):
        """(à compléter)..."""
        self.best_profit_by_budget = {}
        self.calculate_best_profit(budget_max, action_added, previous_wallet)

    def calculate_best_profit(self, budget_max, action_added, previous_wallet):
        """(à compléter)..."""
        max_budget_list = self.define_max_budgets(
            budget_max, action_added, previous_wallet
        )

        for max_budget in max_budget_list:
            if previous_wallet:

                no_new_purchase = previous_wallet.get_best_purchase(max_budget)

                if Action.get_all[action_added].price <= max_budget:
                    new_purchase = Purchase([action_added])
                    remaining_purchase = previous_wallet.get_best_purchase(
                        max_budget - new_purchase.price
                    )

                    if remaining_purchase:
                        profit_with_new_action = (
                            new_purchase.brut_profit + remaining_purchase.brut_profit
                        )
                    else:
                        profit_with_new_action = new_purchase.brut_profit

                    if no_new_purchase:
                        profit_without_new_action = no_new_purchase.brut_profit
                    else:
                        profit_without_new_action = 0

                    if profit_with_new_action > profit_without_new_action:
                        if remaining_purchase:
                            purchase_list = list(remaining_purchase.actions)
                        else:
                            purchase_list = []
                        purchase_list.append(action_added)
                        self.best_profit_by_budget[max_budget] = Purchase(purchase_list)
                    else:
                        self.best_profit_by_budget[max_budget] = no_new_purchase

                else:
                    self.best_profit_by_budget[max_budget] = no_new_purchase
            else:
                self.best_profit_by_budget[max_budget] = Purchase([action_added])

    def define_max_budgets(self, budget_max, action_added, previous_wallet):
        """(à compléter)..."""
        if previous_wallet:
            previous_max_budget = list(previous_wallet.best_profit_by_budget.keys())
            result = list(previous_max_budget)
            previous_max_budget.append(0)
            for budget in previous_max_budget:
                budget_with_new_action = budget + Action.get_all[action_added].price
                if budget_with_new_action <= budget_max:
                    result.append(budget_with_new_action)

            result.sort()
        else:
            result = []
            result.append(Action.get_all[action_added].price)
            result.append(budget_max)

        return result

    def get_best_purchase(self, budget):
        """(à compléter)..."""
        max_budget_list = list(self.best_profit_by_budget.keys())

        index_result = "0"
        for max_budget in max_budget_list:
            if float(max_budget) <= budget:
                index_result = max_budget

        if index_result == "0":
            return None
        else:
            return self.best_profit_by_budget[index_result]

    @staticmethod
    def find_optimum_investment(budget_max, possible_purchases):
        """(à compléter)..."""
        index_action_treated = 0
        dynamic_wallets = {}
        previous_dynamic_wallet = None
        wallet_memory_index = 0

        start_time = time.time()

        while index_action_treated < len(possible_purchases):
            dynamic_wallets[wallet_memory_index] = DynamicWallet(
                budget_max,
                possible_purchases[index_action_treated],
                previous_dynamic_wallet,
            )
            previous_dynamic_wallet = dynamic_wallets[wallet_memory_index]
            index_action_treated += 1
            wallet_memory_index += 1
            if wallet_memory_index > 2:
                wallet_memory_index = 0

        # print(previous_dynamic_wallet.best_profit_by_budget.keys())
        print(" ")
        print(" ")
        exe_time = round(time.time() - start_time, 2)
        print(f"Completed in {exe_time} seconds")
        print(" ")
        print("Optimum purchase has the following properties :")
        budget = list(previous_dynamic_wallet.best_profit_by_budget.keys())[-1]
        purchase = previous_dynamic_wallet.best_profit_by_budget[budget]
        money_left = budget_max - purchase.price
        profit = purchase.brut_profit
        print(f"{money_left}€ left, {purchase.actions} brut profit: {profit}€")


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

        DynamicWallet.find_optimum_investment(500, list(actions.keys()))


def main():
    """Program entry point."""
    app = Application()
    app.run()


main()
