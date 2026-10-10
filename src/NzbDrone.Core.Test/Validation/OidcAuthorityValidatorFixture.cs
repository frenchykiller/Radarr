using System.Net.Http;
using Moq;
using NUnit.Framework;
using FluentAssertions;
using NzbDrone.Core.Test.Framework;
using NzbDrone.Core.Validation;
using NzbDrone.Core.Authentication;

namespace NzbDrone.Core.Test.Validation
{
    [TestFixture]
    public class OidcAuthorityValidatorFixture : CoreTest<OidcAuthorityValidator>
    {
        [SetUp]
        public void Setup()
        {
            Mocker.GetMock<IOidcDiscoveryService>()
                  .Setup(s => s.GetOidcConfiguration(It.IsAny<string>()))
                  .Returns(new OidcConfiguration());
        }

        [Test]
        public void should_be_valid_when_authority_is_valid()
        {
            Subject.IsValid("https://example.com").Should().BeTrue();
        }

        [Test]
        public void should_be_invalid_when_authority_is_invalid()
        {
            Mocker.GetMock<IOidcDiscoveryService>()
                  .Setup(s => s.GetOidcConfiguration(It.IsAny<string>()))
                  .Throws(new HttpRequestException());

            Subject.IsValid("https://example.com").Should().BeFalse();
        }
    }
}
