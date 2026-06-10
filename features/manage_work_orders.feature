Feature: Manage Work Orders
  As a G2 service technician I want to open the Work Orders screen
  so that I can create and manage work orders for customers

  Background:
    Given G2 is running and the Navigator is open

  @smoke
  Scenario: Open Work Orders screen from the Service menu
    When I navigate to "Work Orders" from the Service menu
    Then the "Astra G2 - Service Manager" window is open and visible

  @smoke
  Scenario: Filter work orders to show open WOs
    Given the "Astra G2 - Service Manager" window is open and visible
    When I check the "Open WO's" filter
    And I apply the work order filter
    Then the work order list is displayed
    And the "Completed Within" checkbox is unchecked
