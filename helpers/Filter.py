from helpers.Contact import Contact

def filter_by_prefix(prefix: str, persons_list: list):
    prefix = prefix.lower()
    return list(filter(lambda person: ((prefix in person.name.lower())|
                                       (prefix in person.surname.lower())|
                                       (prefix in person.phone.lower())), persons_list))


if __name__ == "__main__":
    test_persons_list = [Contact("klic", "v sili", "112"),
                         Contact("Klemen", "Klemen", "424242")]

    assert len(filter_by_prefix("3", test_persons_list)) == 0
    assert len(filter_by_prefix("kli", test_persons_list)) == 1
    assert len(filter_by_prefix("kl", test_persons_list)) == 2

    for filtered_person in filter_by_prefix("Kl", test_persons_list):
        print(filtered_person.to_string())
