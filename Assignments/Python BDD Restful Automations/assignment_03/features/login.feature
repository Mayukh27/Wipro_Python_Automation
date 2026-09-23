Feature: Page-Object-backed login on Automation Exercise

  Scenario Outline: Invalid login attempts rejected with an error
    Given the user opens the login page
    When the user submits login credentials "<email>" and "<password>"
    Then the login page should show an incorrect credentials error

    Examples:
      | email                        | password      |
      | pom.behave.user1@example.com | WrongPass!101 |
      | pom.behave.user2@example.com | WrongPass!102 |

  Scenario: New user can register and reach the logged-in dashboard state
    Given the user opens the login page
    When the user registers a new account and completes their profile
    Then the dashboard should show the user as logged in
