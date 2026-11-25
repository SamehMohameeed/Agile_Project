Feature: Add a Course (SCRUM-57)
  As a student
  I want to add a Course
  So that I can organize its Assignments and Exams under the correct subject

  Background:
    Given a logged-in student

  Scenario: Successfully add a new course
    When the student adds the course "SET312" named "Agile Software Engineering"
    Then "SET312" appears in the student's registered courses
    And the student has 1 registered course

  Scenario: Refuse adding a duplicate course
    Given the student already has the course "SET312" named "Agile Software Engineering"
    When the student adds the course "SET312" named "Agile Software Engineering"
    Then the action is refused with "Course already exists"
    And the student has 1 registered course

  Scenario Outline: Check different course additions
    Given the student already has the course "SET312" named "Agile Software Engineering"
    When the student adds the course "<code>" named "<name>"
    Then the result is "<result>"

    Examples:
      | code   | name                       | result   |
      | CS101  | Intro to Programming       | accepted |
      | MATH20 | Discrete Mathematics       | accepted |
      | SET312 | Software Engineering       | refused  |
      | set312 | Agile Software Engineering | refused  |
