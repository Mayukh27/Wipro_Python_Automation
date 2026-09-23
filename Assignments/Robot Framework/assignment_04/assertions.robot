*** Settings ***
Library    SeleniumLibrary
Library    RequestsLibrary
Library    Collections

*** Variables ***
${SITE_URL}    https://automationexercise.com
${BROWSER}    Chrome

*** Test Cases ***
Page Title Assertion Reflects Actual Page
    Open Browser    ${SITE_URL}    ${BROWSER}
    ${actual_title}=    Get Title
    Should Be Equal As Strings    ${actual_title}    Automation Exercise
    [Teardown]    Close Browser

Products API Returns Expected Structure
    Create Session    ae    ${SITE_URL}
    ${response}=    GET On Session    ae    /api/productsList    expected_status=200
    ${payload}=    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${payload}    products
    @{products}=    Get From Dictionary    ${payload}    products
    Should Not Be Empty    ${products}
    ${first_product}=    Set Variable    ${products}[0]
    Dictionary Should Contain Key    ${first_product}    id
    Dictionary Should Contain Key    ${first_product}    name
