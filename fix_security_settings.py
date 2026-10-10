import re

with open("frontend/src/Settings/General/SecuritySettings.js", "r") as f:
    content = f.read()

# Add import AuthenticationMethodSettings
content = content.replace("import translate from 'Utilities/String/translate';", "import translate from 'Utilities/String/translate';\nimport AuthenticationMethodSettings from './AuthenticationMethodSettings';")

# Add Oidc to authenticationMethodOptions
oidc_option = """  {
    key: 'oidc',
    get value() {
      return translate('Oidc');
    }
  },"""
content = content.replace("  {\n    key: 'basic',", oidc_option + "\n  {\n    key: 'basic',")

# Extract properties from settings
new_props = """      passwordConfirmation,
      oidcAuthority,
      oidcClientId,
      oidcClientSecret,
      oidcUserIdentifier,
      oidcScopes,"""
content = content.replace("      passwordConfirmation,", new_props)

# Replace the three form groups (Username, Password, PasswordConfirmation) with AuthenticationMethodSettings
replace_pattern = r'\{[\s\n]*authenticationEnabled \?[\s\n]*<FormGroup>[\s\n]*<FormLabel>\{translate\(\'Username\'\)\}</FormLabel>.*?null[\s\n]*\}'
replacement = """      <AuthenticationMethodSettings
        authenticationMethod={authenticationMethod}
        username={username}
        password={password}
        passwordConfirmation={passwordConfirmation}
        oidcAuthority={oidcAuthority}
        oidcClientId={oidcClientId}
        oidcClientSecret={oidcClientSecret}
        oidcUserIdentifier={oidcUserIdentifier}
        oidcScopes={oidcScopes}
        showValidationWarnings={true}
        onInputChange={onInputChange}
      />"""

content = re.sub(r'\{[\s]*authenticationEnabled \?[\s]*<FormGroup>[\s]*<FormLabel>\{translate\(\'Username\'\)\}</FormLabel>.*?null[\s]*\}[\s]*\{[\s]*authenticationEnabled \?[\s]*<FormGroup>[\s]*<FormLabel>\{translate\(\'Password\'\)\}</FormLabel>.*?null[\s]*\}[\s]*\{[\s]*authenticationEnabled \?[\s]*<FormGroup>[\s]*<FormLabel>\{translate\(\'PasswordConfirmation\'\)\}</FormLabel>.*?null[\s]*\}', replacement, content, flags=re.DOTALL)

with open("frontend/src/Settings/General/SecuritySettings.js", "w") as f:
    f.write(content)
