# This file is a part of the AnyBlok / Marshmallow project
#
#    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from . import CustomerSchema


class TestComplexeSchema:

    @pytest.fixture(autouse=True)
    def transact(self, request, registry_complexe_model):
        transaction = registry_complexe_model.begin_nested()
        request.addfinalizer(transaction.rollback)

    def test_dump_complexe_schema(self, registry_complexe_model):
        registry = registry_complexe_model
        customer_schema = CustomerSchema(context={'registry': registry})
        tag = registry.Tag.insert(name="tag 1")
        customer = registry.Customer.insert(name="C1")
        customer.tags.append(tag)
        city = registry.City.insert(name="Rouen", zipcode="76000")
        address = registry.Address.insert(
            customer=customer, city=city, street="Somewhere")
        data = customer_schema.dump(customer)
        assert (
            data ==
            {
                'id': customer.id,
                'name': customer.name,
                'addresses': [
                    {
                        'id': address.id,
                        'street': address.street,
                        'city': {
                            'id': city.id,
                            'name': city.name,
                            'zipcode': city.zipcode,
                        },
                    },
                ],
                'tags': [
                    {
                        'id': tag.id,
                        'name': tag.name,
                    },
                ],
            }
        )

    def test_load_complexe_schema(self, registry_complexe_model):
        registry = registry_complexe_model
        dump_data = {
            'id': 1,
            'name': 'name',
            'addresses': [
                {
                    'id': 2,
                    'street': 'street',
                    'city': {
                        'id': 3,
                        'name': 'name',
                        'zipcode': 'zipcode',
                    },
                },
            ],
            'tags': [
                {
                    'id': 4,
                    'name': 'name',
                },
            ],
        }
        customer_schema = CustomerSchema(context={'registry': registry})
        data = customer_schema.load(dump_data)
        assert data == dump_data

    def test_validate_complexe_schema(self, registry_complexe_model):
        registry = registry_complexe_model
        dump_data = {
            'id': 1,
            'name': 'name',
            'addresses': [
                {
                    'id': 2,
                    'street': 'street',
                    'city': {
                        'id': 3,
                        'name': 'name',
                        'zipcode': 'zipcode',
                    },
                },
            ],
            'tags': [
                {
                    'id': 4,
                    'name': 'name',
                },
            ],
        }
        customer_schema = CustomerSchema(context={'registry': registry})
        errors = customer_schema.validate(dump_data)
        assert not errors
