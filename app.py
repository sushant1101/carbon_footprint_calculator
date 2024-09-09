from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask.views import MethodView
import pandas as pd

app = Flask(__name__, static_url_path='/static')


# Helper function for CO2 calculation
def cal(activity_type, subtype, unit, activity_data):
    """
    Calculate the carbon footprint based on user input.

    Args:
        activity_type (str): The type of activity (e.g., 'transportation', 'energy').
        subtype (str): The subtype of the activity (e.g., 'Car', 'Electricity').
        unit (str): The unit of measurement (e.g., 'gallon', 'kWh').
        activity_data (float): The activity data (e.g., distance traveled, energy used).

    Returns:
        float: The calculated carbon footprint.

    Raises:
        ValueError: If the subtype is not found in the dataset or if conversion rate is zero.
        FileNotFoundError: If the dataset file is not found.
        Exception: For any other unexpected errors.
    """
    try:
        # Load the dataset
        df = pd.read_excel('CO2_Emission_Dataset.xlsx')

        # Filter data based on subtype
        filtered_df = df[df['SubType'] == subtype]
        if filtered_df.empty:
            raise ValueError(f"Subtype '{subtype}' not found in the dataset.")

        co2 = filtered_df['CO2'].iloc[0]
        conv_rate = filtered_df['conv_rate'].iloc[0]

        if conv_rate == 0:
            raise ValueError("Conversion rate cannot be zero.")

        # Calculate the carbon footprint
        carbon_footprint = (float(activity_data) / float(conv_rate)) * float(co2)
        # print(f"Carbon footprint: {carbon_footprint}")

        return carbon_footprint

    except FileNotFoundError:
        print("CO2 emission dataset file not found.")
        raise
    except ValueError as ve:
        print(f"Value error during CO2 calculation: {ve}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during CO2 calculation: {e}")
        raise


# Home page route
@app.route('/')
def cal_page():
    """
    Route for the homepage, which renders the main form.
    """
    return render_template('index_.html')


# Class-based view for individual form submission
class IndividualFormAPI(MethodView):
    """
    API for handling individual form submission.
    """

    def post(self):
        """
        Handles POST requests to submit the individual form.

        Returns:
            JSON response indicating success or error message.
        """
        try:
            user_type = 'Individual'
            name = request.form.get('name')
            email = request.form.get('email')
            no_of_mem = request.form.get('no_of_user')
            country = request.form.get('country')
            # cal_by = request.form.get('cal_by')
            print(name, email, no_of_mem, country)
            # Validate required fields
            if not all([name, email, no_of_mem, country]):
                return jsonify({'error': 'All fields are required.'}), 400

            # Process the data as needed (e.g., save to database)
            # ...

            response = {'message': "Individual submission successful"}
            return jsonify(response), 200

        except Exception as e:
            print(f"Error in IndividualFormAPI: {e}")
            return jsonify({'error': 'An error occurred while processing your request.'}), 500


# Class-based view for company form submission
class CompanyFormAPI(MethodView):
    """
    API for handling company form submission.
    """

    def post(self):
        """
        Handles POST requests to submit the company form.

        Returns:
            JSON response indicating success or error message.
        """
        try:
            user_type = 'Company'
            name = request.form.get('name')
            email = request.form.get('email')
            no_of_mem = request.form.get('no_of_mem')
            country = request.form.get('country')
            cal_by = request.form.get('cal_by')

            # Validate required fields
            if not all([name, email, no_of_mem, country, cal_by]):
                return jsonify({'error': 'All fields are required.'}), 400

            # Process the data as needed (e.g., save to database)
            # ...

            response = {'message': "Company submission successful"}
            return jsonify(response), 200

        except Exception as e:
            print(f"Error in CompanyFormAPI: {e}")
            return jsonify({'error': 'An error occurred while processing your request.'}), 500


# Class-based view for transportation form submission
class TransportationAPI(MethodView):
    """
    API for handling transportation form submission.
    """

    def post(self):
        """
        Handles POST requests to calculate CO2 emissions for transportation.

        Returns:
            JSON response with calculated CO2 emissions or error message.
        """
        try:
            psmiles = request.form.get('psmiles')
            pstypes = request.form.get('pstype')
            pbmiles = request.form.get('pbmiles')
            pbtypes = request.form.get('pbtype')

            # Validate required fields
            if not all([psmiles, pstypes, pbmiles, pbtypes]):
                return jsonify({'error': 'All transportation fields are required.'}), 400

            # Calculate CO2 for transportation types
            data_ps = cal('transportation', pstypes, 'gallon', psmiles)
            data_pb = cal('transportation', pbtypes, 'gallon', pbmiles)

            response_ = {'message': [data_ps, data_pb]}
            return jsonify(response_), 200

        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400
        except FileNotFoundError:
            return jsonify({'error': 'CO2 emission dataset file not found.'}), 500
        except Exception as e:
            print(f"Error in TransportationAPI: {e}")
            return jsonify({'error': 'An unexpected error occurred.'}), 500


# Class-based view for energy form submission
class EnergyAPI(MethodView):
    """
    API for handling energy form submission.
    """

    def post(self):
        """
        Handles POST requests to calculate CO2 emissions for energy usage.

        Returns:
            JSON response with calculated CO2 emissions or error message.
        """
        try:
            kwatt = request.form.get('kwatt')
            energytype = request.form.get('energytype')

            # Validate required fields
            if not all([kwatt, energytype]):
                return jsonify({'error': 'All energy fields are required.'}), 400

            # Calculate CO2 for energy usage
            data_energy = cal('Electricity', energytype, 'kWh', kwatt)

            response = {'message': [data_energy]}
            return jsonify(response), 200

        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400
        except FileNotFoundError:
            return jsonify({'error': 'CO2 emission dataset file not found.'}), 500
        except Exception as e:
            print(f"Error in EnergyAPI: {e}")
            return jsonify({'error': 'An unexpected error occurred.'}), 500


# Class-based view for waste form submission
class WasteAPI(MethodView):
    """
    API for handling waste form submission.
    """

    def post(self):
        """
        Handles POST requests to calculate CO2 emissions for waste disposal.

        Returns:
            JSON response with calculated CO2 emissions or error message.
        """
        try:
            landfill = request.form.get('landfill')
            incineration = request.form.get('incineration')
            recycling = request.form.get('recycling')

            # Validate required fields
            if not all([landfill, incineration, recycling]):
                return jsonify({'error': 'All waste fields are required.'}), 400

            # Calculate CO2 for waste management
            data_landfill = cal('Waste', 'Landfill', 'kg', landfill)
            data_incineration = cal('Waste', 'Incineration', 'kg', incineration)
            data_recycling = cal('Waste', 'Recycling', 'kg', recycling)

            response = {'message': [data_landfill, data_incineration, data_recycling]}
            return jsonify(response), 200

        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400
        except FileNotFoundError:
            return jsonify({'error': 'CO2 emission dataset file not found.'}), 500
        except Exception as e:
            print(f"Error in WasteAPI: {e}")
            return jsonify({'error': 'An unexpected error occurred.'}), 500


# Class-based view for food form submission
class FoodAPI(MethodView):
    """
    API for handling food consumption form submission.
    """

    def post(self):
        """
        Handles POST requests to calculate CO2 emissions for food consumption.

        Returns:
            JSON response with calculated CO2 emissions or error message.
        """
        try:
            meat = request.form.get('meat')
            dairy = request.form.get('dairy')
            small_fish = request.form.get('small_fish')
            large_fish = request.form.get('large_fish')
            fandv = request.form.get('fandv')
            bread = request.form.get('bread')
            snack = request.form.get('snack')

            # Validate required fields
            if not all([meat, dairy, small_fish, large_fish, fandv, bread, snack]):
                return jsonify({'error': 'All food fields are required.'}), 400

            # Calculate CO2 for food consumption
            data_meat = cal('Food', 'Meat', 'kg', meat)
            data_dairy = cal('Food', 'Dairy', 'kg', dairy)
            data_small_fish = cal('Food', 'Small Fish', 'kg', small_fish)
            data_large_fish = cal('Food', 'Large Fish', 'kg', large_fish)
            data_vandg = cal('Food', 'Fruits & Vegetables', 'kg', fandv)
            data_bread = cal('Food', 'Bread', 'kg', bread)
            data_snack = cal('Food', 'Snacks and Beverage', 'kg', snack)

            response = {
                'message': [
                    data_meat,
                    data_dairy,
                    data_small_fish,
                    data_large_fish,
                    data_vandg,
                    data_bread,
                    data_snack
                ]
            }
            return jsonify(response), 200

        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400
        except FileNotFoundError:
            return jsonify({'error': 'CO2 emission dataset file not found.'}), 500
        except Exception as e:
            print(f"Error in FoodAPI: {e}")
            return jsonify({'error': 'An unexpected error occurred.'}), 500


# Registering routes with class-based views
app.add_url_rule('/indform', view_func=IndividualFormAPI.as_view('individual_form_api'))
app.add_url_rule('/cmpyform', view_func=CompanyFormAPI.as_view('company_form_api'))
app.add_url_rule('/transportation', view_func=TransportationAPI.as_view('transportation_api'))
app.add_url_rule('/energy', view_func=EnergyAPI.as_view('energy_api'))
app.add_url_rule('/waste', view_func=WasteAPI.as_view('waste_api'))
app.add_url_rule('/food', view_func=FoodAPI.as_view('food_api'))



# Generic form submission route (used in test form)
@app.route('/submit', methods=['POST'])
def submit():
    """
    Handles generic form submission (for testing purposes).

    Returns:
        JSON response indicating success or error message.
    """
    try:
        name = request.form.get('name')
        email = request.form.get('email')

        # Validate required fields
        if not all([name, email]):
            return jsonify({'error': 'Name and email are required.'}), 400

        print(f"Name: {name}")
        print(f"Email: {email}")

        # Process the data as needed (e.g., save to database)
        # ...

        response = {'message': 'Form submitted successfully'}
        return jsonify(message=response), 200

    except Exception as e:
        print(f"Error in /submit route: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500


# Another generic form submission route
@app.route('/submit123', methods=['POST'])
def submit123():
    """
    Handles another generic form submission.

    Returns:
        JSON response indicating success or error message.
    """
    try:
        name = request.form.get('name123')
        email = request.form.get('email123')

        # Validate required fields
        if not all([name, email]):
            return jsonify({'error': 'Name and email are required.'}), 400

        print(f"Name123: {name}")
        print(f"Email123: {email}")

        # Process the data as needed (e.g., save to database)
        # ...

        response = {'message': 'Form submitted successfully'}
        return jsonify(message=response), 200

    except Exception as e:
        print(f"Error in /submit123 route: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500


# Custom error handlers
@app.errorhandler(400)
def bad_request(error):
    """
    Handler for 400 Bad Request errors.
    """
    return jsonify({'error': 'Bad Request'}), 400


@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 Not Found errors.
    """
    return jsonify({'error': 'Resource Not Found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handler for 500 Internal Server errors.
    """
    return jsonify({'error': 'Internal Server Error'}), 500


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

