using Moq;
using NUnit.Framework;
using FluentAssertions;
using NzbDrone.Core.Test.Framework;
using NzbDrone.Core.HealthCheck;
using NzbDrone.Core.HealthCheck.Checks;
using NzbDrone.Core.Configuration;
using NzbDrone.Core.Authentication;

namespace NzbDrone.Core.Test.HealthCheck
{
    [TestFixture]
    public class OidcConfigurationCheckFixture : CoreTest<OidcConfigurationCheck>
    {
        [Test]
        public void should_return_ok_when_not_oidc()
        {
            Mocker.GetMock<IConfigFileProvider>()
                  .Setup(s => s.AuthenticationMethod)
                  .Returns(AuthenticationType.Forms);

            Subject.Check().Type.Should().Be(HealthCheckResult.Ok().Type);
        }

        [Test]
        public void should_return_error_when_oidc_not_configured()
        {
            Mocker.GetMock<IConfigFileProvider>()
                  .Setup(s => s.AuthenticationMethod)
                  .Returns(AuthenticationType.Oidc);
                  
            Mocker.GetMock<IConfigFileProvider>()
                  .Setup(s => s.OidcAuthority)
                  .Returns("");

            Subject.Check().Reason.Should().Be(HealthCheckReason.OidcNotConfigured);
        }
    }
}
