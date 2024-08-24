# ROSHAN RAJ
# 90439894
# roshar1@uci.edu

# test_ds_messenger.py

from ds_messenger import DirectMessenger


def test_send_message():
    messenger = DirectMessenger(dsuserver="168.235.86.101", username="ani", password="lol")

    assert messenger.send("Hello!", "deltacohater")


def test_retrieve_new_messages():
    messenger = DirectMessenger(dsuserver="168.235.86.101", username="deltacohater", password="tacobell")

    new_messages = messenger.retrieve_new()
    assert isinstance(new_messages, list)


def test_retrieve_all_messages():
    messenger = DirectMessenger(dsuserver="168.235.86.101", username="ani", password="lol")

    all_messages = messenger.retrieve_all()
    assert isinstance(all_messages, list)


if __name__ == "__main__":
    test_send_message()
    test_retrieve_new_messages()
    test_retrieve_all_messages()
    print("All tests passed successfully!")
