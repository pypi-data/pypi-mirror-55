import zeep
from zeep import Client
from zeep.helpers import serialize_object


class PlanningNl(object):
    def __init__(self, username, password):
        """
        This package is meant to get from or push data to planning.nl. An timeschedule tool. The requests are all made with soap.
        See for documentation of the SOAP API the following link: https://wiki.visibox.nl/display/VIS/Algemene+informatie
        :param username: The username for planning.nl
        :param password: The corresponding password
        """
        client = Client('https://api.visibox.nl/v1/authentication?wsdl')
        request_body = {'username': username, 'password': password}
        response = client.service.login(request_body)
        self.token = response['authenticationToken']

    def get_human_resources(self, employee_id=None):
        """
        Get all the employees with their basic information (like personal details).
        :param employee_id: An optional filter to receive data from only 1 employee
        :return: the data returned from the SOAP request
        """
        # Determine the client for the resources
        client = Client('https://api.visibox.nl/v1/resource?wsdl')
        # Get all the employee resources without filters
        if employee_id == None:
            request_body = {
                'authentication': {
                    'token': self.token
                },
                'humanResource': {
                    'resourceClass': 'PERSONNEL',
                    'humanResourceMatcher': {
                        'allowMultiple': 'true'
                    }
                }
            }
        else:
            request_body = {
                'authentication': {
                    'token': self.token
                },
                'humanResource': {
                    'resourceClass': 'PERSONNEL',
                    'humanResourceMatcher': {
                        'allowMultiple': 'true',
                        'number': employee_id
                    }
                }
            }
        response = client.service.getHumanResources(**request_body)['matcherResults']['matcherResult'][0]['entities']['entity']
        data = serialize_object(response)
        return data

    def get_departments(self):
        """
        Get all the departments from planning.nl. Only the departments, no employees etc.
        :return: the data returned from the SOAP request
        """
        client = Client('https://api.visibox.nl/v1/department?wsdl')
        request_body = {
            'authentication': {
                'token': self.token
            },
            'departmentMatcher': {
                'allowMultiple': 'true'
            }
        }
        response = client.service.getDepartments(**request_body)['matcherResults']['matcherResult'][0]['entities']['entity']
        data = serialize_object(response)
        return data

    def get_human_departments(self):
        """
        Get the ID's of employees with their departments
        :return: the data returned from the SOAP request
        """
        client = Client('https://api.visibox.nl/v1/resource?wsdl')
        request_body = {
            'authentication': {
                'token': self.token
            },
            'resourceDepartment': {
                'resourceClass': 'PERSONNEL',
                'resourceDepartmentMatcher': {
                    'allowMultiple': 'true',
                    'humanResourceMatcher': {
                        'allowMultiple': 'true'
                    },
                    'departmentMatcher': {
                        'allowMultiple': 'true'
                    }
                }
            }
        }
        response = client.service.getResourceDepartments(**request_body)['matcherResults']['matcherResult'][0]['entities']['entity']
        data = serialize_object(response)
        return data

    def push_human_recources(self):
        client = Client('https://api.visibox.nl/v1/resource?wsdl')

    def logout(self):
        client = Client('https://api.visibox.nl/v1/authentication?wsdl')
        # Logout so that the token is destroyed. The logoutRequest key is mandatory but because there is no available value set a zeep.xsd.SkipValue
        request_body = {
            'authentication': {
                'token': self.token
            },
            'logoutRequest': zeep.xsd.SkipValue
        }
        response = client.service.logout(**request_body)
        return response