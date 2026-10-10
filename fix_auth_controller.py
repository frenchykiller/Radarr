import re

with open("src/Radarr.Http/Authentication/AuthenticationController.cs", "r") as f:
    content = f.read()

# Add using Microsoft.AspNetCore.Authentication.Cookies;
if "using Microsoft.AspNetCore.Authentication.Cookies;" not in content:
    content = content.replace("using Microsoft.AspNetCore.Authentication;", "using Microsoft.AspNetCore.Authentication;\nusing Microsoft.AspNetCore.Authentication.Cookies;")

# Add LoginSso
login_sso = """
        [HttpGet("login/sso")]
        public IActionResult LoginSso([FromQuery] string returnUrl = null)
        {
            if (_configFileProvider.AuthenticationMethod != AuthenticationType.Oidc)
            {
                return Redirect(_configFileProvider.UrlBase + "/login");
            }

            if (!_configFileProvider.IsOidcConfigured())
            {
                _logger.Error("OIDC authentication is enabled, but Authority, Client ID, Client Secret, User and Scopes are not all configured");

                return Redirect(_configFileProvider.UrlBase + "/login");
            }

            return Challenge(
                new AuthenticationProperties { RedirectUri = GetRedirectUrl(returnUrl) },
                new[] { nameof(AuthenticationType.Oidc) });
        }
"""
content = content.replace('[HttpPost("login")]', login_sso.strip() + '\n\n        [HttpPost("login")]')

# Fix Login return url logic
login_redirect_fix = """            return Redirect(GetRedirectUrl(returnUrl));
        }"""
content = re.sub(r'if \(returnUrl\.IsNullOrWhiteSpace\(\).*?return Redirect\(_configFileProvider\.UrlBase \+ returnUrl\);\n        }', login_redirect_fix, content, flags=re.DOTALL)

# Fix Logout
logout_fix = """
        [HttpGet("logout")]
        public async Task<IActionResult> Logout()
        {
            _authService.Logout(HttpContext);

            if (_configFileProvider.EffectiveAuthenticationMethod() == AuthenticationType.Oidc)
            {
                var loggedOutUrl = _configFileProvider.UrlBase + "/loggedout";
                var signedOut = false;

                try
                {
                    await HttpContext.SignOutAsync(nameof(AuthenticationType.Oidc), new AuthenticationProperties { RedirectUri = loggedOutUrl });

                    signedOut = true;
                }
                catch (Exception e)
                {
                    _logger.Warn(e, "Unable to sign out of the OIDC provider, signing out locally only");
                }

                await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
                await HttpContext.SignOutAsync(AuthenticationType.Forms.ToString());

                if (signedOut || Response.HasStarted)
                {
                    return new EmptyResult();
                }

                return Redirect(loggedOutUrl);
            }

            await HttpContext.SignOutAsync(AuthenticationType.Forms.ToString());
            await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);

            return Redirect(_configFileProvider.UrlBase + "/");
        }

        private string GetRedirectUrl(string returnUrl)
        {
            var urlBase = _configFileProvider.UrlBase;

            if (returnUrl.IsNullOrWhiteSpace() || !Url.IsLocalUrl(returnUrl))
            {
                return urlBase + "/";
            }

            if (urlBase.IsNullOrWhiteSpace() ||
                returnUrl.Equals(urlBase, StringComparison.OrdinalIgnoreCase) ||
                returnUrl.StartsWith(urlBase + "/", StringComparison.OrdinalIgnoreCase))
            {
                return returnUrl;
            }

            return urlBase + returnUrl;
        }
"""
content = re.sub(r'\[HttpGet\("logout"\)\].*?return Redirect\(_configFileProvider\.UrlBase \+ "/"\);\n        }', logout_fix.strip(), content, flags=re.DOTALL)

with open("src/Radarr.Http/Authentication/AuthenticationController.cs", "w") as f:
    f.write(content)
