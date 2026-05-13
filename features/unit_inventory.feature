Feature: Unit Inventory
  As a G2 user I want to access unit inventory to maintain units

  Background:
    Given G2 is running and the Navigator is open

  @smoke
  Scenario: Open Maintain Units from Sales menu
    When I navigate to "Unit Inventory" from the "Sales" menu
    When I click "Maintain Units"
    Then the "Inventory - SMC - Sunset Marine" window opens
    When I enter a new stock number in the "Stock #" field
    When I click "Yes" in the "New Unit" dialog
    When I click the dropdown next to "Designation"
    When I select "N NEW" from the dropdown
