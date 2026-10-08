contacts = []
phone_numbers = set()


def value(label):
    while True:
        result = input(label).strip()
        if result:
            return result
        print("This value is required.")


def find_contact(contact_id):
    return next((contact for contact in contacts if contact["id"] == contact_id), None)


def display(contact):
    print(f"ID: {contact['id']} | {contact['name']} | {contact['phone']} | {contact['email']} | {contact['city']} | {contact['category']}")


def add_contact():
    contact_id = value("Contact ID: ")
    if find_contact(contact_id):
        print("Contact ID already exists.")
        return
    phone = value("Phone number: ")
    if phone in phone_numbers:
        print("Phone number already exists.")
        return
    email = value("Email: ")
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        print("Invalid email address.")
        return
    contacts.append({"id": contact_id, "name": value("Name: "), "phone": phone, "email": email, "city": value("City: "), "category": value("Category: ")})
    phone_numbers.add(phone)
    print("Contact added.")


def view_contacts(items=None):
    items = contacts if items is None else items
    if not items:
        print("No matching contacts.")
        return
    for contact in items:
        display(contact)


def search_by_name():
    query = value("Name: ").lower()
    view_contacts([contact for contact in contacts if query in contact["name"].lower()])


def update_contact():
    contact = find_contact(value("Contact ID: "))
    if not contact:
        print("Contact not found.")
        return
    for field, prompt in (("name", "Name"), ("phone", "Phone"), ("email", "Email"), ("city", "City"), ("category", "Category")):
        updated = input(f"{prompt} [{contact[field]}]: ").strip()
        if not updated:
            continue
        if field == "phone" and updated != contact["phone"]:
            if updated in phone_numbers:
                print("Phone number already exists.")
                continue
            phone_numbers.remove(contact["phone"])
            phone_numbers.add(updated)
        contact[field] = updated
    print("Contact updated.")


def delete_contact():
    contact = find_contact(value("Contact ID: "))
    if not contact:
        print("Contact not found.")
        return
    contacts.remove(contact)
    phone_numbers.remove(contact["phone"])
    print("Contact deleted.")


def filter_contacts(field):
    query = value(f"{field.title()}: ").lower()
    view_contacts([contact for contact in contacts if contact[field].lower() == query])


def main():
    actions = {"1": add_contact, "2": view_contacts, "3": search_by_name, "4": update_contact, "5": delete_contact, "6": lambda: filter_contacts("city"), "7": lambda: filter_contacts("category"), "8": lambda: print(f"Contacts: {len(contacts)}")}
    while True:
        print("\n1 Add  2 View  3 Search name  4 Update  5 Delete  6 City  7 Category  8 Count  9 Exit")
        choice = input("Choice: ").strip()
        if choice == "9":
            return
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
