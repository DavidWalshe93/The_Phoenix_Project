# """
# Author:     David Walshe
# Date:       14 May 2021
# """
#
# from unittest.mock import patch, MagicMock
#
# import pytest
#
# import app.api.authentication as sut
#
#
# def test_verify_password_no_email_or_token(caplog):
#     """
#     :GIVEN: No username, token or password.
#     :WHEN:  Verifying a users credentials.
#     :THEN:  Verify the verification fails due to no email/token being supplied.
#     """
#     # Target paths of functions to mock.
#     auth_token_target = "app.api.authentication.auth_with_token"
#     auth_password_target = "app.api.authentication.auth_with_password"
#
#     with patch(auth_token_target) as mock_token:
#         with patch(auth_password_target) as mock_password:
#             assert sut._verify_password("", "") == False
#             assert caplog.messages[0] == "No email or token provided."
#
#     # Ensure the token/password verification function were not called.
#     mock_token.assert_not_called()
#     mock_password.assert_not_called()
#
#
# def test_verify_password_auth_token(caplog):
#     """
#     :GIVEN: An auth token.
#     :WHEN:  Verifying a users credentials.
#     :THEN:  Verify the token authentication procedure is called.
#     """
#     # Target paths of functions to mock.
#     auth_token_target = "app.api.authentication.auth_with_token"
#     auth_password_target = "app.api.authentication.auth_with_password"
#
#     token = "pytest_token"
#
#     with patch(auth_token_target, return_value=False) as mock_token:
#         with patch(auth_password_target, return_value=False) as mock_password:
#             assert sut._verify_password(token, "") == False
#             assert caplog.messages[0] == "Authorized with Token."
#
#     # Assert token auth was called.
#     mock_token.assert_called_once_with(token=token)
#     mock_password.assert_not_called()
#
#
# def test_verify_password_auth_password(caplog):
#     """
#     :GIVEN: An email and password.
#     :WHEN:  Verifying a users credentials.
#     :THEN:  Verify the password authentication procedure is called.
#     """
#     # Target paths of functions to mock.
#     auth_token_target = "app.api.authentication.auth_with_token"
#     auth_password_target = "app.api.authentication.auth_with_password"
#
#     email = "pytest@example.com"
#     password = "123abd"
#
#     with patch(auth_token_target, return_value=False) as mock_token:
#         with patch(auth_password_target, return_value=False) as mock_password:
#             assert sut._verify_password(email, password) == False
#             assert caplog.messages[0] == "Authorized with Email/Password."
#
#     mock_token.assert_not_called()
#     # Assert password auth was called.
#     mock_password.assert_called_once_with(email=email, password=password)
#
#
# @pytest.mark.parametrize("set_user, ret_value",
#                          [
#                              (True, True),
#                              (True, False),
#                              (False, False),
#                          ])
# def test_auth_with_password(set_user, ret_value, mock_user_class_for, target_factory, fake_user):
#     """
#     :GIVEN: An email and password.
#     :WHEN:  Authenticating a client based on their email and password.
#     :THEN:  Verify the correct output is returned
#     """
#     # Inputs
#     email = fake_user["email"]
#     password = fake_user["password"]
#
#     # Create a mock User to patch static methods on.
#     mock_user = mock_user_class_for(sut)
#
#     # Create a User to return from User.query...
#     returned_user = mock_user_class_for(sut)
#     returned_user.verify_password.return_value = ret_value
#
#     # Grab user_filter to assert call params.
#     user_filter: MagicMock = mock_user.query.filter_by
#
#     # Assign Mock return value as a Mocked User Object.
#     if set_user:
#         user_filter.return_value.first.return_value = returned_user
#     else:
#         user_filter.return_value.first.return_value = None
#
#     # Patch internal function calls.
#     with patch(target_factory(sut, "set_globals")):
#         # Test SUT
#         actual = sut.auth_with_password(email, password)
#
#     # Assert return value
#     assert actual == ret_value
#
#     # Assert all User calls were expected
#     user_filter.assert_called_once_with(email=email)
#
#     if set_user:
#         # Check if verify password was called only if user was not None.
#         returned_user.verify_password.assert_called_once_with(password=password)
