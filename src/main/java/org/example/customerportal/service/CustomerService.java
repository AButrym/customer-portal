package org.example.customerportal.service;

import org.example.customerportal.exception.DuplicateEmailException;
import org.example.customerportal.exception.InvalidPasswordException;
import org.example.customerportal.model.dto.CustomerResponse;
import org.example.customerportal.model.entity.Customer;
import org.example.customerportal.model.entity.Role;
import org.example.customerportal.model.request.RegistrationRequest;
import org.example.customerportal.repository.CustomerRepository;
import org.example.customerportal.validation.PasswordPolicyValidator;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Locale;

/**
 * Registration business logic (architecture.md AD-2 / AD-3 / AD-4).
 *
 * <p>Normalizes the email to lowercase (OD-006:A), re-checks the password policy
 * in bytes before hashing (FR-6, PD-2), rejects a duplicate email
 * (OD-003:A), BCrypt-hashes the password (SC-1), and persists an enabled
 * {@code CUSTOMER} account with UTC audit timestamps. Entity ↔ DTO mapping is
 * done here (PD-3).
 *
 * <p>The duplicate-email guard is check-then-act; two concurrent requests for
 * the same new email can both pass {@code existsByEmail} and race to
 * {@code save}. The loser's insert trips {@code uq_customer_email} as a
 * {@link DataIntegrityViolationException}; that single constraint is mapped to
 * the same {@link DuplicateEmailException} / {@code 409} as the pre-check path
 * (OD-003:A / AC-002). Any other integrity violation propagates unchanged so it
 * is not misreported as a duplicate email.
 */
@Service
public class CustomerService {

    private final CustomerRepository customerRepository;
    private final PasswordEncoder passwordEncoder;

    public CustomerService(CustomerRepository customerRepository, PasswordEncoder passwordEncoder) {
        this.customerRepository = customerRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional
    public CustomerResponse register(RegistrationRequest request) {
        String email = normalizeEmail(request.email());
        String password = request.password();

        // FR-6 / SC-1: service-layer policy re-check before hashing (defense in depth).
        if (!PasswordPolicyValidator.isCompliant(password)) {
            throw new InvalidPasswordException();
        }

        if (customerRepository.existsByEmail(email)) {
            throw new DuplicateEmailException();
        }

        Customer customer = new Customer();
        customer.setEmail(email);
        customer.setPasswordHash(passwordEncoder.encode(password));
        customer.setRole(Role.CUSTOMER);
        customer.setEnabled(true);

        try {
            // IDENTITY id generation forces the INSERT to run here, so a
            // uq_customer_email race surfaces inside this try (not at commit).
            return toResponse(customerRepository.save(customer));
        } catch (DataIntegrityViolationException ex) {
            if (isEmailUniquenessViolation(ex)) {
                throw new DuplicateEmailException();
            }
            throw ex;
        }
    }

    private static String normalizeEmail(String email) {
        return email == null ? null : email.trim().toLowerCase(Locale.ROOT);
    }

    /**
     * True only when {@code ex} was caused by the {@code uq_customer_email}
     * constraint — checked via the Hibernate constraint name and, as a fallback,
     * the message chain (H2 names the backing index after the constraint). A
     * violation of any other constraint returns {@code false} so it is not
     * mapped to a duplicate-email {@code 409}.
     */
    private static boolean isEmailUniquenessViolation(DataIntegrityViolationException ex) {
        for (Throwable cause = ex; cause != null; cause = cause.getCause()) {
            if (cause instanceof org.hibernate.exception.ConstraintViolationException hce) {
                String constraintName = hce.getConstraintName();
                if (constraintName != null
                        && constraintName.toLowerCase(Locale.ROOT).contains("uq_customer_email")) {
                    return true;
                }
            }
            String message = cause.getMessage();
            if (message != null && message.toLowerCase(Locale.ROOT).contains("uq_customer_email")) {
                return true;
            }
        }
        return false;
    }

    private static CustomerResponse toResponse(Customer customer) {
        return new CustomerResponse(
                customer.getId(),
                customer.getEmail(),
                customer.getRole().name(),
                customer.getCreatedAt());
    }
}
