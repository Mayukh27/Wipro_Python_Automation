Feature: Data-driven login on Automation Exercise

  Scenario Outline: Login attempt with various invalid credentials
    Given the user is on the Automation Exercise login page
    When the user logs in with email "<email>" and password "<password>"
    Then the user should see an incorrect credentials error

    Examples:
      | email                       | password     |
      | outline.user1@example.com   | WrongPass!11 |
      | outline.user2@example.com   | WrongPass!12 |
      | outline.user3@example.com   | WrongPass!13 |

  Scenario: Login attempts driven entirely by external JSON test data
    Given the user is on the Automation Exercise login page
    When the user attempts login using each combination in "login_data.json"
    Then every attempt should be rejected with an incorrect credentials error
