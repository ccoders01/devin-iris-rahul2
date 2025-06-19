package com.mrm.modelregistry.dto;

import com.mrm.modelregistry.entity.Model;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class ModelRequestTest {

    private Validator validator;

    @BeforeEach
    void setUp() {
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
    }

    @Test
    void constructor_ValidParameters_CreatesModelRequest() {
        ModelRequest request = new ModelRequest(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        assertEquals("Test Model", request.getModelName());
        assertEquals("v1.0", request.getModelVersion());
        assertEquals("Test Sponsor", request.getModelSponsor());
        assertEquals(Model.BusinessLine.RETAIL_BANKING, request.getBusinessLine());
        assertEquals(Model.ModelType.CREDIT_RISK, request.getModelType());
        assertEquals(Model.RiskRating.MEDIUM, request.getRiskRating());
        assertEquals(Model.Status.IN_DEVELOPMENT, request.getStatus());
    }

    @Test
    void defaultConstructor_CreatesEmptyModelRequest() {
        ModelRequest request = new ModelRequest();

        assertNull(request.getModelName());
        assertNull(request.getModelVersion());
        assertNull(request.getModelSponsor());
        assertNull(request.getBusinessLine());
        assertNull(request.getModelType());
        assertNull(request.getRiskRating());
        assertNull(request.getStatus());
    }

    @Test
    void validation_BlankModelName_FailsValidation() {
        ModelRequest request = new ModelRequest(
            "",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Set<ConstraintViolation<ModelRequest>> violations = validator.validate(request);

        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("Model name is required")));
    }

    @Test
    void validation_NullModelName_FailsValidation() {
        ModelRequest request = new ModelRequest(
            null,
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Set<ConstraintViolation<ModelRequest>> violations = validator.validate(request);

        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("Model name is required")));
    }

    @Test
    void validation_BlankModelVersion_FailsValidation() {
        ModelRequest request = new ModelRequest(
            "Test Model",
            "",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Set<ConstraintViolation<ModelRequest>> violations = validator.validate(request);

        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("Model version is required")));
    }

    @Test
    void validation_BlankModelSponsor_FailsValidation() {
        ModelRequest request = new ModelRequest(
            "Test Model",
            "v1.0",
            "",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Set<ConstraintViolation<ModelRequest>> violations = validator.validate(request);

        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("Model sponsor is required")));
    }

    @Test
    void validation_NullBusinessLine_FailsValidation() {
        ModelRequest request = new ModelRequest(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            null,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Set<ConstraintViolation<ModelRequest>> violations = validator.validate(request);

        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("Business line is required")));
    }

    @Test
    void validation_ValidRequest_PassesValidation() {
        ModelRequest request = new ModelRequest(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Set<ConstraintViolation<ModelRequest>> violations = validator.validate(request);

        assertTrue(violations.isEmpty());
    }

    @Test
    void gettersAndSetters_WorkCorrectly() {
        ModelRequest request = new ModelRequest();

        request.setModelName("Test Model");
        request.setModelVersion("v1.0");
        request.setModelSponsor("Test Sponsor");
        request.setBusinessLine(Model.BusinessLine.RETAIL_BANKING);
        request.setModelType(Model.ModelType.CREDIT_RISK);
        request.setRiskRating(Model.RiskRating.MEDIUM);
        request.setStatus(Model.Status.IN_DEVELOPMENT);

        assertEquals("Test Model", request.getModelName());
        assertEquals("v1.0", request.getModelVersion());
        assertEquals("Test Sponsor", request.getModelSponsor());
        assertEquals(Model.BusinessLine.RETAIL_BANKING, request.getBusinessLine());
        assertEquals(Model.ModelType.CREDIT_RISK, request.getModelType());
        assertEquals(Model.RiskRating.MEDIUM, request.getRiskRating());
        assertEquals(Model.Status.IN_DEVELOPMENT, request.getStatus());
    }
}
