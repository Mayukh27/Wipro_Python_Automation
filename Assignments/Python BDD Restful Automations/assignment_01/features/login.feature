Feature: Login on Automation Exercise
  As a visitor
  I want to attempt logging in
  So that I can access my account or see a clear error when credentials are wrong

  Scenario: Invalid login shows an error message
    Given the user is on the Automation Exercise login page
    When the user logs in with email "no_such_user_behave@example.com" and password "WrongPass!1"
    Then the user should see an incorrect credentials error

  Scenario: Missing account login attempt is rejected
    Given the user is on the Automation Exercise login page
    When the user logs in with email "another_missing_user@example.com" and password "AnotherWrong!2"
    Then the user should see an incorrect credentials error
