import React from 'react';
import { render } from 'enzyme';
import OidcAuthenticationSettings from './OidcAuthenticationSettings';

describe('OidcAuthenticationSettings', () => {
  it('should render without crashing', () => {
    const wrapper = render(
      <OidcAuthenticationSettings
        oidcAuthority={{ value: '' }}
        oidcClientId={{ value: '' }}
        oidcClientSecret={{ value: '' }}
        oidcUserIdentifier={{ value: '' }}
        oidcScopes={{ value: '' }}
        onInputChange={() => {}}
      />
    );
    expect(wrapper).toBeTruthy();
  });
});
