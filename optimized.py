"""Project OC DAP 7 main file."""

import time
import csv
import numpy as np
import math

FIND_INTERVAL = False
REFRESH_PRINT = 5
ROUND_PURCHASE = True
MIN_METHOD = True
CSV_FILE = "dataset2.csv"


class Action:
    """Project Action class."""

    get_all: dict = {}

    def __init__(self, name, price, profit):
        """Init Action class."""
        self.name = name
        self.price = price
        self.profit = profit
        self.brut_profit = self.calculate_brut_profit()

        if ROUND_PURCHASE:
            self.price = math.ceil(price)

        Action.get_all[self.name] = self

    def calculate_brut_profit(self):
        """Calculate action brut profit."""
        result = self.price * self.profit / 100
        return result

    @staticmethod
    def read_csv(csv_name):
        """Read action data from csv file."""
        result = {}

        with open(csv_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    # Name / Price / Profit
                    line_count += 1
                else:
                    name = row[0]
                    price = round(float(row[1]), 2)
                    profit = round(float(row[2]), 2)
                    if price > 0:
                        result[name] = Action(name, price, profit)
                    line_count += 1

        return result


class Purchase:
    """Project Purchase class."""

    def __init__(self, actions_list):
        """Init Purchase class."""
        self.actions = list(actions_list)
        self.price = self.calculate_price()
        self.brut_profit = self.calculate_brut_profit()

    def calculate_brut_profit(self):
        """Calculate purchase brut profit."""
        result = 0
        for action_name in self.actions:
            result += Action.get_all[action_name].brut_profit

        return round(result, 2)

    def calculate_price(self):
        """Calculate purchase price."""
        result = 0
        for action_name in self.actions:
            result += Action.get_all[action_name].price

        return round(result, 2)


class DynamicWallet:
    """Project DynamicWallet class."""

    fix_max_budgets: list = []

    def __init__(self, budget_max, action_added, previous_wallet):
        """Init DynamicWallet class."""
        self.best_profit_by_budget = {}
        self.calculate_best_profit(budget_max, action_added, previous_wallet)

    def calculate_best_profit(self, budget_max, action_added, previous_wallet):
        """Calculate best purchase for profit for dynamic wallet."""
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
                if Action.get_all[action_added].price <= max_budget:
                    self.best_profit_by_budget[max_budget] = Purchase([action_added])
                else:
                    self.best_profit_by_budget[max_budget] = None

    def define_max_budgets(self, budget_max, action_added, previous_wallet):
        """Define the budget studied for best purchases."""
        if FIND_INTERVAL:
            if previous_wallet:
                previous_max_budget = list(previous_wallet.best_profit_by_budget.keys())
                result = list(previous_max_budget)
                previous_max_budget.append(0)
                for budget in previous_max_budget:
                    budget_with_new_action = budget + Action.get_all[action_added].price
                    if budget_with_new_action <= budget_max:
                        if budget_with_new_action not in result:
                            result.append(budget_with_new_action)

            else:
                result = []
                result.append(Action.get_all[action_added].price)
                result.append(budget_max)
        else:
            if DynamicWallet.fix_max_budgets:
                result = DynamicWallet.fix_max_budgets
            else:
                if ROUND_PURCHASE:
                    interval = 1
                else:
                    interval = 0.01

                np_list = np.arange(interval, budget_max + interval, interval)
                DynamicWallet.fix_max_budgets = [round(n, 2) for n in np_list]
                result = DynamicWallet.fix_max_budgets

        return result

    def get_best_purchase(self, budget):
        """Get the dynamic wallet best purchase associated with a fixed budget."""
        if FIND_INTERVAL:
            max_budget_list = list(self.best_profit_by_budget.keys())

            if MIN_METHOD:
                lower_budget_list = [
                    element for element in max_budget_list if budget - element >= 0
                ]
                if lower_budget_list:
                    index_result = min(lower_budget_list, key=lambda x: (budget - x))
                else:
                    index_result = 0

                index_result = index_result
            else:
                index_result = 0
                for max_budget in max_budget_list:
                    if float(max_budget) <= budget:
                        if index_result < float(max_budget):
                            index_result = max_budget

            if index_result == 0:
                return None
            else:
                return self.best_profit_by_budget[index_result]
        else:
            if round(budget, 2) < 0.01:
                return None
            else:
                return self.best_profit_by_budget[round(budget, 2)]

    @staticmethod
    def find_optimum_investment(budget_max, possible_purchases):
        """Find the optimum investment with dynamic wallets creation."""
        refresh_counter = REFRESH_PRINT

        index_action_treated = 0
        total_actions = len(possible_purchases)
        dynamic_wallets = {}
        previous_dynamic_wallet = None
        wallet_memory_index = 0

        start_time = time.time()

        while index_action_treated < total_actions:
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

            refresh_counter -= 1
            if refresh_counter == 0:
                pourcent_progress = round(index_action_treated * 100 / total_actions, 2)
                print(f"Progress : {pourcent_progress}%")
                refresh_counter = REFRESH_PRINT

        print(" ")
        print(" ")
        exe_time = round(time.time() - start_time, 2)
        print(f"Completed in {exe_time} seconds")
        print(" ")
        print("Optimum purchase has the following properties :")
        budget = max(list(previous_dynamic_wallet.best_profit_by_budget.keys()))
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
        actions = Action.read_csv(CSV_FILE)

        DynamicWallet.find_optimum_investment(500, list(actions.keys()))


def main():
    """Program entry point."""
    app = Application()
    app.run()


main()
