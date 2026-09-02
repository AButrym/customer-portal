package org.example.customerportal.model.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import org.example.customerportal.validation.ValidPassword;

/**
 * Inbound body of {@code POST /api/v1/customers}
 * ({@code docs/designs/api/US-001-openapi.yaml} {@code RegistrationRequest}).
 *
 * <p>{@code email}: required, well-formed, max 254 characters (OD-001:A).
 * {@code password}: required and policy-compliant ({@link ValidPassword}).
 * Unknown / extra JSON properties are rejected with {@code 400} via
 * {@code spring.jackson.deserialization.fail-on-unknown-properties} (PD-1) — the
 * DTO needs no {@code @JsonIgnoreProperties}.
 *
 * <p>{@link #toString()} is overridden to mask {@code password} (SC-1 / SEC-3),
 * mirroring {@code model/entity/Customer#toString()} which excludes
 * {@code passwordHash}: the compiler-generated record {@code toString()} would
 * otherwise render the submitted plaintext password if a bound instance were
 * ever logged.
 */
public record RegistrationRequest(

        @NotBlank
        @Email
        @Size(max = 254)
        String email,

        @NotBlank
        @ValidPassword
        String password) {

    /** Masks {@code password} so a log or diagnostic of a bound instance never renders the plaintext (SC-1, SEC-3). */
    @Override
    public String toString() {
        return "RegistrationRequest{email='" + email + "', password=***}";
    }
}
