### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta
from botocore.vendored import requests

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")


def risk(risk_level):
    """
    Defines each risk level
    """
    if risk_level == "None":
        recommend = "100% bonds (AGG), 0% equities (SPY)"
    elif risk_level == "Very Low":
        recommend = "80% bonds (AGG), 20% equities (SPY)"
    elif risk_level == "Low":
        recommend = "60% bonds (AGG), 40% equities (SPY)"
    elif risk_level == "Medium":
        recommend = "40% bonds (AGG), 60% equities (SPY)"
    elif risk_level == "High":
        recommend = "20% bonds (AGG), 80% equities (SPY)"
    else:
        recommend = "0% bonds (AGG), 100% equities (SPY)"

    return recommend


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


def validate_data(age, investment_amount, intent_request):
    """
    Validates the data provided by the user.
    """
    # Validate that the user is over 0 years old
    if age is not None:
        age = parse_int(age)
        
        if age<=0 or age>65:
            return build_validation_result(
                                False,
                                "age",
                                "You should be greater than 0 years and less than 65 to use this service,"
                                "Please provide proper details"
                                )
    
    # Validate the investment amount, it should be > 0
    if investment_amount is not None:
        investment_amount = parse_int(investment_amount)
            
    # Since parameters are strings it's important to cast values    
    
        if investment_amount<5000:
            return build_validation_result(
                False,
                "totalStocksBonds",
                "You should invest more than $5000 to use this service,"
                "Please provide another amount"
                )
            
    # A True results is returned if age or amount are valid
    return build_validation_result(True, None, None)

### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response

### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    retirement_age = get_slots(intent_request)["retirementAge"]
    savings = get_slots(intent_request)["savings"]
    portfolio_type = get_slots(intent_request)["portfolioType"]
    total_stocks_bonds = get_slots(intent_request)["totalStocksBonds"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Gets all the slots
        slots = get_slots(intent_request)

        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.
        
        validation_result = validate_data(age, total_stocks_bonds, intent_request)
        
        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation
    
    age_of_death = int(80)
    retirement_years = int(age_of_death - parse_int(retirement_age))
    years_to_retirement = int(parse_int(retirement_age) - parse_int(age))
    
    # input = retirement_years, years_to_retirement, savings, portfolio_type, total_stocks_bonds

    initial_recommendation = 'test rec'
   

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{}, based on the information you provided, please choose an investment portfolio with {}
            """.format(
                first_name, initial_recommendation
            ),
        },
    )


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "recommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)