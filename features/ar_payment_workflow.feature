Feature: AR Payment
  As a G2 user I want to process AR payments for customers

  Background:
    Given G2 is running and the Navigator is open


  Scenario: Pay invoice for customer 4268
    When I navigate to "Take AR Payments" from the "Parts" menu
    Then the "Accounts Receivable" window opens

    When I enter customer number "4268"
    Then the invoice table loads

    When I sort the invoice table by "Balance" descending
    And I select the first invoice
    And I set the pay amount to "100"
    And I accept the payment

    Then the "Take Payment" window opens
    When I choose "Credit" as the payment method

    Then the "IDSPay" window opens
    When I click the "SAVED CARDS" tab
    And I click "PROCESS PAYMENT"
