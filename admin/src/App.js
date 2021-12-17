import * as React from 'react';
import { Admin, Resource, ListGuesser } from 'react-admin';
import jsonServerProvider from 'ra-data-json-server';

const dataProvider = jsonServerProvider(
  'http://127.0.0.1:8080/admin/resources',
);

const App = () => (
  <Admin dataProvider={dataProvider}>
    <Resource name="users" list={ListGuesser} />
    <Resource name="companies" list={ListGuesser} />
    <Resource name="companies_m2m_contractors" list={ListGuesser} />
    <Resource name="companies_m2m_employers" list={ListGuesser} />
    <Resource name="invite_users_to_companies" list={ListGuesser} />
    <Resource name="recipient_bank_accounts" list={ListGuesser} />
    <Resource name="sender_bank_accounts" list={ListGuesser} />
    <Resource name="invoices" list={ListGuesser} />
    <Resource name="operations" list={ListGuesser} />
  </Admin>
);

export default App;
