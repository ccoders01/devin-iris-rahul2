package com.mrm.modelregistry.entity;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import jakarta.validation.ValidatorFactory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDateTime;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@ActiveProfiles("test")
class ModelTest {

    private Validator validator;
    private BusinessLineEntity businessLine;
    private ModelTypeEntity modelType;
    private RiskRatingEntity riskRating;
    private StatusEntity status;

    @BeforeEach
    void setUp() {
        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
        
        businessLine = new BusinessLineEntity("RETAIL_BANKING", "Retail Banking");
        modelType = new ModelTypeEntity("CREDIT_RISK", "Credit Risk");
        riskRating = new RiskRatingEntity("MEDIUM", "Medium");
        status = new StatusEntity("IN_DEVELOPMENT", "In Development");
    }

    @Test
    void constructor_ValidParameters_CreatesModel() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            businessLine,
            modelType,
            riskRating,
            status
        );

        assertEquals("Test Model", model.getModelName());
        assertEquals("v1.0", model.getModelVersion());
        assertEquals("Test Sponsor", model.getModelSponsor());
        assertEquals(businessLine, model.getBusinessLine());
        assertEquals(modelType, model.getModelType());
        assertEquals(riskRating, model.getRiskRating());
        assertEquals(status, model.getStatus());
    }

    @Test
    void validation_BlankModelName_FailsValidation() {
        Model model = new Model(
            "",
            "v1.0",
            "Test Sponsor",
            businessLine,
            modelType,
            riskRating,
            status
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
            businessLine,
            modelType,
            riskRating,
            status
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
            businessLine,
            modelType,
            riskRating,
            status
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
            modelType,
            riskRating,
            status
        );

        Set<ConstraintViolation<Model>> violations = validator.validate(model);

        assertFalse(violations.isEmpty());
        assertTrue(violations.stream().anyMatch(v -> v.getMessage().contains("Business line is required")));
    }

    @Test
    void entities_BusinessLine_HasCorrectDisplayNames() {
        assertEquals("Retail Banking", businessLine.getDisplayName());
        assertEquals("RETAIL_BANKING", businessLine.getCode());
    }

    @Test
    void entities_ModelType_HasCorrectDisplayNames() {
        assertEquals("Credit Risk", modelType.getDisplayName());
        assertEquals("CREDIT_RISK", modelType.getCode());
    }

    @Test
    void entities_RiskRating_HasCorrectDisplayNames() {
        assertEquals("Medium", riskRating.getDisplayName());
        assertEquals("MEDIUM", riskRating.getCode());
    }

    @Test
    void entities_Status_HasCorrectDisplayNames() {
        assertEquals("In Development", status.getDisplayName());
        assertEquals("IN_DEVELOPMENT", status.getCode());
    }

    @Test
    void prePersist_SetsCreatedAtAndUpdatedAt() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            businessLine,
            modelType,
            riskRating,
            status
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
            businessLine,
            modelType,
            riskRating,
            status
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
        model.setBusinessLine(businessLine);
        model.setModelType(modelType);
        model.setRiskRating(riskRating);
        model.setStatus(status);

        LocalDateTime now = LocalDateTime.now();
        model.setCreatedAt(now);
        model.setUpdatedAt(now);

        assertEquals(1L, model.getId());
        assertEquals("Test Model", model.getModelName());
        assertEquals("v1.0", model.getModelVersion());
        assertEquals("Test Sponsor", model.getModelSponsor());
        assertEquals(businessLine, model.getBusinessLine());
        assertEquals(modelType, model.getModelType());
        assertEquals(riskRating, model.getRiskRating());
        assertEquals(status, model.getStatus());
        assertEquals(now, model.getCreatedAt());
        assertEquals(now, model.getUpdatedAt());
    }
}
