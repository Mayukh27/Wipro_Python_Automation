*** Settings ***
Library    SeleniumLibrary
Suite Setup    Open Application Browser
Suite Teardown    Close Browser
Test Setup    Go To Login Page
Test Teardown    Log Out If Logged In

*** Variables ***
${SITE_URL}    https://automationexercise.com
${BROWSER}    Chrome
${EMAIL_INPUT}    css:input[data-qa='login-email']
${PASSWORD_INPUT}    css:input[data-qa='login-password']
${LOGIN_BUTTON}    css:button[data-qa='login-button']
${ERROR_MESSAGE}    css:div.login-form p
${LOGGED_IN_LINK}    xpath://a[contains(text(),'Logged in as')]
${LOGOUT_LINK}    xpath://a[contains(text(),'Logout')]

*** Test Cases ***
First Invalid Login Attempt Shows Error
    Input Text    ${EMAIL_INPUT}    setup.teardown.user1@example.com
    Input Text    ${PASSWORD_INPUT}    WrongPass!301
    Click Button    ${LOGIN_BUTTON}
    Wait Until Page Contains Element    ${ERROR_MESSAGE}
    Page Should Contain    incorrect

Second Invalid Login Attempt Also Shows Error
    Input Text    ${EMAIL_INPUT}    setup.teardown.user2@example.com
    Input Text    ${PASSWORD_INPUT}    WrongPass!302
    Click Button    ${LOGIN_BUTTON}
    Wait Until Page Contains Element    ${ERROR_MESSAGE}
    Page Should Contain    incorrect

*** Keywords ***
Open Application Browser
    Open Browser    ${SITE_URL}    ${BROWSER}

Go To Login Page
    Go To    ${SITE_URL}/login
    Wait Until Page Contains Element    ${EMAIL_INPUT}

Log Out If Logged In
    ${logged_in}=    Run Keyword And Return Status    Page Should Contain Element    ${LOGGED_IN_LINK}
    Run Keyword If    ${logged_in}    Click Element    ${LOGOUT_LINK}
