from behave import given, then, when

from registration import RegistrationError, Student


@given('a student with ID "{sid}"')
def step_student(context, sid):
    context.student = Student(sid)
    
@when('the student registers for "{code}" worth {hours:d} hours')
def step_register(context, code, hours):
    context.error = None
    try:
        context.student.register(code, hours)
    except RegistrationError as e:
        context.error = str(e)
    
@then("the student has {hours:d} registered hours")
def step_check_hours(context, hours):
    assert context.student.total_hours == hours
    
@given("the student already has {hours:d} registered hours")
def step_existing_hours(context, hours):
    if hours:
        context.student.register("FILLER", hours)
        
@then('the registration is refused with "{text}"')
def step_refused(context, text):
    assert context.error is not None
    assert text in context.error
    
    
@given('the student is registered for "{code}" worth {hours:d} hours')
def step_course_registered(context, code, hours):
    context.student.register(code, hours)

@then('the result is "{result}"')
def step_result(context, result):
    if result == "accepted":
        assert context.error is None
    else:
        assert context.error is not None
        
        
@when('the student drops "{code}"')
def step_drop(context, code):
    context.student.drop(code)

