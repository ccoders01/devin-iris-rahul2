package com.mrm.modelregistry.entity;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class ModelTest {

    private Validator validator;

    @BeforeEach
    void setUp() {
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
    }

    @Test
    void constructor_ValidParameters_CreatesModel() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        assertEquals("Test Model", model.getModelName());
        assertEquals("v1.0", model.getModelVersion());
        assertEquals("Test Sponsor", model.getModelSponsor());
        assertEquals(Model.BusinessLine.RETAIL_BANKING, model.getBusinessLine());
        assertEquals(Model.ModelType.CREDIT_RISK, model.getModelType());
        assertEquals(Model.RiskRating.MEDIUM, model.getRiskRating());
        assertEquals(Model.Status.IN_DEVELOPMENT, model.getStatus());
    }

    @Test
    void validation_BlankModelName_FailsValidation() {
        Model model = new Model(
            "",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Set<ConstraintViolation<Model>> violations = validator.validate(model);

        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("Model name is required")));
    }

    @Test
    void validation_BlankModelVersion_FailsValidation() {
        Model model = new Model(
            "Test Model",
            "",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Set<ConstraintViolation<Model>> violations = validator.validate(model);

        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("Model version is required")));
    }

    @Test
    void validation_BlankModelSponsor_FailsValidation() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Set<ConstraintViolation<Model>> violations = validator.validate(model);

        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("Model sponsor is required")));
    }

    @Test
    void validation_NullBusinessLine_FailsValidation() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            null,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Set<ConstraintViolation<Model>> violations = validator.validate(model);

        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("Business line is required")));
    }

    @Test
    void enums_BusinessLine_HasCorrectDisplayNames() {
        assertEquals("Retail Banking", Model.BusinessLine.RETAIL_BANKING.getDisplayName());
        assertEquals("Wholesale Lending", Model.BusinessLine.WHOLESALE_LENDING.getDisplayName());
        assertEquals("Investment Banking", Model.BusinessLine.INVESTMENT_BANKING.getDisplayName());
        assertEquals("Risk Management", Model.BusinessLine.RISK_MANAGEMENT.getDisplayName());
    }

    @Test
    void enums_ModelType_HasCorrectDisplayNames() {
        assertEquals("Credit Risk", Model.ModelType.CREDIT_RISK.getDisplayName());
        assertEquals("Market Risk", Model.ModelType.MARKET_RISK.getDisplayName());
        assertEquals("Operational Risk", Model.ModelType.OPERATIONAL_RISK.getDisplayName());
        assertEquals("AML", Model.ModelType.AML.getDisplayName());
        assertEquals("Capital Calculation", Model.ModelType.CAPITAL_CALCULATION.getDisplayName());
        assertEquals("Valuation", Model.ModelType.VALUATION.getDisplayName());
    }

    @Test
    void enums_RiskRating_HasCorrectDisplayNames() {
        assertEquals("High", Model.RiskRating.HIGH.getDisplayName());
        assertEquals("Medium", Model.RiskRating.MEDIUM.getDisplayName());
        assertEquals("Low", Model.RiskRating.LOW.getDisplayName());
    }

    @Test
    void enums_Status_HasCorrectDisplayNames() {
        assertEquals("In Development", Model.Status.IN_DEVELOPMENT.getDisplayName());
        assertEquals("Validated", Model.Status.VALIDATED.getDisplayName());
        assertEquals("Production", Model.Status.PRODUCTION.getDisplayName());
        assertEquals("Retired", Model.Status.RETIRED.getDisplayName());
    }

    @Test
    void prePersist_SetsCreatedAtAndUpdatedAt() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        LocalDateTime beforePersist = LocalDateTime.now();
        model.onCreate();
        LocalDateTime afterPersist = LocalDateTime.now();

        assertNotNull(model.getCreatedAt());
        assertNotNull(model.getUpdatedAt());
        assertTrue(model.getCreatedAt().isAfter(beforePersist.minusSeconds(1)));
        assertTrue(model.getCreatedAt().isBefore(afterPersist.plusSeconds(1)));
        assertTrue(model.getUpdatedAt().isAfter(beforePersist.minusSeconds(1)));
        assertTrue(model.getUpdatedAt().isBefore(afterPersist.plusSeconds(1)));
    }

    @Test
    void preUpdate_UpdatesUpdatedAt() throws InterruptedException {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        model.onCreate();
        LocalDateTime originalUpdatedAt = model.getUpdatedAt();

        Thread.sleep(10);

        model.onUpdate();

        assertNotNull(model.getUpdatedAt());
        assertTrue(model.getUpdatedAt().isAfter(originalUpdatedAt));
    }

    @Test
    void gettersAndSetters_WorkCorrectly() {
        Model model = new Model();

        model.setId(1L);
        model.setModelName("Test Model");
        model.setModelVersion("v1.0");
        model.setModelSponsor("Test Sponsor");
        model.setBusinessLine(Model.BusinessLine.RETAIL_BANKING);
        model.setModelType(Model.ModelType.CREDIT_RISK);
        model.setRiskRating(Model.RiskRating.MEDIUM);
        model.setStatus(Model.Status.IN_DEVELOPMENT);

        LocalDateTime now = LocalDateTime.now();
        model.setCreatedAt(now);
        model.setUpdatedAt(now);

        assertEquals(1L, model.getId());
        assertEquals("Test Model", model.getModelName());
        assertEquals("v1.0", model.getModelVersion());
        assertEquals("Test Sponsor", model.getModelSponsor());
        assertEquals(Model.BusinessLine.RETAIL_BANKING, model.getBusinessLine());
        assertEquals(Model.ModelType.CREDIT_RISK, model.getModelType());
        assertEquals(Model.RiskRating.MEDIUM, model.getRiskRating());
        assertEquals(Model.Status.IN_DEVELOPMENT, model.getStatus());
        assertEquals(now, model.getCreatedAt());
        assertEquals(now, model.getUpdatedAt());
    }
}
