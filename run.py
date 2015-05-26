from eve import Eve
from eve.auth import BasicAuth


class RolesAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        accounts = app.data.driver.db['users']
        lookup = {'username': username, 'password': password}
        if allowed_roles:
            # only retrieve a user if his roles match ``allowed_roles``
            lookup['roles'] = {'$in': allowed_roles}

        account = accounts.find_one(lookup)

        return account


if __name__ == '__main__':
	app = Eve(auth=RolesAuth)
	app.run()
