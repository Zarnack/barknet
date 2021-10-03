from dataclasses import dataclass
from pydiscourse import DiscourseClient
import config


class Controller():
    def __init__(self, url, username, api_key):
        self.client = DiscourseClient(
        url,
        api_username=username,
        api_key= api_key)
        self.category_list = []

    def set_sub_category(self, name, category_id, parent_category_id, **kwargs):
        """
        sets category to parent of another category

        name: name of category
        category_id: id of that category
        parent_category_id: id of new parent category, use "" when setting to root level
        """
        kwargs["parent_category_id"] = parent_category_id
        self.client._put(f"/categories/{category_id}.json", **kwargs)

    def get_id_by_name(self, name):
        """
        return id of category by name of that category
        """

        for category in self.category_list:
            if name == category.name:
                return category.id
        response = self.client._get(f"/site.json")["categories"]
        for dic in response:
            if dic["name"] == name:
                return dic["id"]
        raise ValueError("no Category with given name has been found")

    def create_category(self, name, color, parent=None):
        """
        create category and adds new "Category" object to list with info about that category for easy access 

        name: name of new category
        color: background color of category
        parent: name of parent category
        """
        response = self.client.create_category(name, color, parent=parent)["category"]
        self.category_list.append(Category(response["name"], response["id"], response["color"], response["text_color"]))

@dataclass
class Category():
    name: str
    id: int
    color: str
    text_color: str
        

if __name__ == "__main__": 
    """
    add user specific API credentials to config.py to use the API
    """
    controller = Controller(config.url, config.username, config.api_key)
    #create new category with given name and color
    #controller.create_category("subtestest", "12A89D")
    # get id by name
    print(controller.get_id_by_name("subtestest"))
    # set category as subcategory 
    controller.set_sub_category("testtest", 26, 27)
    
