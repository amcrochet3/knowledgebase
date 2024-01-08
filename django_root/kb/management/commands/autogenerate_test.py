from importlib import import_module
import os
import sys
from django.apps import apps

from django.core.management.base import BaseCommand
from django.urls import reverse

class Command(BaseCommand):
    help = "Adds APIs to urls.py for a model"

    def add_arguments(self, parser):
         parser.add_argument('app_name', type=str)
         parser.add_argument('model_name', type=str)

    def handle(self, *__args__, **options):
        app_name = options['app_name']
        model_name = options['model_name']
        generate(app_name, model_name)

def generate(app_name, model_name):
    generate_conftest(app_name, model_name)
    generate_test(app_name, model_name)
    
def generate_conftest(app_name, model_name):
    print("Writing to conftest.py...")
    model = apps.get_model(app_name, model_name)
    verbose_name = model._meta.verbose_name
    function_name = verbose_name.replace(" ", "_").lower()

    # Complete file path
    file_path = os.path.join(os.getcwd(), f"{app_name}/tests/conftest.py")
    # Read existing content
    with open(file_path, 'r') as file:
        lines = file.readlines()
    if any(model_name in line for line in lines):
        print(f"conftest.py already modified for {app_name}.{model_name}.")
        return 1
    import_added = False
    json_added = False
    fixture_added = False
    fixture_text = f"""
@pytest.fixture
def {function_name}():
    return {model_name}.objects.create(**{function_name}_json)

"""
    with open(file_path, 'w') as file:
        for line in lines:
            if "_json" in line and not json_added:
                json_added = True
                file.write(f'{function_name}_json = {{ "name": "Test {verbose_name}"}},\n')
            if "@pytest.fixture" in line and not fixture_added:
                fixture_added = True
                file.write(fixture_text)
            file.write(line)
            if "models import" in line and not import_added:
                import_added = True
                file.write(f"    {model_name},\n")
              
    print("done")
    
    
def generate_test(app_name, model_name):
    print("Writing to test_get_apis.py...")
    model = apps.get_model(app_name, model_name)
    verbose_name = model._meta.verbose_name
    verbose_with_underscore = verbose_name.replace(" ", "_").lower()
    verbose_with_dash = verbose_name.replace(" ", "-").lower()

    # Complete file path
    file_path = os.path.join(os.getcwd(), f"{app_name}/tests/test_get_apis.py")
    # Read existing content
    with open(file_path, 'r') as file:
        lines = file.readlines()
    if any(verbose_with_underscore in line for line in lines):
        print(f"test_get_apis.py already modified for {app_name}.{model_name}.")
        return 1
    url_added = False
    test_added = False
    test_text = f"""def test_{verbose_with_underscore}({verbose_with_underscore}):
    response = client.get({verbose_with_underscore.upper()}_URL)
    assert response.json()[0]["name"] == {verbose_with_underscore}.name


"""
    with open(file_path, 'w') as file:
        for line in lines:
            if "_URL =" in line and not url_added:
                url_added = True
                file.write(f'{verbose_with_underscore.upper()}_URL = reverse("{verbose_with_dash}-list")\n')
            if "def test" in line and not test_added:
                test_added = True
                file.write(test_text)
            file.write(line)
              
    print("done")

