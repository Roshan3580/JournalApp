# ROSHAN RAJ
# roshar1@uci.edu
# 90439894

# test_ds_message_protocol.py

import unittest
import ds_protocol
import json


class TestDSMessageProtocol(unittest.TestCase):

    def test_create_direct_message(self):
        token = "user_token"
        entry = "Hello World!"
        recipient = "ohhimark"
        timestamp = "1603167689.3928561"

        expected_result = json.dumps(
            {"token": token, "directmessage": {"entry": entry, "recipient": recipient, "timestamp": timestamp}})
        result = ds_protocol.create_direct_message(token, entry, recipient, timestamp)

        self.assertEqual(result, expected_result, f"Expected: {expected_result}, Got: {result}")

    def test_request_new_direct_messages(self):
        token = "user_token"
        request_type = "new"

        expected_result = json.dumps({"token": token, "directmessage": request_type})
        result = ds_protocol.request_direct_messages(token, request_type)

        self.assertEqual(result, expected_result, f"Expected: {expected_result}, Got: {result}")

    def test_request_all_direct_messages(self):
        token = "user_token"
        request_type = "all"

        expected_result = json.dumps({"token": token, "directmessage": request_type})
        result = ds_protocol.request_direct_messages(token, request_type)

        self.assertEqual(result, expected_result, f"Expected: {expected_result}, Got: {result}")

    def test_process_direct_message_response(self):
        response_new_messages = '{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'
        result_new_messages = ds_protocol.process_direct_message_response(response_new_messages)

        self.assertIsInstance(result_new_messages, list, f"Expected a list, Got: {result_new_messages}")

        response_ok = '{"response": {"type": "ok", "message": "Direct message sent"}}'
        result_ok = ds_protocol.process_direct_message_response(response_ok)

        self.assertIsInstance(result_ok, str, f"Expected a string, Got: {result_ok}")

        response_error = '{"response": {"type": "error", "message": "Invalid recipient"}}'
        result_error = ds_protocol.process_direct_message_response(response_error)

        self.assertIsInstance(result_error, str, f"Expected a string, Got: {result_error}")


if __name__ == "__main__":
    unittest.main()
