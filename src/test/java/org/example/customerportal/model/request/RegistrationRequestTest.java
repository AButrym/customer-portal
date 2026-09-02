package org.example.customerportal.model.request;

import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Guards RC-1 / REJECT-3: the {@code RegistrationRequest} record must not render
 * the submitted plaintext password through {@code toString()} (SC-1 / SEC-3), the
 * way the compiler-generated record {@code toString()} would.
 */
class RegistrationRequestTest {

    private static final String SECRET = "Aa1!s3cr3t-plaintext";

    @Test
    void toStringNeverRendersTheSubmittedPlaintextPassword() {
        RegistrationRequest request = new RegistrationRequest("alice@example.com", SECRET);

        String rendered = request.toString();

        assertThat(rendered)
                .doesNotContain(SECRET)
                .contains("alice@example.com")
                .contains("password=***");
    }

    @Test
    void toStringRenderIsIndependentOfThePasswordValueAndDoesNotThrowOnNull() {
        assertThat(new RegistrationRequest("bob@example.com", null).toString())
                .contains("bob@example.com")
                .contains("password=***");
        assertThat(new RegistrationRequest("bob@example.com", "Different!Value9").toString())
                .isEqualTo(new RegistrationRequest("bob@example.com", SECRET).toString());
    }

    @Test
    void passwordAccessorStillReturnsTheRealValue() {
        assertThat(new RegistrationRequest("carol@example.com", SECRET).password()).isEqualTo(SECRET);
    }
}
