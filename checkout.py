from typing import List, Dict
from collections import Counter


def checkout(item_list: List[str], price_dict: Dict[str, float], raise_error: bool = True) -> float:
    """
    A reusable function to checkout all items in shopping list
    :param item_list: List of item codes
    :param price_dict: Item price dictionary
    :param raise_error: Wether to raise error when item code is not in price dictionary
    :return:
    """
    if not item_list:
        return 0
    counter = Counter(item_list)
    if any(x not in [*price_dict] for x in [*counter]):
        error_items = list({*counter} - {*price_dict})
        error_msg = f"Cannot find price for item{'s' if len(error_items) > 1 else ''}: {', '.join(error_items)}"
        print(error_msg)
        if raise_error:
            raise ValueError(error_msg)
    return sum([_checkout_item(item_code, price_dict[item_code], item_count) for item_code, item_count in
                counter.items()])


class Checkout:
    def __init__(self, prices: Dict[str, float] = None, raise_price_not_found_error: bool = False) -> None:
        if prices is None:
            prices = {}
        self.prices = prices
        self.items = []  # type: List[str]
        self.raise_error = raise_price_not_found_error

    def scan(self, item_code: str) -> List[str]:
        self.items.append(item_code)
        return self.items

    def total(self) -> float:
        return checkout(self.items, self.prices, self.raise_error)

    def reset(self) -> List[str]:
        self.items = []
        return self.items

    def update_price(self, item_code: str, item_price: float) -> Dict[str, float]:
        self.prices[item_code] = item_price
        return self.prices

    def set_prices(self, prices: Dict[str, float] = None) -> Dict[str, float]:
        self.prices = prices
        return self.prices


def _group_offer_price(group_size: int, group_price: float, item_count: int,
                       item_price: float) -> float:
    """
    A reusable function to calculate items with multi-buy offer
    :param group_size: Offer group size, e.g. Three for two, group size is 3
    :param group_price: Offer price for the group, e.g. Three for £100, group price is £100
    :param item_count: Total item count
    :param item_price: Item price
    :return: Final price for all items in the same group
    """
    div, mod = divmod(item_count, group_size)
    return div * group_price + mod * item_price


def _checkout_item(item_code: str, item_price: float, item_count: int) -> float:
    """
    A reusable function to get checkout price on items based on item code
    :param item_code: Item inventory code
    :param item_price: Item price
    :param item_count: Number of items
    :return: Final price for all items in the same group
    """
    if item_code == "A":
        # Three for two offer
        return _group_offer_price(3, item_price * 2, item_count, item_price)
    if item_code == "B":
        # Note here uses the offer Three for £100 not £1
        return _group_offer_price(3, 100, item_count, item_price)
    return item_price * item_count
